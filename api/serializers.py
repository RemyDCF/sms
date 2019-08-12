from rest_framework import serializers
from main.models import Contact, Message


class ContactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contact


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
