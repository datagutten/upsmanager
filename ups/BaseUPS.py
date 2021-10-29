from abc import ABC


class BaseUPS(ABC):
    def manufacturer(self) -> str:
        pass

    def name(self) -> str:
        """
        Get UPS host name
        @return: UPS host name
        """
        pass

    def model(self):
        pass

    def runtime(self):
        pass
