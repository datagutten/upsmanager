import datetime
from abc import ABC


class BaseUPS(ABC):
    def manufacturer(self) -> str:
        raise NotImplementedError

    def name(self) -> str:
        """
        Get UPS host name
        @return: UPS host name
        """
        raise NotImplementedError

    def model(self) -> str:
        """
        @return: UPS model name
        """
        raise NotImplementedError

    def runtime(self) -> datetime.timedelta:
        """
        Get UPS runtime
        @return: Runtime as timedelta object
        """
        raise NotImplementedError

    def runtime_minutes(self) -> int:
        """
        Runtime as total minutes
        """
        return int(self.runtime().total_seconds() // 60)

    def runtime_string(self) -> str:
        """
        Format UPS run time as hour:minute string
        """
        runtime = self.runtime()
        if runtime is None:
            return ''
        return '%02d:%02d' % (runtime.seconds // 3600, (runtime.seconds // 60) % 60)

    def time_on_battery(self) -> datetime.timedelta:
        """
        The elapsed time since the UPS has switched to battery power.
        """
        raise NotImplementedError

    def load(self) -> int:
        """
        UPS load
        @return: UPS load in %
        """
        raise NotImplementedError

    def battery_temperature(self) -> int:
        """
        @return: Battery temperature in centigrade
        """
        raise NotImplementedError

    def battery(self) -> int:
        """
        Get battery charge level
        @return: Battery charge level in %
        """
        raise NotImplementedError

    def battery_voltage(self) -> float:
        """
        Get battery voltage
        @return: Battery voltage
        """
        raise NotImplementedError

    def status_messages(self) -> list:
        """
        Get a list of status messages
        @return: List of status messages
        """
        raise NotImplementedError

    def status_string(self, separator='\n') -> str:
        """
        Get status messages joined to a string
        @return: Joined status messages
        """
        return separator.join(self.status_messages())

    def input_voltage(self) -> int:
        """
        Get input voltage
        @return: Input voltage
        """
        raise NotImplementedError

    def output_current(self) -> float:
        """
        The current in amperes drawn by the load on the UPS.
        """
        raise NotImplementedError
