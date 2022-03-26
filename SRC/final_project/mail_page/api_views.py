from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from .models import Contacts, Email
from .serializers import ContactsSerializer, EmailSerializer
from rest_framework.response import Response


# class ContactsViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     A simple ViewSet for viewing accounts.
#     """
#     queryset = Contacts.objects.all()
#     serializer_class = ContactsSerializer

class ContactsViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Contacts.objects.all()
        serializer = ContactsSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Contacts.objects.all()
        contact = queryset.filter(owner=pk)
        serializer = ContactsSerializer(contact, many=True)
        return Response(serializer.data)


# class EmailViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Email.objects.all()
#     serializer_class = EmailSerializer

class EmailViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Email.objects.all()
        serializer = EmailSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Email.objects.all()
        email = queryset.filter(user=pk)
        serializer = EmailSerializer(email, many=True)
        return Response(serializer.data)
