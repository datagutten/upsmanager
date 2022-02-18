from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'upsinfo'
urlpatterns = [
    path('', views.ups_list, name='index'),
    path('events', views.events, name='events'),
]
