from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('login/', views.login, name='login'),
    # path('register/', views.register, name='register'),
    # path('logout/', views.logout, name='logout'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name='activate'),
    path('logout/', views.logout, name='logout'),
]
