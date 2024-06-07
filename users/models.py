from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group
from phonenumber_field.modelfields import PhoneNumberField
from .managers import CustomUserManager


class User(AbstractUser):
    username = None
    mobile = PhoneNumberField(region='EG', blank=False, null=False, unique=True)
    USERNAME_FIELD = "mobile"
    REQUIRED_FIELDS = []
    wallet = models.IntegerField(default=0)
    name = models.CharField(max_length=245, blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name=("groups"),
        blank=True,
        help_text=(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="user_groups",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=("user permissions"),
        blank=True,
        help_text=("Specific permissions for this user."),
        related_name="user_permissions",
        related_query_name="user",
    )

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.mobile}'

    class Meta:
        indexes = [
            models.Index(fields=['mobile']),
        ]
        
class Location(models.Model):
    user = models.ForeignKey(User, related_name="locations", on_delete=models.CASCADE)
    name = models.CharField(max_length=245)
    address = models.CharField(max_length=245)
    location_lat = models.FloatField(null=True, blank=True)
    location_long = models.FloatField(null=True, blank=True)
    location_url = models.URLField(max_length=500, null=True, blank=True)

