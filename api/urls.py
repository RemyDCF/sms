from api import views
from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path("messages/", views.Messages.as_view()),
    path("messages/send", views.SendMessages.as_view()),
    path("contacts", views.Contacts.as_view()),
    path("contacts/<int:id>", views.IndividualContact.as_view()),
    path("balance", views.Balance.as_view()),
    path("auth/", include("rest_framework.urls", namespace="rest_framework")),
]

urlpatterns = format_suffix_patterns(urlpatterns)
