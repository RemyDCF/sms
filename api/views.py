import logging

import phonenumbers
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from twilio.rest import Client
from django.contrib.auth.models import User
from webpush import send_user_notification

from main.models import *

import requests

twilio_client = Client(settings.TWILIO_ACCOUNT_SIDS, settings.TWILIO_AUTH_TOKEN)


def sendPush(title, body):
    payload = {"head": title, "body": body, "url": "https://sms.remydcf.dev/"}
    users = User.objects.all()
    for user in users:
        send_user_notification(user=user, payload=payload, ttl=1000)


class Contacts(APIView):
    def get(self, request, format=None):
        if not request.user.is_authenticated:
            return Response("Not authenticated", status=status.HTTP_403_FORBIDDEN)

        a = []
        for contact in Contact.objects.all():
            a.append(
                {
                    "id": contact.id,
                    "name": contact.name,
                    "phone_number": contact.phone_number,
                    "phone_number_formatted": phonenumbers.format_number(
                        phonenumbers.parse(contact.phone_number, None),
                        phonenumbers.PhoneNumberFormat.INTERNATIONAL,
                    ),
                    "image_url": f"https://www.tinygraphs.com/isogrids/{contact.phone_number}?theme=duskfalling&numcolors=4&size=220&fmt=svg",
                    "flag_url": f"https://www.countryflags.io/{phonenumbers.region_code_for_country_code(phonenumbers.parse(contact.phone_number, None).country_code).lower()}/flat/24.png",
                    "messages": [
                        {
                            "text": x.text,
                            "contact_is_sender": x.contact_is_sender,
                            "timestamp": x.timestamp,
                        }
                        for x in contact.message_set.order_by("-timestamp").all()
                    ],
                }
            )
        return JsonResponse(a, safe=False)

    def post(self, request, format=None):
        if not request.user.is_authenticated:
            return Response("Not authenticated", status=status.HTTP_403_FORBIDDEN)

        contact = Contact(
            name=request.POST.get("name", None),
            phone_number=request.POST.get("phone-number", None),
        )
        contact.save()
        return Response("Created.", status=status.HTTP_201_CREATED)


class Messages(APIView):
    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        body = request.POST.get("Body", None)
        from_contact = request.POST.get("From", None)
        contact = None
        try:
            contact = Contact.objects.filter(phone_number=from_contact).all()[0]
        except:
            contact = Contact(name=from_contact, phone_number=from_contact)
            contact.save()

        message = Message(text=body, contact=contact, contact_is_sender=True)
        message.save()
        sendPush(contact.name, body)
        return Response("", status=status.HTTP_201_CREATED)


class SendMessages(APIView):
    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        if not request.user.is_authenticated:
            return Response("Not authenticated", status=status.HTTP_403_FORBIDDEN)

        message = request.POST.get("message", None)
        contact_id = request.POST.get("contact_id", None)

        contact = None
        try:
            contact = Contact.objects.filter(id=contact_id).all()[0]
        except:
            return Response("Failed.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        message_twilio = twilio_client.messages.create(
            body=message, from_=settings.TWILIO_PHONE_NUMBER, to=contact.phone_number
        )
        message = Message(text=message, contact=contact, contact_is_sender=False)
        message.save()
        return Response("Created.", status=status.HTTP_201_CREATED)


class Balance(APIView):
    def get(self, request, format=None):
        if not request.user.is_authenticated:
            return Response("Not authenticated", status=status.HTTP_403_FORBIDDEN)

        balance = requests.get(
            f"https://api.twilio.com/2010-04-01/Accounts/{settings.TWILIO_ACCOUNT_SIDS}/Balance.json",
            auth=(settings.TWILIO_ACCOUNT_SIDS, settings.TWILIO_AUTH_TOKEN),
        ).json()["balance"]
        return Response(balance)
