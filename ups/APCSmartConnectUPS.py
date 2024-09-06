import datetime

from apc_smartconnect import APCSmartConnect
from django.conf import settings
from requests import HTTPError

from ups import BaseUPS, exceptions


class APCSmartConnectUPS(BaseUPS):
    def __init__(self, _, key):
        key = int(key)
        super().__init__()
        self.apc = APCSmartConnect()
        try:
            self._get_info(key)
        except HTTPError as e:
            if e.response.status_code == 401:
                self.apc.login(settings.SMARTCONNECT_USERNAME, settings.SMARTCONNECT_PASSWORD)
                self._get_info(key)
            else:
                raise e

    def _get_info(self, key):
        self.ups = self.apc.gateway_info(key)
        self.details = self.apc.gateway_info_detail(key)

    def manufacturer(self) -> str:
        return 'APC'

    def name(self):
        return self.ups['name']

    def model(self):
        return self.ups['model']

    def status_messages(self):
        modes = {
            'online': 'Online'
        }
        status_key = self.ups['status']['upsOperatingMode']
        if status_key in modes:
            return [modes[status_key]]
        else:
            return [status_key]

    def load(self):
        return self.details['output']['loadRealPercentage']

    def battery(self):
        return self.details['battery']['chargeStatePercentage']

    def battery_voltage(self):
        return self.details['battery']['voltage']

    def input_voltage(self):
        return self.details['input']['voltage']

    def battery_temperature(self):
        return self.details['battery']['temperature']

    def runtime(self) -> datetime.timedelta:
        seconds = self.details['battery']['runtimeRemaining']
        return datetime.timedelta(seconds=seconds)
