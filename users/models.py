from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    username = None
    phone_number = PhoneNumberField(region='EG', blank=False, null=False, unique=True)
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []
    wallet = models.IntegerField(default=0)

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
