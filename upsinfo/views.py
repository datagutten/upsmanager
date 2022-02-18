from django.shortcuts import render
from requests import HTTPError

from .models import Ups


def ups_list(request):
    snmp = []
    info_list = []
    for ups in Ups.objects.all():
        try:
            snmp_obj = ups.snmp()
            snmp_obj.name()
            snmp.append(snmp_obj)
            info_list.append({'snmp': snmp_obj, 'ups': ups})
        except ValueError as e:
            # snmp.append({'name': ups.name, 'status': 'Offline'})
            info_list.append({'ups': ups, 'error': e})
        except HTTPError as e:
            info_list.append({'ups': ups, 'error': e})

    return render(request, 'upsinfo/ups_list.html', {'ups_list': info_list})
