from django.urls import path
from .views import UserProfileViewSet

urlpatterns = [
    path('api/profile/', UserProfileViewSet.as_view(), name='user_profile'),
]
