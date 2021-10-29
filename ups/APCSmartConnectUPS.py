import datetime

from django.conf import settings
from requests import HTTPError

from . import APCSmartConnect, BaseUPS


class APCSmartConnectUPS(BaseUPS):
    def __init__(self, _, key):
        key = int(key)
        super().__init__(key)
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

    def name(self):
        return self.ups['name']

    def model(self):
        return self.ups['model']

    def status_string(self):
        modes = {
            'online': 'Online'
        }
        status_key = self.ups['status']['upsOperatingMode']
        if status_key in modes:
            return modes[status_key]
        else:
            return status_key

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

    def runtime(self):
        seconds = self.details['battery']['runtimeRemaining']
        total_minutes = int(seconds / 60)
        hours = total_minutes // 60
        minutes = total_minutes - (hours * 60)

        return datetime.time(hour=hours, minute=minutes)
