from django.contrib import admin

# Register your models here.
from main.models import Contact, Message

admin.site.register(Contact)
admin.site.register(Message)
