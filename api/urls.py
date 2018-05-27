from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from api.views import *

urlpatterns = [
    url(r'^api_influx/', influx_rest, name='influx_rest'),
    url(r'^email_notif/', email_notif, name='email_notif'),
]