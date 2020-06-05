try:
    from ups import UpsInfo
except ImportError:
    from ups.ups import UpsInfo
import re


class RfcUps(UpsInfo):
    # def status(self):
    #    return self.get()

    def battery_voltage(self):
        voltage = self.get('.1.3.6.1.2.1.33.1.2.5.0')
        print('Voltage', voltage)
        return int(voltage)/10
