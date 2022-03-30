import json
from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from .models import User
from mail_page.models import Email


def size_format(value):
    """
    Simple kb/mb/gb size:
    """
    # value = int(value)
    if value < 512000:
        value = value / 1024.0
        ext = 'kb'
    elif value < 4194304000:
        value = value / 1048576.0
        ext = 'mb'
    else:
        value = value / 1073741824.0
        ext = 'gb'
    # bite = (str(round(value, 2)))
    # return f'{bite}\{ext}'
    # return '%s %s' % (str(round(value, 5)), ext)
    return (round(value, 4), ext)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username", "email", "phone_number", "date_joined", "is_active", "is_staff", "send_emails", "received_emails",
        "used_storage")

    # readonly_fields = ("username", "send_emails", "received_emails", "used_storage")

    # fields = readonly_fields

    # list_filter = ("is_staff", "is_active",)
    # search_fields = ("username", "email", "phone")
    # fieldsets = (
    #     ('Info',
    #      {'fields': ("username", "password", "verification", "email", "phone", "list_login")}),
    #     ("Permission",
    #      {'fields': ("is_staff", "is_active")}),
    #     ('Other Information',
    #      {'fields': ("first_name", "last_name", "date_joined", "birth_date", "gender", 'country')}),
    #     ("Sent/Received Emails",
    #      {'fields': ("send_emails", "received_emails")}),
    # )

    def send_emails(self, obj):
        from django.db.models import Avg
        result = Email.objects.filter(user=obj).count()
        return result

    send_emails.short_description = "Send Emails"

    def received_emails(self, obj):
        from django.db.models import Avg
        result = Email.objects.filter(receiver=obj).count()
        return result

    received_emails.short_description = "Received Emails"

    def used_storage(self, obj):
        user_files = Email.objects.filter(user=obj).exclude(Q(file="") | Q(file__isnull=True))
        # user_files = Email.objects.filter(Q(user=obj) | Q(receiver=obj)).exclude(Q(file="") | Q(file__isnull=True))
        total = sum(int(objects.file_size) for objects in user_files if objects.file_size)
        total = f"{size_format(total)[0]}{size_format(total)[1]}"
        return total

    used_storage.short_description = "Used Storage"

    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per month
        emails_with_file = Email.objects.filter(file__isnull=False).exclude(file='')

        usernames = []
        for email in emails_with_file:
            usernames.append(User.objects.get(pk=email.user.id))
            # asel noskhe :
            # usernames.append(User.objects.filter(Q(username=email.user.username) | Q(username=email.receiver)))
        usernames = set(usernames)
        usernames = list(usernames)

        file_data = []
        for user in usernames:
            files_of_user = emails_with_file.filter(user=user.id)
            # files_of_user = emails_with_file.filter(Q(user=user.id) | Q(receiver=user.username)) # asel noskhe
            # files_of_user = emails_with_file.filter(Q(user=user) | Q(receiver=user.username))
            total = sum(int(objects.file_size) for objects in files_of_user)
            total = size_format(total)[0]
            file_data.append({"user": user.username, "user_size": total})
        # return file_data

        as_json = json.dumps(file_data, cls=DjangoJSONEncoder)
        extra_context = extra_context or {"file_data": as_json}
        return super().changelist_view(request, extra_context=extra_context)

    used_storage.short_description = "changelist_view"
