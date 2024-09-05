from abc import ABC
from datetime import time


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

    def runtime(self) -> time:
        """
        Get UPS runtime
        @return: Runtime as time object
        """
        raise NotImplementedError

    def runtime_seconds(self):
        if hasattr(self, 'runtime_minutes'):
            return int(self.runtime_minutes()*60)
        else:
            raise NotImplementedError

    def runtime_minutes(self):
        if hasattr(self, 'runtime_seconds'):
            return int(self.runtime_seconds()/60)
        else:
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
