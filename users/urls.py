from django.urls import path
from .views import UserProfileViewSet, CustomObtainAuthToken


urlpatterns = [
    path('user/profile/', UserProfileViewSet.as_view(), name='user_profile'),
]
