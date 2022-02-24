from django.core.exceptions import ValidationError
from django.db import models
from accounts.models import User


def file_size(value):  # add this to some file where you can import it from
    limit = 26214400  # 20971520+5342880
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 25 MiB.')


class Label(models.Model):
    title = models.CharField(
        max_length=200, blank=True, null=True
    )


class Signature(models.Model):
    username = models.CharField(max_length=60, )
    send = models.BooleanField()


class Contacts(models.Model):
    name = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    phon_number = models.CharField(max_length=15)
    birth_date = models.DateTimeField(null=True, )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts_owner")


class Email(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="emails")
    signature = models.ForeignKey(User, on_delete=models.PROTECT, related_name="emails_sent")
    contacts = models.ManyToManyField(Contacts, related_name="emails_contacts")
    receiver = models.ManyToManyField(User, related_name="emails_received")
    subject = models.CharField(max_length=100, blank=True, null=True)
    label = models.ManyToManyField(Label, blank=True, )
    body = models.TextField(blank=True, null=True)
    file = models.FileField(validators=[file_size], blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, )  # زمان ارسال ایمیل
    read = models.BooleanField(default=False, )  # فیلد read هم مربوط به این هستش آیا اون ایمیل خونده شده یا نه؟
    archived = models.BooleanField(default=False, )

    # فیلد archived هم مربوط به این هستش که آیا کاربر اون ایمیل رو آرشیو کرده یا نه.

    def serialize(self):
        # تابع serialize هم برای برای اینه که تمام فیلد های اون دیتابیس رو بصورت مرتب شده به ما برگردونه
        return {
            "id": self.id,
            "sender": self.sender.email,
            "recipients": [user.email for user in self.contacts.all()],
            "subject": self.subject,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "read": self.read,
            "archived": self.archived
        }

    def __str__(self):
        return f"From: {self.sender}, Sub: {self.subject}"

# class Profile(models.Model):
#     accounts = models.OneToOneField(User, on_delete=models.CASCADE)
#     email_confirmed = models.BooleanField(default=False)


# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(accounts=instance)
#     instance.profile.save()
