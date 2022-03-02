from django.urls import path
from . import views

app_name = 'mail_page'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('compose/', views.ComposeEmail.as_view(), name='compose'),
    path('inbox/', views.Inbox.as_view(), name='inbox'),
    path('detail/<int:id>', views.DetailEmail.as_view(), name='detail'),
    path('sent/', views.SentEmail.as_view(), name='sent'),
    # path('reply/<int:id>', views.ReplyEmail.as_view(), name='reply'),
    path('reply/<str:email_user>', views.reply_email, name='reply'),
]
