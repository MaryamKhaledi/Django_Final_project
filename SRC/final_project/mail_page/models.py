from enum import unique
from django.core.exceptions import ValidationError
from taggit.managers import TaggableManager
from accounts.models import User, valid_phone_number
from django.utils.translation import ugettext as _
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


def file_size(value):
    """ Check the accuracy of the uploaded file size """
    limit = 26214400  # 20971520+5342880
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 25 MiB.')


class Label(models.Model):
    """ Emails can be categorized by label """
    title = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="label_owner")

    class Meta:
        unique_together = ['title', 'owner']

    def __str__(self):
        return self.title


class Signature(models.Model):
    """Add name in the email sent """
    owner = models.ForeignKey(User, on_delete=models.PROTECT, max_length=50)
    title = models.CharField(max_length=300)

    # is_send = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.title


class Contacts(models.Model):
    """ Add people as contacts """
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=60)
    phone_number = models.CharField(max_length=13, blank=True, null=True, validators=[valid_phone_number],
                                    help_text=('The number of characters entered must be at least 12 and at most 13 '
                                               'digits and must start with +.'))
    other_email = models.CharField(max_length=60, blank=True, null=True)
    birth_date = models.DateTimeField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts_owner")

    def __str__(self):
        return f"{self.name}, {self.email}"


class Filter(models.Model):
    CATEGORY_CHOICES = (
        ('no', '----'),
        ('label', 'LABEL'),
        ('trash', 'TRASH'),
        ('archive', 'ARCHIVE')
    )
    sender = models.CharField(max_length=50, blank=True, null=True, help_text=('username@eml.com'))
    subject = models.CharField(max_length=500, blank=True, null=True)
    body = models.TextField(max_length=500, blank=True, null=True)
    file = models.BooleanField(default=False, blank=True, null=True)
    action = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='no')


class Email(models.Model):
    """ Email class and its fields """
    SIGNATURE_CHOICES = (
        ('add signature', 'Add Signature'),
        ('none', 'None')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    signature = models.ForeignKey(Signature, on_delete=models.PROTECT, related_name="signature",
                                  blank=True, null=True)
    # contacts = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True,
    #                              related_name="contacts")
    # receiver = models.ManyToManyField(User, related_name="receiver")
    receiver = models.CharField(max_length=50, blank=True, null=True, help_text=('username@eml.com'))
    # cc = models.ManyToManyField(User, related_name="cc", blank=True)
    cc = models.CharField(max_length=800, null=True, blank=True)
    # bcc = models.ManyToManyField(User, related_name="bcc", blank=True)
    bcc = models.CharField(max_length=800, null=True, blank=True)
    subject = models.CharField(max_length=100, blank=True, null=True)
    label = models.ManyToManyField(Label, blank=True, )
    filter = models.ManyToManyField(Filter, blank=True, )
    # body = models.TextField(blank=True, null=True)
    body = RichTextUploadingField(null=True, blank=True)
    file = models.FileField(upload_to='documents/%Y/%m/%d/', validators=[file_size], blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # زمان ارسال ایمیل
    is_draft = models.BooleanField(default=False, )
    is_read = models.BooleanField(default=False, )
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='remail', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False, blank=True, null=True)
    is_trash = models.BooleanField(default=False, blank=True, null=True)
    status = models.CharField(max_length=20, choices=SIGNATURE_CHOICES, default='none')

    # tags = TaggableManager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"From: {self.signature}, Sub: {self.subject}"

    @property
    #  در حالی که file_size به صورت متد تعریف شده، اما property کاری کرده که انگار داریم با یک attribute کار می‌کنیم.
    # و بدون نیاز به پرانتز بتونید متدهاتون رو صدا بزنید.
    def file_size(self):
        if self.file and hasattr(self.file, 'size'):
            return self.file.size

    # class Profile(models.Model):
    #     accounts = models.OneToOneField(User, on_delete=models.CASCADE)
    #     email_confirmed = models.BooleanField(default=False)

    # @receiver(post_save, sender=User)
    # def update_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(accounts=instance)
    #     instance.profile.save()
