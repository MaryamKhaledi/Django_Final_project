from enum import unique

from django.core.exceptions import ValidationError
from taggit.managers import TaggableManager

from accounts.models import User, valid_phone_number
from django.utils.translation import ugettext as _
from django.db import models


def file_size(value):
    """ Check the accuracy of the uploaded file size """
    limit = 26214400  # 20971520+5342880
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 25 MiB.')


class Label(models.Model):
    """ Emails can be categorized by label """
    title = models.CharField(max_length=30, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="label_owner")

    # todo : add unique_together
    class Meta:
        unique_together = ['title', 'owner']

    def __str__(self):
        return self.title


class Signature(models.Model):
    """Add name in the email sent """
    user = models.OneToOneField(User, on_delete=models.PROTECT, max_length=50)
    is_send = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.is_send


class Contacts(models.Model):
    """ Add people as contacts """
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=60)
    phone_number = models.CharField(max_length=13, blank=True, null=True, validators=[valid_phone_number],
                                    help_text=_('The number of characters entered must be at least 12 and at most 13 '
                                                'digits and must start with +.'))
    birth_date = models.DateTimeField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts_owner")

    def __str__(self):
        return self.name, self.email


class Email(models.Model):
    """ Email class and its fields """
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('send', 'Send')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    signature = models.ForeignKey(Signature, on_delete=models.PROTECT, related_name="signature",
                                  blank=True, null=True)
    # contacts = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True,
    #                              related_name="contacts")
    # receiver = models.ManyToManyField(User, related_name="receiver")
    receiver = models.CharField(max_length=50, help_text=_('username@eml.com'))
    # cc = models.ManyToManyField(User, related_name="cc", blank=True)
    cc = models.CharField(max_length=500, null=True, blank=True)
    # bcc = models.ManyToManyField(User, related_name="bcc", blank=True)
    bcc = models.CharField(max_length=500, null=True, blank=True)
    subject = models.CharField(max_length=100, blank=True, null=True)
    label = models.ManyToManyField(Label, blank=True, )
    body = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='', validators=[file_size], blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # زمان ارسال ایمیل
    is_read = models.BooleanField(default=False, )  # فیلد read هم مربوط به این هستش آیا اون ایمیل خونده شده یا نه؟
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='remail', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False, blank=True, null=True)
    is_trash = models.BooleanField(default=False, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    # tags = TaggableManager()

    # فیلد archived هم مربوط به این هستش که آیا کاربر اون ایمیل رو آرشیو کرده یا نه.

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"From: {self.signature}, Sub: {self.subject}"

# class Profile(models.Model):
#     accounts = models.OneToOneField(User, on_delete=models.CASCADE)
#     email_confirmed = models.BooleanField(default=False)


# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(accounts=instance)
#     instance.profile.save()
