import datetime
import re

import netsnmp

from . import BaseUPS


class SnmpUps(BaseUPS):
    def __init__(self, ip, community='public', version=0):
        self.session = netsnmp.SNMPSession(ip, community, version=version, timeout=0.1)

    def get(self, oid):
        try:
            data = self.session.get(oid)
        except netsnmp._api.SNMPError as e:
            raise ValueError(e)

        data_type = data[0][1]
        value = data[0][2]
        if data_type == 'STRING':
            return value[1:-1]
        elif data_type == 'Gauge32':
            return int(value)
        elif data_type == 'INTEGER':
            return int(value)
        elif data_type == 'Timeticks':
            matches = re.match(r'([0-9]+):([0-9]+):([0-9]+):([0-9]+)\.([0-9]+)', value)
            return datetime.time(hour=int(matches[2]), minute=int(matches[3]),
                                 second=int(matches[4]))
        return None
