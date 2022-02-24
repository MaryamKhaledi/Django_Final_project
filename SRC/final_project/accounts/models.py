from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.db import models
import re
from .managers import UserManager


def valid_username(username):
    email_made = re.search('@eml.com$', username)
    if email_made is not None:
        raise ValidationError('Note that you must write the name without a domain')


class User(AbstractUser):
    RECOVERY_CHOICES = (
        ('phone_number', 'Phone'),
        ('email_address', 'Email'),
    )
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    username = models.CharField(_('username'), validators=[valid_username], max_length=60, unique=True,
                                help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                                error_messages={'unique': _("A accounts with that username already exists."),
                                                })
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    recovery = models.CharField(max_length=15, choices=RECOVERY_CHOICES, default='')
    email = models.CharField(unique=True, max_length=60)
    phone_number = models.CharField(max_length=15, unique=True, validators=[], help_text='', error_messages={})
    # password = models.CharField(max_length=64, )
    birth_date = models.DateTimeField(null=True, )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    country = models.CharField(max_length=50, null=True)
    is_active = models.BooleanField(default=False)
    # is_staff = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'username'  # بهش گفتم فیلد اصلی برای ورود یورزر نیم باشه
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
