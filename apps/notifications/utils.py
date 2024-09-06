# from django.conf import settings
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification

# from twilio.rest import Client


# Manually handle notification on app
def send_fcm(user, title, data=None):
    """Send Firebase Cloud Messaging notifications"""

    device = FCMDevice.objects.filter(user=user).first()
    if device:
        title = title or "Notification"
        device.send_message(
            Message(
                data=data,
            )
        )


# Manually handle notification on app
def send_fcm_bulk(title, data=None):
    """Send Firebase Cloud Messaging notifications"""

    devices = FCMDevice.objects.all()
    title = title or "Notification"
    devices.send_message(
        Message(
            data=data,
        )
    )


# FCM handle notification on app automatically
def fcm_notify(user, title, body, custom_data={}):
    device = FCMDevice.objects.filter(user=user).first()
    if device:
        device.send_message(
            Message(notification=Notification(title=title, body=body), data=custom_data)
        )


# FCM handle notification on app automatically
def fcm_notify_bulk(title, body, custom_data={}, devices=None):
    if devices:
        devices = devices
    else:
        devices = FCMDevice.objects.all()
    devices.send_message(
        Message(notification=Notification(title=title, body=body), data=custom_data)
    )


def send_notification(user=None, data=None):
    """Util function to send nofication with cloud task"""

    from api_project.common.tasks import create_task

    payload = {
        "user_id": str(user.pk) if user else None,
        "data": {
            "title": data["title"] if hasattr(data, "title") else "Notification",
            "body": data["body"] if hasattr(data, "body") else "",
        },
    }

    create_task("send-notification", payload=payload)


# Send sms
# def send_sms(phone_number, message):
#     client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#     client.messages.create(
#         body=message,
#         from_=settings.TWILIO_NUMBER,
#         to=f"{phone_number}",
#     )
