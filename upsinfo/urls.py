from django.urls import path

from .views import web
from .views.metrics import UPSMetrics

app_name = 'upsinfo'

metrics_class = UPSMetrics()
urlpatterns = [
    path('', web.ups_list, name='index'),
    path('events', web.events, name='events'),
    path('metrics', metrics_class.metrics, name='metrics')
]

# path('ups_ajax', views.ajax.ups_row_ajax, name='ups_ajax'),
