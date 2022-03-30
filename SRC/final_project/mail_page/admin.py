from django.contrib import admin
from .models import *
from django.http import HttpResponseRedirect
from django.contrib import messages

admin.site.register(Email)
admin.site.register(Contacts)
# admin.site.register(Label)
admin.site.register(Signature)


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    fields = ('title',)
    list_display = ['owner', 'title']

    def add_view(self, request):
        if request.method == 'POST':
            try:
                users = User.objects.all()
                for user in users:
                    Label.objects.create(owner=user, title=request.POST.get('title'))
                return HttpResponseRedirect('/admin/mail_page/label/')
            except Exception as e:
                messages.error(request, 'this label exist', extra_tags="error")
                return HttpResponseRedirect('/admin/mail_page/label/add/')
        return super(LabelAdmin, self).add_view(request)
