from abc import ABC


class UPS(ABC):
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
