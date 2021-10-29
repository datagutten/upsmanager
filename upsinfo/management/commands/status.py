from pprint import pprint

from django.core.management.base import BaseCommand

from upsinfo.models import Ups


class Command(BaseCommand):
    help = 'Show UPS status'

    def add_arguments(self, parser):
        parser.add_argument('ip', nargs='+', type=str)

    def handle(self, *args, **options):
        ip = options['ip'][0]
        ups = Ups.objects.get(ip=ip)
        snmp = ups.snmp()
        print(snmp.status())
        print(snmp.status_string())
        print(ups.snmp().battery_voltage())
