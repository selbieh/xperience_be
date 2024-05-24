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
        return self.mobile


class locations(models.Model):
    user = models.ForeignKey(User, related_name="locations", on_delete=models.CASCADE)
    name = models.CharField(max_length=245)
    location = models.CharField(max_length=245, null=False)

