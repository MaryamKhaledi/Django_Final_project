from rest_framework import serializers
from .models import *


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ["name", "email"]
        # extra_kwargs = {"email": {'write_only': True}}


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ["user", "receiver"]
