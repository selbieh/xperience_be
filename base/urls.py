from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PolicyViewSet, FAQViewSet, NotificationViewSet

router = DefaultRouter()
router.register(r'policy', PolicyViewSet, basename='policy')
router.register(r'faqs', FAQViewSet)
router.register(r'notifications', NotificationViewSet, basename='notification')


urlpatterns = [
    path('', include(router.urls)),
]