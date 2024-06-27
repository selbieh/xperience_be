from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Reservation
from firebase_admin.messaging import Message, Notification
from fcm_django.models import FCMDevice



@receiver(post_save, sender=Reservation)
def message_handler(sender, instance, created, **kwargs):
    status = instance.status
    if status == 'WAITING_FOR_PAYMENT':
        title = 'Reservation Updates'
        body= 'Your Reservaytion is Waiting for payment now'
    elif status == 'CONFIRMED':
        title = 'Confirmed'
        body= 'Your Reservaytion is Confirmed'
    elif status == 'CANCELLED':
        title = 'Cancelled'
        body= 'Your Reservaytion is Cancelled'
    elif status == 'COMPLETED':
        title = 'Completed'
        body= 'You have earned 100 points'

    try:
        register_tokens = FCMDevice.objects.filter(user=instance.user)
        register_tokens.send_message(Message(notification=Notification(
            title=title,
            body=body
        )))
    except Exception as e:
        print(e)
