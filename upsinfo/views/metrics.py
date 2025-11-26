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

    def _phase_table(self, snmp_table: dict, fields: dict, ups_obj: models.Ups):
        for phase, data in snmp_table.items():
            ups_labels = [ups_obj.name, ups_obj.ip, phase]
            for metric_key, snmp_field in fields.items():
                if snmp_field not in data or data[snmp_field] is None:
                    continue
                metric = getattr(self, metric_key).labels(*ups_labels)
                if metric_key.find('frequency') > -1:
                    metric.set(data[snmp_field] / 10)
                else:
                    metric.set(data[snmp_field])

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
            fields_input = {'input_frequency': 'upsInputFrequency',
                            'input_voltage': 'upsInputVoltage',
                            'input_current': 'upsInputCurrent',
                            'input_power': 'upsInputTruePower', }
            self._phase_table(input_table, fields_input, ups_obj)

            fields_output = {'output_voltage': 'upsOutputVoltage',
                             'output_current': 'upsOutputCurrent',
                             'output_power': 'upsOutputPower',
                             'output_load': 'upsOutputPercentLoad', }

            output_table = ups_snmp.ups_output_table()
            self._phase_table(output_table, fields_output, ups_obj)

        output = prometheus_client.generate_latest()
        return HttpResponse(output, content_type='text/plain', charset='utf-8')
