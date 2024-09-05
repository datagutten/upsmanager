import prometheus_client
from django.http import HttpResponse

from upsinfo import models

labels = {'ups_name': 'UPS Name', 'ups_ip': 'UPS IP'}
load = prometheus_client.Gauge('ups_load', 'UPS load percentage', labels)
battery_temperature = prometheus_client.Gauge('ups_battery_temperature', 'Battery temperature in centigrade',
                                              labels)
battery = prometheus_client.Gauge('ups_battery', 'UPS battery percentage', labels)
battery_voltage = prometheus_client.Gauge('ups_battery_voltage', 'Battery voltage', labels)
input_voltage = prometheus_client.Gauge('ups_input_voltage', 'UPS input voltage', labels)
runtime = prometheus_client.Gauge('ups_runtime', 'UPS runtime in seconds', labels)
status_string = prometheus_client.Info('ups_status_string', 'UPS status string', labels)


def metrics(request):
    for ups_obj in models.Ups.objects.filter(enabled=True):
        ups_labels = [ups_obj.name, ups_obj.ip]
        try:
            ups_snmp = ups_obj.snmp()

            load.labels(*ups_labels).set(ups_snmp.load())
            battery_temperature.labels(*ups_labels).set(ups_snmp.battery_temperature())
            battery.labels(*ups_labels).set(ups_snmp.battery())
            battery_voltage.labels(*ups_labels).set(ups_snmp.battery_voltage())
            input_voltage.labels(*ups_labels).set(ups_snmp.input_voltage())
            runtime.labels(*ups_labels).set(ups_snmp.runtime_seconds())
            status_string.labels(*ups_labels).info({'status': ups_snmp.status_string()})
        except Exception as e:
            status_string.labels(*ups_labels).info({'status': str(e)})
            continue
    output = prometheus_client.generate_latest()
    return HttpResponse(output, content_type='text/plain', charset='utf-8')
