import ups

vendors = {
    'Generic': ups.RfcUps,
    'APC': ups.ApcUps,
    'Eaton': ups.Eaton,
    'APCSmartConnect': ups.APCSmartConnectUPS,
    'EPPC': ups.PowerWalkerEPPC,
    'NextUPSSystems': ups.NextUPSSystems,
}


def select(vendor):
    if vendor in vendors:
        return vendors[vendor]
    else:
        raise AttributeError('Unsupported vendor: ' + vendor)
