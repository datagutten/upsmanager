from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render

from ups import exceptions
from .models import Ups

connections = {}


def ups_info(ups: Ups):
    name = ups.name
    try:
        if ups.id not in connections:
            connections[ups.id] = ups.snmp()

        snmp_obj = connections[ups.id]
        if hasattr(snmp_obj, 'get_info'):
            try:
                snmp_obj.get_info()
            except exceptions.UPSError:
                del connections[ups.id]
                connections[ups.id] = ups.snmp()
                snmp_obj = connections[ups.id]

        # Always try to fetch name to trigger exception
        snmp_name = snmp_obj.name()
        if not name:
            name = snmp_name

        return {'snmp': snmp_obj, 'ups': ups, 'name': name}
    except exceptions.UPSTimeout:
        return {'ups': ups, 'name': name, 'error': 'Offline'}
    except exceptions.UPSError as e:
        return {'ups': ups, 'name': name, 'error': e}


def ups_list(request):
    info_list = []
    for ups in Ups.objects.filter(enabled=True):
        info_list.append(ups_info(ups))

    return render(request, 'upsinfo/ups_list.html', {'ups_list': info_list})


def events(request):
    ip = request.GET.get('ip')
    if ip:
        ups = get_object_or_404(Ups, ip=ip)
    else:
        return HttpResponseBadRequest()
    events_obj = ups.events.all().order_by('-time')
    return render(request, 'upsinfo/event_log.html', {
        'ups': ups,
        'events': events_obj,
        'title': 'UPS events: %s' % ups.name,
    })
