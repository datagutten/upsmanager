from .exceptions import UnsupportedUPSVendor

vendors = {}
try:  # SNMP UPS classes
    from .rfc import RfcUps
    from .Eaton import Eaton
    from .apc import ApcUps
    from .EPPC import PowerWalkerEPPC
    from .NextUPSSystems import NextUPSSystems

    vendors = {
        'Generic': RfcUps,
        'APC': ApcUps,
        'Eaton': Eaton,
        'EPPC': PowerWalkerEPPC,
        'NextUPSSystems': NextUPSSystems,
    }

except ImportError as e:
    # print('Error importing SNMP: %s' % e)
    pass

try:
    from .APCSmartConnectUPS import APCSmartConnectUPS

    vendors['APCSmartConnect'] = APCSmartConnectUPS
except ImportError:
    # print('Error importing APC SmartConnect')
    pass

try:
    from .NUTUps import NUTUps

    vendors['NUT'] = NUTUps
except ImportError:
    # print('Error importing NUT')
    pass


def select(vendor):
    if vendor in vendors:
        return vendors[vendor]
    else:
        raise UnsupportedUPSVendor('Unsupported vendor: ' + vendor)
