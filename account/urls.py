from django.conf.urls import url
from django.urls import path, include
from .api import RegisterApi
urlpatterns = [
      path('register', RegisterApi.as_view(), name='account-register'),
]
