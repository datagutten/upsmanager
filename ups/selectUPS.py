from . import Eaton, RfcUps, ApcUps


def select(vendor):
    if vendor == 'APC':
        return ApcUps
    elif vendor == 'Eaton':
        return Eaton
    elif vendor == 'Generic':
        return RfcUps
    else:
        raise AttributeError('Unsupported vendor: ' + vendor)
