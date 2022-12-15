from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from next_level.accounts.models import Profile
from next_level.accounts.tasks import send_greeting_email

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_profile(sender, instance, created, **kwargs):
    if created:
        subject = 'Registration greetings'
        html_message = render_to_string('email-greeting.html', {'user': instance})
        plain_message = strip_tags(html_message)
        to = instance.email

        send_greeting_email.delay(subject, plain_message, to, html_message)

        Profile.objects.create(user=instance)

