from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


<<<<<<< HEAD
class User(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
=======
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255, verbose_name="First name")
    last_name = models.CharField(max_length=255, verbose_name="Last name")
    email = models.EmailField(max_length=254, verbose_name="E-mail", unique=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ()
>>>>>>> e90f94348b26b5cd6185b1d3e857665259a0a24a

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

<<<<<<< HEAD
    def __str__(self):
        return f"{self.first_name[:1]}.{self.last_name} [{self.role[:1]}][id{self.id}]"
=======
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name[:1]}.{self.last_name}.{self.role[:3]}.id{self.id}"
>>>>>>> e90f94348b26b5cd6185b1d3e857665259a0a24a

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
