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
