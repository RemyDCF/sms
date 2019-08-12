from datetime import datetime, timedelta
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from main.models import *
from django.utils.translation import gettext as _
from django.contrib.auth.hashers import check_password


class Messages(APIView):
    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        body = request.POST.get("Body", None)
        from_contact = request.POST.get("From", None)
        contact = None
        try:
            contact = Contact.objects.filter(phone_number=from_contact).all[0]
        except:
            contact = Contact(name=from_contact, phone_number=from_contact)
            contact.save()

        message = Message(text=body, contact=contact, contact_is_sender=True)
        message.save()
        return Response("Message created", status=status.HTTP_201_CREATED)
