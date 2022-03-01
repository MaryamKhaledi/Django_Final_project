from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models
from accounts.models import User


def file_size(value):  # add this to some file where you can import it from
    limit = 26214400  # 20971520+5342880
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 25 MiB.')


class Label(models.Model):
    title = models.CharField(
        max_length=30, blank=True, null=True
    )

    def __str__(self):
        return self.title


class Signature(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, max_length=60)
    is_send = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.is_send


class Contacts(models.Model):
    name = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    phon_number = models.CharField(max_length=11, blank=True, null=True)
    birth_date = models.DateTimeField(null=True, )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts_owner")

    def __str__(self):
        return self.name, self.email


class Email(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    signature = models.ForeignKey(Signature, on_delete=models.PROTECT, related_name="signature",
                                  blank=True, null=True)
    # contacts = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True,
    #                              related_name="contacts")
    receiver = models.ManyToManyField(User, related_name="receiver")
    cc = models.ManyToManyField(User, related_name="cc", blank=True)
    bcc = models.ManyToManyField(User, related_name="bcc", blank=True)
    subject = models.CharField(max_length=100, blank=True, null=True)
    label = models.ManyToManyField(Label, blank=True, )
    body = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='', validators=[file_size], blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # زمان ارسال ایمیل
    is_read = models.BooleanField(default=False, )  # فیلد read هم مربوط به این هستش آیا اون ایمیل خونده شده یا نه؟
    # replay = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)
    is_archived = models.BooleanField(default=False, blank=True, null=True)
    is_trash = models.BooleanField(default=False, blank=True, null=True)

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
