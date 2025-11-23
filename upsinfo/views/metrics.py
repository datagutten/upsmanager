import prometheus_client
from django.http import HttpResponse

from upsinfo import models

labels = {'ups_name': 'UPS Name', 'ups_ip': 'UPS IP'}
labels_phase = labels.copy()
labels_phase['phase'] = 'Phase'


class UPSMetrics:
    def __init__(self):
        # General
        self.battery_temperature = prometheus_client.Gauge('ups_battery_temperature',
                                                           'Battery temperature in centigrade',
                                                           labels)
        self.battery = prometheus_client.Gauge('ups_battery', 'UPS battery percentage', labels)
        self.battery_voltage = prometheus_client.Gauge('ups_battery_voltage', 'Battery voltage', labels)
        self.time_on_battery = prometheus_client.Gauge('ups_on_battery',
                                                       'The elapsed time in seconds since the UPS has switched to battery power',
                                                       labels)
        self.runtime = prometheus_client.Gauge('ups_runtime', 'UPS runtime in seconds', labels)
        self.status_string = prometheus_client.Info('ups_status_string', 'UPS status string', labels)

        # Input
        self.input_frequency = prometheus_client.Gauge('ups_input_frequency', 'UPS input frequency', labels_phase)
        self.input_voltage = prometheus_client.Gauge('ups_input_voltage', 'UPS input voltage', labels_phase)
        self.input_current = prometheus_client.Gauge('ups_input_current', 'UPS input current', labels_phase)
        self.input_power = prometheus_client.Gauge('ups_input_power', 'UPS input true power', labels_phase)

        # Output
        self.output_voltage = prometheus_client.Gauge('ups_output_voltage', 'UPS output voltage', labels_phase)
        self.output_current = prometheus_client.Gauge('ups_output_current', 'UPS output current', labels_phase)
        self.output_power = prometheus_client.Gauge('ups_output_power', 'UPS output true power', labels_phase)
        self.output_load = prometheus_client.Gauge('ups_load', 'UPS load percentage', labels_phase)

    def metrics(self, request):
        for ups_obj in models.Ups.objects.filter(enabled=True):
            ups_labels = [ups_obj.name, ups_obj.ip]
            try:
                ups_snmp = ups_obj.snmp()
            except Exception as e:
                self.status_string.labels(*ups_labels).info({'status': str(e)})
                continue

            self.battery_temperature.labels(*ups_labels).set(ups_snmp.battery_temperature())
            self.battery.labels(*ups_labels).set(ups_snmp.battery())
            self.battery_voltage.labels(*ups_labels).set(ups_snmp.battery_voltage())

            self.time_on_battery.labels(*ups_labels).set(ups_snmp.time_on_battery().total_seconds())
            self.runtime.labels(*ups_labels).set(ups_snmp.runtime().total_seconds())
            self.status_string.labels(*ups_labels).info({'status': ups_snmp.status_string()})

            try:
                strings = ups_snmp.status_messages()
                if not ups_obj.last_event() or ups_obj.last_event().event not in strings:
                    for string in strings:
                        event = models.Event(ups=ups_obj, event=string)
                        event.save()
            except ValueError:
                pass

            input_table = ups_snmp.ups_input_table()
            for phase, data in input_table.items():
                ups_labels = [ups_obj.name, ups_obj.ip, phase]
                try:
                    self.input_frequency.labels(*ups_labels).set(data['upsInputFrequency'] / 10)
                    self.input_voltage.labels(*ups_labels).set(data['upsInputVoltage'])
                    self.input_current.labels(*ups_labels).set(data['upsInputCurrent'])
                    self.input_power.labels(*ups_labels).set(data['upsInputTruePower'])
                except RuntimeError as e:
                    pass

            output_table = ups_snmp.ups_output_table()
            for phase, data in output_table.items():
                ups_labels = [ups_obj.name, ups_obj.ip, phase]
                try:
                    self.output_voltage.labels(*ups_labels).set(data['upsOutputVoltage'])
                    self.output_current.labels(*ups_labels).set(data['upsOutputCurrent'])
                    self.output_power.labels(*ups_labels).set(data['upsOutputPower'])
                    self.output_load.labels(*ups_labels).set(data['upsOutputPercentLoad'])

                except RuntimeError as e:
                    pass

        output = prometheus_client.generate_latest()
        return HttpResponse(output, content_type='text/plain', charset='utf-8')
