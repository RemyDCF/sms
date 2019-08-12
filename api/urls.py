from api import views
from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [path("messages/", views.Messages.as_view())]

urlpatterns = format_suffix_patterns(urlpatterns)
