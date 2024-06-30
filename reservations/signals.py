from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Reservation
from firebase_admin.messaging import Message, Notification
from fcm_django.models import FCMDevice
from base.models import UserNotification



@receiver(post_save, sender=Reservation)
def message_handler(sender, instance, created, **kwargs):
    status = instance.status
    if status == 'WAITING_FOR_PAYMENT':
        title = 'Reservation Updates'
        body= 'Your Reservation is Waiting for Payment'
    elif status == 'CONFIRMED':
        title = 'Confirmed'
        body= 'Your Reservation is Confirmed'
    elif status == 'CANCELLED':
        title = 'Cancelled'
        body= 'Your Reservation is Cancelled'
    elif status == 'COMPLETED':
        title = 'Completed'
        body= 'You have earned 100 Points'

    try:
        register_tokens = FCMDevice.objects.filter(user=instance.user)
        register_tokens.send_message(Message(notification=Notification(
            title=title,
            body=body
        )))

        UserNotification.objects.create(
            user=instance.user,
            title=title,
            body=body
        )
    except Exception as e:
        print(e)
