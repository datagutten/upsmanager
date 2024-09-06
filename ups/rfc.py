import datetime
from typing import Optional

from . import SnmpUps


class RfcUps(SnmpUps):
    good_state = 'Normal'

    def manufacturer(self) -> str:
        """
        UPS-MIB::upsIdentManufacturer.0
        @return: UPS manufacturer
        """
        return self.get('1.3.6.1.2.1.33.1.1.1.0')

    def model(self) -> str:
        """
        UPS-MIB::upsIdentModel.0
        @return: UPS model
        """
        return self.get('1.3.6.1.2.1.33.1.1.2.0')

    def ups_software_version(self) -> str:
        """
        UPS-MIB::upsIdentUPSSoftwareVersion.0
        @return: UPS software version
        """
        return self.get('1.3.6.1.2.1.33.1.1.3.0')

    def agent_software_version(self) -> str:
        """
        UPS-MIB::upsIdentAgentSoftwareVersion.0
        @return: Agent software version
        """
        return self.get('1.3.6.1.2.1.33.1.1.4.0')

    def name(self) -> str:
        """
        UPS-MIB::upsIdentName.0
        @return: UPS name
        """
        return self.get('.1.3.6.1.2.1.33.1.1.5.0')

    def battery_status(self) -> str:
        """
        UPS-MIB::upsBatteryStatus.0
        @return: UPS battery status name
        """
        value = self.get('.1.3.6.1.2.1.33.1.2.1.0')
        values = {1: 'Unknown', 2: 'Normal', 3: 'Low battery'}
        if value not in values:
            return value
        return values[value]

    def runtime(self) -> datetime.timedelta:
        total_minutes = self.get('.1.3.6.1.2.1.33.1.2.3.0')  # UPS-MIB::upsEstimatedMinutesRemaining.0
        if total_minutes is None or total_minutes < 0:
            total_minutes = 0

        return datetime.timedelta(minutes=total_minutes)

    def time_on_battery(self) -> datetime.timedelta:
        """
        The elapsed time since the UPS has switched to battery power.
        """
        seconds = self.get('.1.3.6.1.4.1.318.1.1.1.2.1.2.0')  # upsSecondsOnBattery
        return datetime.timedelta(seconds=seconds or 0)

    def battery(self) -> int:
        """
        UPS-MIB::upsEstimatedChargeRemaining
        @return: Battery percentage
        """
        return self.get('1.3.6.1.2.1.33.1.2.4.0')

    def battery_voltage(self) -> float:
        """
        UPS-MIB::upsBatteryVoltage.0
        @return: Battery voltage (V)
        """
        voltage = self.get('.1.3.6.1.2.1.33.1.2.5.0')
        if voltage:
            return voltage / 10

    def battery_current(self) -> float:
        """
        UPS-MIB::upsBatteryCurrent.0
        @return: Battery current
        """
        current = self.get('1.3.6.1.2.1.33.1.2.6.0')
        if current:
            return current / 10

    def battery_temperature(self) -> int:
        """
        UPS-MIB::upsBatteryTemperature.0
        @return: Battery temperature in centigrade
        """
        return self.get('1.3.6.1.2.1.33.1.2.7.0')

    def input_num_lines(self) -> int:
        """
        UPS-MIB::upsInputNumLines.0
        @return: Number of phases
        """
        return self.get('1.3.6.1.2.1.33.1.3.2.0')

    def input_frequency(self, phase=0) -> float:
        """
        UPS-MIB::upsInputFrequency.0
        @param phase: Phase number, 0 for single phase UPS
        @return: Input frequency
        """
        frequency = self.get('1.3.6.1.2.1.33.1.3.3.1.2.%d' % phase)
        if frequency:
            return frequency / 10

    def input_voltage(self, phase=0) -> float:
        """
        UPS-MIB::upsInputVoltage.0
        @param phase: Phase number, 0 for single phase UPS
        @return: Input voltage (V)
        """
        return self.get('.1.3.6.1.2.1.33.1.3.3.1.3.%d' % phase)

    def input_current(self, phase=0) -> float:
        """
        UPS-MIB::upsInputCurrent.0
        @param phase: Phase number, 0 for single phase UPS
        @return: Input current (A)
        """
        current = self.get('1.3.6.1.2.1.33.1.3.3.1.4.%d' % phase)
        if current:
            return current / 10

    def input_true_power(self, phase=0) -> int:
        """
        UPS-MIB::upsInputTruePower.0
        @param phase: Phase number, 0 for single phase UPS
        @return: Input true power (W)
        """
        return self.get('1.3.6.1.2.1.33.1.3.3.1.5.%d' % phase)

    def output_source(self):
        """
        UPS-MIB::upsOutputSource.0
        @return: Output source name
        """
        values = {
            1: 'None',
            2: 'Other',
            3: 'Normal',
            4: 'Bypass',
            5: 'Battery',
            6: 'Booster',
            7: 'Reducer',
        }

        status = self.get('.1.3.6.1.2.1.33.1.4.1.0')
        if status not in values:
            return status
        elif status:
            return values[status]

    def output_frequency(self) -> float:
        """
        UPS-MIB::upsOutputFrequency.0
        @return: Output frequency (Hz)
        """
        frequency = self.get('1.3.6.1.2.1.33.1.4.2.0')
        if frequency:
            return frequency / 10

    def output_num_lines(self) -> int:
        """
        UPS-MIB::upsOutputNumLines.0
        @return: Number of phases
        """
        return self.get('1.3.6.1.2.1.33.1.4.3.0')

    def output_current(self) -> float:
        try:
            return self.get('.1.3.6.1.2.1.33.1.4.4.1.3.1') / 10
        except TypeError:
            return 0.0

    def load(self, phase=0) -> int:
        """
        UPS-MIB::upsOutputPercentLoad.0
        @param phase: Phase number, 0 for single phase UPS
        @return: Load percentage
        """
        return self.get('.1.3.6.1.2.1.33.1.4.4.1.5.%d' % phase)

    def status_messages(self) -> list:
        return [self.battery_status()]
