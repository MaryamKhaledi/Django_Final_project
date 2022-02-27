from django.urls import path
from . import views

urlpatterns = [
    path('home/<int:pk>', views.home, name='home'),
    path('compose-email/', views.ComposeEmail.as_view(), name='ComposeEmail'),
    path('inbox/', views.Inbox.as_view(), name='Inbox'),
    path('sent/', views.SentEmail.as_view(), name='SentEmail'),
    # path('home/', views.home, name='home'),
]
