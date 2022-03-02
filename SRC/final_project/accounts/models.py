from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.db import models
import re
from .managers import UserManager


def valid_username(username):
    """ Validation of the entered username """
    email_made = re.search('@eml.com$', username)
    if email_made is not None:
        raise ValidationError('Note that you must write the name without a domain')


def valid_phone_number(phone_number):
    """ Validation of the entered phone number """
    phone_number_made = re.search("/^([+]?\d{1,2}[-\s]?|)\d{3}[-\s]?\d{3}[-\s]?\d{4}$/", phone_number)
    if phone_number_made is not None:
        raise ValidationError('The entered phone number is incorrect')


class User(AbstractUser):
    """Users model"""
    RECOVERY_CHOICES = (
        ('phone_number', 'Phone'),
        ('email_address', 'Email'),
    )
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    username = models.CharField(_('username'), validators=[valid_username], max_length=50, unique=True,
                                help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                                error_messages={'unique': _("A accounts with that username already exists."),
                                                })
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    recovery = models.CharField(max_length=15, choices=RECOVERY_CHOICES, default='')
    email = models.CharField(unique=True, max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=13, unique=True, validators=[valid_phone_number], blank=True, null=True,
                                    help_text=_('The number of characters entered must be at least 12 and at most 13 '
                                                'digits and must start with +.'),
                                    error_messages={"The mobile number is incorrect"})
    birth_date = models.DateTimeField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    country = models.CharField(max_length=40, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'username'  # field asli baraye verod ,username bashe
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
