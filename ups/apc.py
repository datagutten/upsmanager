from datetime import timedelta, time

from . import SnmpUps
import textwrap


class ApcUps(SnmpUps):
    good_state = 'On Line'

    def manufacturer(self) -> str:
        return 'APC'

    def name(self):
        return self.get('.1.3.6.1.4.1.318.1.1.1.1.1.2.0')

    def model(self):
        return self.get('.1.3.6.1.4.1.318.1.1.1.1.1.1.0')

    def battery(self):
        return self.get('.1.3.6.1.4.1.318.1.1.1.2.2.1.0')

    def runtime(self) -> time:
        """
        upsAdvBatteryRunTimeRemaining
        The UPS battery run time remaining before battery exhaustion.
        """
        return self.get('.1.3.6.1.4.1.318.1.1.1.2.2.3.0')

    def runtime_seconds(self):
        runtime = self.runtime()
        runtime_delta = timedelta(seconds=runtime.second, minutes=runtime.minute, hours=runtime.hour)
        return runtime_delta.total_seconds()

    def battery_status(self):
        value = self.get('.1.3.6.1.4.1.318.1.1.1.2.1.1.0')
        values = {'1': 'Unknown', '2': 'Normal', '3': 'Low battery'}
        return values[value]

    def battery_voltage(self):
        value = self.get('.1.3.6.1.4.1.318.1.1.1.2.3.4.0')
        if value and type(value) == int:
            return value/10

    def battery_sku(self):
        return self.get('.1.3.6.1.4.1.318.1.1.1.2.2.19.0')

    def status(self):
        # upsAdvStateAbnormalConditions
        return self.get('.1.3.6.1.4.1.318.1.1.1.11.1.1.0')

    @staticmethod
    def split_status(status):
        matches = textwrap.wrap(status, 1)
        return matches

    @staticmethod
    def parse_status(status: str) -> list:
        """
        Parse a status string to a list with readable status messages
        @param status: Status string with 0 and 1
        @return: List with status messages
        """
        values = {
            1: 'Abnormal Condition Present',
            2: 'On Battery',
            3: 'Low Battery',
            4: 'On Line',
            5: 'Replace Battery',
            # 6: 'Serial Communication Established',
            7: 'AVR Boost Active',
            8: 'AVR Trim Active',
            9: 'Overload',
            10: 'Runtime Calibration',
            11: 'Batteries Discharged',
            12: 'Manual Bypass',
            13: 'Software Bypass',
            14: 'In Bypass due to Internal Fault',
            15: 'In Bypass due to Supply Failure',
            16: 'In Bypass due to Fan Failure',
            17: 'Sleeping on a Timer',
            18: 'Sleeping until Utility Power Returns',
            # 19: 'On',
            20: 'Rebooting',
            21: 'Battery Communication Lost',
            22: 'Graceful Shutdown Initiated',
            23: 'Smart Boost or Smart Trim Fault',
            24: 'Bad Output Voltage',
            25: 'Battery Charger Failure',
            26: 'High Battery Temperature',
            27: 'Warning Battery Temperature',
            28: 'Critical Battery Temperature',
            29: 'Self Test In Progress',
            30: 'Low Battery / On Battery',
            31: 'Graceful Shutdown Issued by Upstream Device',
            32: 'Graceful Shutdown Issued by Downstream Device',
            33: 'No Batteries Attached',
            34: 'Synchronized Command is in Progress',
            35: 'Synchronized Sleeping Command is in Progress',
            36: 'Synchronized Rebooting Command is in Progress',
            37: 'Inverter DC Imbalance',
            38: 'Transfer Relay Failure',
            39: 'Shutdown or Unable to Transfer',
            40: 'Low Battery Shutdown',
            41: 'Electronic Unit Fan Failure',
            42: 'Main Relay Failure',
            43: 'Bypass Relay Failure',
            44: 'Temporary Bypass',
            45: 'High Internal Temperature',
            46: 'Battery Temperature Sensor Fault',
            47: 'Input Out of Range for Bypass',
            48: 'DC Bus Overvoltage',
            49: 'PFC Failure',
            50: 'Critical Hardware Fault',
            # 51: 'Green Mode/ECO Mode',
            52: 'Hot Standby',
            53: 'Emergency Power Off (EPO) Activated',
            54: 'Load Alarm Violation',
            55: 'Bypass Phase Fault',
            56: 'UPS Internal Communication Failure',
            57: 'Efficiency Booster Mode',
            58: 'Off',
            59: 'Standby',
            60: 'Minor or Environment Alarm',
            61: '<Not Used>',
            62: '<Not Used>',
            63: '<Not Used>',
            64: '<Not Used>'}

        matches = ApcUps.split_status(status)
        strings = []
        for key, value in values.items():
            if matches[key-1] == '1':
                strings.append(value)
        return strings

    def status_messages(self) -> list:
        return self.parse_status(self.status())

    def time_on_battery(self):
        return self.get('.1.3.6.1.4.1.318.1.1.1.2.1.2.0')

    def battery_temperature(self):
        temperature_string = self.get('.1.3.6.1.4.1.318.1.1.1.2.3.2.0')
        if temperature_string:
            return int(temperature_string)/10

    def input_voltage(self):
        return self.get('.1.3.6.1.4.1.318.1.1.1.3.2.1.0')

    def load(self):
        return self.get('.1.3.6.1.4.1.318.1.1.1.4.2.3.0')

    def on_battery(self):
        strings = self.status_messages()
        if "On Battery" in strings:
            return True
        else:
            return False

