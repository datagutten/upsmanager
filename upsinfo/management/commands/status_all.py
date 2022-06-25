from pprint import pprint

from django.core.management.base import BaseCommand

from upsinfo.models import Event, Ups


class Command(BaseCommand):
    help = 'Show UPS status'

    # def add_arguments(self, parser):
    #    parser.add_argument('ip', nargs='+', type=str)

    def handle(self, *args, **options):
        # ip = options['ip'][0]
        for ups in Ups.objects.all():
            snmp = ups.snmp()
            # print(snmp.status())

            try:
                strings = snmp.status_messages()
                if not ups.last_event() or ups.last_event().event not in strings:
                    for string in strings:
                        event = Event(ups=ups, event=string)
                        event.save()
            except ValueError as e:
                print(e)
            except AttributeError:
                string = snmp.status_string()
                if not ups.last_event() or ups.last_event().event != string:
                    event = Event(ups=ups, event=string)
                    event.save()
