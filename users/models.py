import re

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


def validate_string_field(value):
    reg = re.compile('^[a-zA-Z ]+$')
    if not reg.match(value):
        raise ValidationError(_("%(value)s is not a valid string"),
                              params={'value': value})


def validate_negative_field(value):
    if value <= 0:
        raise ValidationError(_("%(value)s should be greater than zero"),
                              params={'value': value})


def validate_cnic_field(value):
    reg = re.compile("^[0-9]{5}[0-9]{7}[0-9]{1}$")
    if not reg.match(value):
        raise ValidationError(_("%(value)s is invalid cnic number"),
                              params={'value': value})


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
    username = models.CharField(max_length=250, null=True, blank=True, validators=[validate_string_field])
    phone_number = PhoneNumberField(blank=True, null=True)
    address = models.CharField(max_length=250, default="")
    cnic = models.CharField(max_length=100, unique=True, validators=[validate_cnic_field])
    gender = models.CharField(max_length=200, choices=CHOICES, default=None)

    def __str__(self):
        return self.username


class Post(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, null=True, blank=True, validators=[validate_string_field])
    categorie = models.CharField(max_length=250, null=True, blank=True, validators=[validate_string_field])
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.categorie
