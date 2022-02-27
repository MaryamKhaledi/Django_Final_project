from django.urls import path
from . import views

urlpatterns = [
    path('home/<int:pk>', views.home, name='home'),
    # path('home/', views.home, name='home'),
]
