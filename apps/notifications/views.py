import json

from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.common.email import send_email_template
from apps.common.permissions import IsTask

from .utils import fcm_notify, fcm_notify_bulk  # send_sms

User = get_user_model()


class NotificationViewSet(ViewSet):
    permission_classes = [IsTask]

    @action(methods=["post"], detail=False, url_path="send-notification")
    def send_notification(self, request):
        req = json.loads(request.body.decode())

        data = req.get("data")
        user_id = req.get("user_id")
        title = data.get("title", None)
        body = data.get("body")

        # if user_id use single else use bulk
        if user_id:
            user = User.objects.filter(pk=user_id).first()
            if user:
                fcm_notify(user, title=title, body=body, custom_data=data)
                # send_fcm(user, title=title, data=data)
        else:
            fcm_notify_bulk(title, body, custom_data=data)
            # send_fcm_bulk(title, data=data)

        return Response("OK", status=200)

    @action(methods=["POST"], detail=False, url_path="send-email")
    def send_email(self, request):
        """
        Endpoint used in conjuction with cloud task to send emails
        """
        body = json.loads(request.body.decode())

        to_email = body["to_email"]
        template_id = body["template_id"]
        dynamic_template_data = body["dynamic_template_data"]
        fail_silently = body["fail_silently"]

        send_email_template(
            to_email,
            template_id,
            dynamic_template_data=dynamic_template_data,
            fail_silently=fail_silently,
        )

        return Response("OK", status=200)

    # @action(detail=False, methods=["POST"], url_path="send-sms")
    # def send_sms(self, request):
    #     """
    #     Endpoint used in conjuction with cloud task to send sms
    #     """
    #     body = json.loads(request.body.decode())
    #     phone_number = body.get("phone_number")
    #     message = body.get("message")

    #     send_sms(phone_number, message)

    #     return Response("OK", status=200)
