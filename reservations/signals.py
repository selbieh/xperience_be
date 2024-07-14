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
        body= 'Your Reservation is Waiting for Payment'
        body1=f'Reservation of user {instance.user.name} is Waiting for Payment'

    elif status == 'CONFIRMED':
        title = 'Reservation Updates'
        body= 'Your Reservation has been Confirmed'
        body1=f'Reservation of user {instance.user.name} has been Confirmed'

    elif status == 'CANCELLED':
        title = 'Reservation Updates'
        body= 'Your Reservation has been Cancelled'
        body1=f'Reservation of user {instance.user.name} has been Cancelled'

    elif status == 'COMPLETED':
        title = 'Reservation Updates'
        body = 'You have earned Points'
        body1 = f'User {instance.user.name} has earned Points'
        total_points = 0

        hotel_reservations = instance.hotel_reservations.all()
        for hotel_reservation in hotel_reservations:
            if hotel_reservation.hotel_service.points:
                total_points += hotel_reservation.hotel_service.points

        car_reservations = instance.car_reservations.all()
        for car_reservation in car_reservations:
            if car_reservation.subscription_option and car_reservation.subscription_option.points:
                total_points += car_reservation.subscription_option.points

        if instance.user.points is None:
            instance.user.points = 0

        instance.user.points += total_points
        instance.user.save()

        body = f'You have earned {total_points} Points'
        body1 = f'User {instance.user.name} has earned {total_points} Points'

    elif status == 'WAITING_FOR_CONFIRMATION':
        title = 'Reservation Updates'
        body= 'Your Reservation is Waiting For Confirmation'
        body1=f'Reservation of user {instance.user.name} is Waiting for Confirmation'

    elif status == 'PAID':
        title = 'Reservation Updates'
        body= 'Your Reservation has been Paid'
        body1=f'Reservation of user {instance.user.name} has been Paid'

    elif status == 'REFUNDED':
        title = 'Reservation Updates'
        body= 'Your Reservation has been Refunded'
        body1=f'Reservation of user {instance.user.name} has been Refunded'


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
