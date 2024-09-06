import datetime
from timedelta import Timedelta
import re
from abc import ABC

import netsnmp

from ups import BaseUPS, exceptions


class SnmpUps(BaseUPS, ABC):
    session: netsnmp.SNMPSession

    def __init__(self, ip, community='public', version=0):
        self.session = netsnmp.SNMPSession(ip, community, version=version, timeout=0.1)

    def get(self, oid):
        # noinspection PyProtectedMember
        try:
            data = self.session.get(oid)
        except netsnmp._api.SNMPError as e:
            if str(e).strip() == 'Timeout':
                raise exceptions.UPSTimeout(e)
            else:
                raise exceptions.UPSError(e)
        except Exception as e:
            raise exceptions.UPSError(e)

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
            return datetime.timedelta(hours=int(matches[2]), minutes=int(matches[3]),
                                      seconds=int(matches[4]))
        return None
