import time

from django.core.management.base import BaseCommand

from ups import exceptions
from upsinfo.models import Event, Ups


class Command(BaseCommand):
    help = 'Log UPS status'

    def handle(self, *args, **options):
        ups_snmp = {}

        for ups in Ups.objects.filter(enabled=True):
            if ups.id not in ups_snmp:
                ups_snmp[ups.id] = [ups.snmp(), ups]

        while True:
            try:
                for [snmp, ups] in ups_snmp.values():
                    if snmp is None:
                        continue

                    try:
                        if hasattr(snmp, 'get_info'):
                            snmp.get_info()

                        strings = snmp.status_messages()
                        if not ups.last_event() or ups.last_event().event not in strings:
                            for string in strings:
                                event = Event(ups=ups, event=string)
                                event.save()
                    except exceptions.UPSTimeout:
                        print('Timeout: %s' % ups)
                        ups_snmp[ups.id] = [None, None]
                    except exceptions.UPSError as e:
                        print('Error: %s: %s' % (ups, e))
                        ups_snmp[ups.id] = [None, None]
                        if not ups.last_event() or ups.last_event().event != str(e):
                            event = Event(ups=ups, event=str(e))
                            event.save()
                time.sleep(60)
            except KeyboardInterrupt:
                break

        for [snmp, _] in ups_snmp.values():
            if snmp is not None and hasattr(snmp, 'session'):
                snmp.session.close()
