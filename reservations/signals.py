from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Reservation
from firebase_admin.messaging import Message, Notification
from fcm_django.models import FCMDevice
from base.models import UserNotification, AdminNotification
import logging

logger = logging.getLogger(__name__)

# Helper function for sending notifications
def send_reservation_notifications(reservation, created):
    current_status = reservation.status
    title, body, body1 = '', '', ''
    logger.critical(f"first line of send notification for {reservation.id} with status {current_status}")

    if current_status == 'WAITING_FOR_PAYMENT':
        title = 'Reservation Updates'
        body = 'Your Reservation is Waiting for Payment'
        body1 = f'Reservation of user {reservation.user.name} is Waiting for Payment'

    elif current_status == 'CONFIRMED':
        title = 'Reservation Updates'
        body = 'Your Reservation has been Confirmed'
        body1 = f'Reservation of user {reservation.user.name} has been Confirmed'

    elif current_status == 'CANCELLED':
        title = 'Reservation Updates'
        body = 'Your Reservation has been Cancelled'
        body1 = f'Reservation of user {reservation.user.name} has been Cancelled'

    elif current_status == 'COMPLETED':
        title = 'Reservation Updates'
        body = 'You have earned Points'
        body1 = f'User {reservation.user.name} has earned Points'
        total_points = 0

        hotel_reservations = reservation.hotel_reservations.all()
        for hotel_reservation in hotel_reservations:
            if hotel_reservation.hotel_service.points:
                total_points += hotel_reservation.hotel_service.points

        car_reservations = reservation.car_reservations.all()
        for car_reservation in car_reservations:
            if car_reservation.subscription_option and car_reservation.subscription_option.points:
                total_points += car_reservation.subscription_option.points

        if reservation.user.points is None:
            reservation.user.points = 0

        reservation.user.points += total_points
        reservation.user.save()

        body = f'You have earned {total_points} Points'
        body1 = f'User {reservation.user.name} has earned {total_points} Points'

    elif current_status == 'WAITING_FOR_CONFIRMATION':
        title = 'Reservation Updates'
        body = 'Your Reservation is Waiting For Confirmation'
        body1 = f'Reservation of user {reservation.user.name} is Waiting for Confirmation'

    elif current_status == 'PAID':
        title = 'Reservation Updates'
        body = 'Your Reservation has been Paid'
        body1 = f'Reservation of user {reservation.user.name} has been Paid'

    elif current_status == 'REFUNDED':
        title = 'Reservation Updates'
        body = 'Your Reservation has been Refunded'
        body1 = f'Reservation of user {reservation.user.name} has been Refunded'

    else:
        pass


    logger.critical(f"Sending notifications for reservation {reservation.id} of user {reservation.user} with status {current_status}")

    # Send notifications to the user
    register_tokens = FCMDevice.objects.filter(user=reservation.user)
    register_tokens.send_message(Message(notification=Notification(
        title=title,
        body=body
    )))
    logger.critical(f"the register tokens: {register_tokens}")

    # Send notifications to the admin
    admin_register_tokens = FCMDevice.objects.filter(user__is_staff=True)
    admin_register_tokens.send_message(Message(notification=Notification(
        title=title,
        body=body1
    )))
    logger.critical(f"the admins register tokens: {admin_register_tokens}")

    # Create notifications records
    UserNotification.objects.create(
        user=reservation.user,
        title=title,
        body=body
    )

    AdminNotification.objects.create(
        user=reservation.user,
        title=title,
        body=body1,
        reservation=reservation
    )

    logger.critical(f"Notifications sent successfully for reservation {reservation.id}")
