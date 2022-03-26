from rest_framework import serializers
from .models import *


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ["name", "email"]
        extra_kwargs = {"email": {'write_only': True}}


# class ContactsSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=200)
#     email = serializers.EmailField()
#     user = serializers.CharField(max_length=200)
#     receiver = serializers.CharField(max_length=200)


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ["user", "receiver"]

# class EmailSerializer(serializers.ModelSerializer):
# user = serializers.CharField(max_length=200)
#     receiver = serializers.CharField(max_length=200)
