from abc import ABC

import snmp_compat.compat
from snmp_compat import snmp_exceptions

from ups import BaseUPS, exceptions, snmp_utils


class SnmpUps(BaseUPS, ABC):
    def __init__(self, ip, community='public'):
        snmp = snmp_compat.compat.select('ezsnmp')
        self.session = snmp(ip, community, timeout=0.1)
        # Try to get sysName to check connection
        self.name = self.session.get('1.3.6.1.2.1.1.5.0')

    def close(self):
        self.session.close()

    def get(self, oid):
        try:
            response = self.session.get(oid)
            return response.typed_value()
        except snmp_exceptions.SNMPTimeout as e:
            raise exceptions.UPSTimeout(e)
        except snmp_exceptions.SNMPNoData:
            return None
        except snmp_exceptions.SNMPError as e:
            raise exceptions.UPSError(e)

    def ups_output_table(self):
        return snmp_utils.snmp_table_bulk(self.session, '.1.3.6.1.2.1.33.1.4.4.1',
                                          {1: 'upsOutputLineIndex',
                                           2: 'upsOutputVoltage',
                                           3: 'upsOutputCurrent',
                                           4: 'upsOutputPower',
                                           5: 'upsOutputPercentLoad'})

    def ups_input_table(self):
        return snmp_utils.snmp_table_bulk(self.session, '.1.3.6.1.2.1.33.1.3.3.1',
                                          {1: 'upsInputLineIndex',
                                           2: 'upsInputFrequency',
                                           3: 'upsInputVoltage',
                                           4: 'upsInputCurrent',
                                           5: 'upsInputTruePower'})
