from tabnanny import verbose
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=255, verbose_name="First name")
    last_name = models.CharField(max_length=255, verbose_name="Last name")
    email = models.EmailField(max_length=254, verbose_name="E-mail")

    class Roles(models.TextChoices):
        DEVELOPER = "developer"
        MANAGER = "manager"
        ADMIN = "admin"

    role = models.CharField(
        max_length=255,
        verbose_name="Role",
        default=Roles.DEVELOPER,
        choices=Roles.choices,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["last_name"]
