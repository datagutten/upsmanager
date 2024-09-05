from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import web, metrics

app_name = 'upsinfo'
urlpatterns = [
    path('', web.ups_list, name='index'),
    path('events', web.events, name='events'),
    path('metrics', metrics.metrics, name='metrics'),
]
