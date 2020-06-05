try:
    from ups.apc import ApcUps
except ImportError:
    from .ups.apc import ApcUps


def select(vendor):
    if vendor == 'APC':
        return ApcUps
    else:
        raise AttributeError('Unsupported vendor: ' + vendor)
