from django.conf import settings
from django.core.mail import EmailMessage


def send_email(to_email, subject, message, fail_silently=True):
    """
    Helper to send emails system wide.
    Special consideration made for sendgrid's dynamic templating.

    https://docs.sendgrid.com/ui/sending-email/how-to-send-an-email-with-dynamic-transactional-templates
    """
    msg = EmailMessage(
        subject,
        message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
        reply_to=[settings.DEFAULT_FROM_EMAIL],
    )

    return msg.send(fail_silently=fail_silently)


def send_email_template(
    email, template_id: str, dynamic_template_data: dict = None, fail_silently=True
):
    """
    Helper to send emails system wide.
    Special consideration made for sendgrid's dynamic templating.

    https://docs.sendgrid.com/ui/sending-email/how-to-send-an-email-with-dynamic-transactional-templates
    """
    msg = EmailMessage(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
        reply_to=[settings.DEFAULT_FROM_EMAIL],
    )
    msg.template_id = template_id

    if dynamic_template_data:
        msg.dynamic_template_data = dynamic_template_data
        msg.merge_global_data = dynamic_template_data

    return msg.send(fail_silently=fail_silently)
