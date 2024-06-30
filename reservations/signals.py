from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Reservation
from firebase_admin.messaging import Message, Notification
from fcm_django.models import FCMDevice
from base.models import UserNotification, AdminNotification



@receiver(post_save, sender=Reservation)
def message_handler(sender, instance, created, **kwargs):
    status = instance.status
    if status == 'WAITING_FOR_PAYMENT':
        title = 'Reservation Updates'
        body1=f'Reservation of user {instance.user.name} has been Confirmed'
    elif status == 'CONFIRMED':
        title = 'Reservation Updates'
        body= 'Your Reservation is Confirmed'
        body1=f'Reservation of user {instance.user.name} has been Confirmed'
    elif status == 'CANCELLED':
        title = 'Reservation Updates'
        body1=f'Reservation of user {instance.user.name} has been Confirmed'
    elif status == 'COMPLETED':
        title = 'Reservation Updates'
        body= 'You have earned 100 Points'
        body1=f'User {instance.user.name} has been earned Points'

    try:
        register_tokens = FCMDevice.objects.filter(user=instance.user)
        register_tokens.send_message(Message(notification=Notification(
            title=title,
            body=body
        )))
        
        admin_register_tokens = FCMDevice.objects.filter(user__is_staff=True)
        admin_register_tokens.send_message(Message(notification=Notification(
            title=title,
            body=body1
        )))

        UserNotification.objects.create(
            user=instance.user,
            title=title,
            body=body
        )

        AdminNotification.objects.create(
            user=instance.user,
            title=title,
            body=body1,
            reservation=instance
        )
    except Exception as e:
        print(e)
