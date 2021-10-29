import datetime

from . import SnmpUps


class RfcUps(SnmpUps):
    # def status(self):
    #    return self.get()

    def name(self):
        return self.get('.1.3.6.1.2.1.33.1.1.5')

    def model(self):
        return self.get('.1.3.6.1.2.1.33.1.1.2')

    def battery_status(self):
        value = self.get('.1.3.6.1.2.1.33.1.2.1')
        values = {1: 'Unknown', 2: 'Normal', 3: 'Low battery'}
        if value not in values:
            return value
        return values[value]

    def output_source(self):
        values = {
            1: 'None',
            2: 'Other',
            3: 'Normal',
            4: 'Bypass',
            5: 'Battery',
            6: 'Booster',
            7: 'Reducer',
        }

        status = self.get('.1.3.6.1.2.1.33.1.4.1')
        if status:
            return values[status]

    def runtime(self):
        total_minutes = self.get('.1.3.6.1.2.1.33.1.2.3.0')
        hours = total_minutes // 60
        minutes = total_minutes - (hours * 60)

        return datetime.time(hour=hours, minute=minutes)

    def load(self, phase=1):
        return self.get('.1.3.6.1.2.1.33.1.4.4.1.5.%d' % phase)

    def status_string(self):
        return self.battery_status()

    def battery_temperature(self):
        return self.get('1.3.6.1.2.1.33.1.2.7')

    def battery_voltage(self):
        voltage = self.get('.1.3.6.1.2.1.33.1.2.5.0')
        return int(voltage) / 10

    def input_voltage(self, phase=1):
        return self.get('.1.3.6.1.2.1.33.1.3.3.1.3.%d' % phase)
