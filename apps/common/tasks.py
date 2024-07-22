import json
import time

from django.conf import settings
from django.urls import reverse
from google.cloud import tasks_v2beta3
from google.protobuf import timestamp_pb2

if settings.GOOGLE_CLOUD_TASKS_ON_GAE:
    cloud_task_client = tasks_v2beta3.CloudTasksClient()

else:
    import grpc
    from google.cloud.tasks_v2 import CloudTasksClient
    from google.cloud.tasks_v2.services.cloud_tasks.transports import (
        CloudTasksGrpcTransport,
    )

    # address from running https://github.com/aertje/cloud-tasks-emulator
    channel = grpc.insecure_channel(settings.GOOGLE_CLOUD_TASKS_CHANNEL)
    transport = CloudTasksGrpcTransport(channel=channel)
    cloud_task_client = CloudTasksClient(transport=transport)


def create_task(
    uri,
    queue=settings.GOOGLE_CLOUD_TASKS_DEFAULT_QUEUE,
    payload=None,
    schedule_time=None,
    name=None,
):
    """Create a task for a qiven queue and payload"""
    parent = cloud_task_client.queue_path(
        settings.GOOGLE_CLOUD_TASKS_PROJECT,
        settings.GOOGLE_CLOUD_TASKS_PROJECT_LOCATION,
        queue,
    )

    # google tasks handler urls
    handler = {
        "send-email": reverse("api:common-send-email"),
        "verify-id": reverse("api:common-verify-id"),
        # "commercial-orders": reverse("api:common-commercial-orders"),
        "send-notification": reverse("api:notifications-send-notification"),
        # "send_notification": reverse("notifications-send-notification"),
        "send-sms": reverse("api:common-send-sms"),
        # "send_sms": reverse("notifications-send-sms"),
    }

    # print("url: ", reverse("api:notifications-send-notification"))

    if settings.GOOGLE_CLOUD_TASKS_ON_GAE:
        task = {
            "app_engine_http_request": {
                "http_method": tasks_v2beta3.HttpMethod.POST,
                "relative_uri": handler[uri],
                "app_engine_routing": {"service": settings.GAE_SERVICE},
            },
        }
    else:
        task = {
            "http_request": {  # Specify the type of request.
                "http_method": tasks_v2beta3.HttpMethod.POST,
                "url": f"http://127.0.0.1:8000{handler[uri]}",  # The full url path that the task will be sent to.
            }
        }

    # if not settings.GOOGLE_CLOUD_TASKS_ON_GAE:
    #     # disable app engine routing for app engine emulation
    #     task["app_engine_http_request"]["app_engine_routing"] = {}

    if name:
        task["name"] = name

    if isinstance(payload, dict):
        payload = json.dumps(payload)

    if payload is not None:
        converted_payload = payload.encode()
        if settings.GOOGLE_CLOUD_TASKS_ON_GAE:
            task["app_engine_http_request"]["body"] = converted_payload
        else:
            task["http_request"]["body"] = converted_payload

    if schedule_time is not None:
        now = time.time() + schedule_time
        seconds = int(now)
        nanos = int(now - seconds) * 10**9

        # create timestamp protobuf
        timestamp = timestamp_pb2.Timestamp(seconds=seconds, nanos=nanos)

        # add timestamp to task
        task["schedule_time"] = timestamp

    resp = cloud_task_client.create_task(parent=parent, task=task)

    # TODO: Use logger although this is still picked up in stackdriver
    return resp
