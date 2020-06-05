from pprint import pprint

from django.core.management.base import BaseCommand

from upsinfo.models import Ups


class Command(BaseCommand):
    help = 'Show UPS status'

    # def add_arguments(self, parser):
    #    parser.add_argument('ip', nargs='+', type=str)

    def handle(self, *args, **options):
        # ip = options['ip'][0]
        for ups in Ups.objects.all():
            snmp = ups.snmp()
            # print(snmp.status())
            print(ups)
            try:
                print(snmp.status_string())
            except ValueError as e:
                print(e)
