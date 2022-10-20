from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Roles(models.TextChoices):
        DEVELOPER = "Developer"
        MANAGER = "Manager"
        ADMIN = "Admin"

    role = models.CharField(
        max_length=255,
        verbose_name="Role",
        default=Roles.DEVELOPER,
        choices=Roles.choices,
    )

    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name[:1]}.{self.last_name} [{self.role[:1]}][id{self.id}]"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
