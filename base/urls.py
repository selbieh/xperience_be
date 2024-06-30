from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PolicyViewSet, FAQViewSet, NotificationViewSet, AdminNotificationViewSet

router = DefaultRouter()
router.register(r'policy', PolicyViewSet, basename='policy')
router.register(r'faqs', FAQViewSet)
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'admin-notifications', AdminNotificationViewSet, basename='admin_notification')



urlpatterns = [
    path('', include(router.urls)),
]