from django.urls import path
from . import views

app_name = 'mail_page'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('compose/', views.ComposeEmail.as_view(), name='compose'),
    path('inbox/<int:pk>', views.Inbox.as_view(), name='Inbox'),
    path('sent/', views.SentEmail.as_view(), name='SentEmail'),
    # path('home/', views.home, name='home'),
]
