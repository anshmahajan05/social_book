# signals.py

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

@receiver(user_logged_in)
def send_login_notification(sender, user, request, **kwargs):
    subject = 'Social Book Login Notification'
    message = f'Hello {user.username}, you have successfully logged in to your account on Social Book.'
    from_email = settings.EMAIL_HOST_USER
    to_email = user.email
    print(subject, message, from_email, [to_email])
    send_mail(subject, message, from_email, [to_email])
    print("Mail Successfully sended")
