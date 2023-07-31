from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from celery import shared_task
from onlineShop import settings


@shared_task(bind=True)
def send_mail_fun(self):
    superusers = get_user_model().objects.filter(is_superuser=True)
    for superuser in superusers:
        mail_subject = "Product added"
        message = "new product added"
        to_email = superuser.email
        sent_mail = send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=False,
        )
    return "Done"
