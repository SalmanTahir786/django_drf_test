from datetime import datetime

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    CHOICES = (
        ("MALE", "male"),
        ("FEMALE", "female"),
    )
    email = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user_profile')
    username = models.CharField(max_length=250, null=True, blank=True)
    phone_number = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=250, default="")
    cnic = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=200, choices=CHOICES, default=None)

    def __str__(self):
        return self.username


class Post(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, null=True, blank=True)
    categorie = models.CharField(max_length=250, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.categorie

