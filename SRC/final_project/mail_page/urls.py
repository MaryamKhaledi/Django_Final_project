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
    path('showcontacts/', views.ShowContacts.as_view(), name='showcontacts'),
    path('newcontacts/', views.NewContacts.as_view(), name='newcontacts'),
    path('detailcontacts/<int:id>', views.DetailContacts.as_view(), name='detailcontacts'),
    path('deletecontacts/<int:id>', views.DeleteContacts.as_view(), name='deletecontacts'),
    path('updatecontacts/<int:id>', views.UpdateContacts.as_view(), name='updatecontacts'),
    path('newlabel/', views.NewLabel.as_view(), name='newlabel'),
    path('showlabel/', views.ShowLabel.as_view(), name='showlabel'),
    # path('showlabel/', views.LabelsEmail.as_view(), name='labelsemail'),
]
