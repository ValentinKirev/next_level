from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from next_level import settings
from next_level.accounts.models import Profile

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_profile(sender, instance, created, **kwargs):
    if created:
        subject = 'Registration greetings'
        html_message = render_to_string('email-greeting.html', {'user': instance})
        plain_message = strip_tags(html_message)
        to = instance.email

        send_mail(subject=subject,
                  message=plain_message,
                  from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[to],
                  html_message=html_message)

        Profile.objects.create(user=instance)