from django.core.mail import send_mail
from celery import shared_task


@shared_task
def send_reminder_email(subject, message, from_email, recipient_list):
    send_mail(subject, message, from_email, recipient_list)
