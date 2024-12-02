from abc import ABC

import snmp_compat.compat
from snmp_compat import snmp_exceptions

from ups import BaseUPS, exceptions


class SnmpUps(BaseUPS, ABC):
    def __init__(self, ip, community='public', version=0):
        snmp = snmp_compat.compat.select('ezsnmp')
        self.session = snmp(ip, community, version=version, timeout=0.1)

    def close(self):
        self.session.close()

    def get(self, oid):
        try:
            response = self.session.get(oid)
            return response.typed_value()
        except snmp_exceptions.SNMPTimeout as e:
            raise exceptions.UPSTimeout(e)
        except snmp_exceptions.SNMPError as e:
            raise exceptions.UPSError(e)
