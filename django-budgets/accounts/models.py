from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext as _


class UserProfileManager(UserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.password = make_password(password)
            user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class UserProfile(AbstractUser):

    username = None
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserProfileManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm: str, obj=None) -> bool:
        return super().has_perm(perm, obj)
