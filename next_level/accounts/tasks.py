from celery import shared_task
from django.core.mail import send_mail

from next_level import settings


@shared_task
def send_greeting_email(subject, plain_message, to, html_message):
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[to],
        html_message=html_message
    )