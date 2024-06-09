from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PolicyViewSet, FAQViewSet

router = DefaultRouter()
router.register(r'policy', PolicyViewSet, basename='policy')
router.register(r'faqs', FAQViewSet)


urlpatterns = [
    path('', include(router.urls)),
]