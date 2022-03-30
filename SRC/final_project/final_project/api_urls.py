from rest_framework import routers
from mail_page.api_views import ContactsViewSet, EmailViewSet


router = routers.DefaultRouter()
router.register('contacts/<int:id>', ContactsViewSet, basename='contacts')
router.register('contacts', ContactsViewSet, basename='contacts')
router.register('emails', EmailViewSet, basename='emails')
router.register('emails/<int:id>', EmailViewSet, basename='emails')
