from unittest import TestCase

from ups.apc import ApcUps
from pprint import pprint


class StatusTestCase(TestCase):
    def test_parse_status(self):
        status = '0100010001000000001000000000000000000000000000000000000000000000'
        parsed = ApcUps.parse_status(status)
        ref = ['0', '1', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0',
               '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0',
               '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
               '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
               '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        self.assertEqual(parsed, ref)

    def test_status_string(self):
        status = '0100010001000000001000000000000000000000000000000000000000000000'
        strings = ApcUps.status_strings(status)
        self.assertEqual(['On Battery', 'Runtime Calibration'], strings)

    def test_on_battery(self):
        status = '0100010001000000001000000000000000000000000000000000000000000000'
        strings = ApcUps.status_strings(status)
        self.assertIn('On Battery', strings)

# On battery
# 0100010000000000001000000000000000000000000000000000000000000000
