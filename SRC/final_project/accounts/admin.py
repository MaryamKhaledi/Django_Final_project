from django.contrib import admin
from .models import User
from mail_page.models import Email


# admin.site.register(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "send_emails", "received_emails")

    readonly_fields = ("username", "send_emails", "received_emails")

    # fields = readonly_fields

    # list_filter = ("username",)

    def send_emails(self, obj):
        from django.db.models import Avg
        result = Email.objects.filter(user=obj).count()
        return result

    def received_emails(self, obj):
        from django.db.models import Avg
        result = Email.objects.filter(receiver=obj).count()
        return result
