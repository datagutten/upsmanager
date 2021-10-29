from . import RfcUps


class Eaton(RfcUps):
    def model(self):
        return 'Eaton %s' % super().model()

    def battery(self):
        return self.get('.1.3.6.1.4.1.534.1.2.4.0')

    def battery_temperature(self):
        return self.get('.1.3.6.1.4.1.534.1.6.1')
