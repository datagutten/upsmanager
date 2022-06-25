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

    def runtime(self):
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
