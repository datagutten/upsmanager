import re

import snmp_compat


def table_index(base_oid, oid):
    """
    Get the row and col from an SNMP table entry oid
    """
    if oid.find('iso') == 0:
        oid = oid.replace('iso', '.1')

    oid_key = oid[len(base_oid):]
    matches = re.search(r'^\.(\d+)\.([\d.]+)', oid_key)
    col = int(matches.group(1))
    try:
        row = int(matches.group(2))
    except ValueError:
        row = matches.group(2)
    return row, col


def snmp_table_bulk(session: snmp_compat.SNMPCompat, oid: str, key_mappings: dict) -> dict:
    """
    Fetch an SNMP table as a dict
    :param oid: Base OID to walk
    :param key_mappings: OID as key, name as value
    :return: Dict with table values
    """

    data = {}
    for item in session.bulkwalk(oid):
        row, col = table_index(oid, item.oid)

        try:
            field_name = key_mappings[col]
        except KeyError:
            field_name = col

        if row not in data.keys():
            data[row] = {}

        data[row][field_name] = item.typed_value()

    return data
