from django.db import models

from ups import select


class Ups(models.Model):
    ip = models.GenericIPAddressField(unique=True)
    community = models.CharField(default='public', max_length=200)
    vendor = models.CharField(choices=[['Generic', 'RFC 1628'], ['APC', 'APC'], ['Eaton', 'Eaton'],
                                       ['APCSmartConnect', 'APC Smart Connect'],
                                       ['EPPC', 'PowerWalker EPPC'],
                                       ], default='Generic',
                              max_length=20)
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        if self.name:
            return '%s (%s)' % (self.name, self.ip)
        else:
            return self.ip

    def snmp(self):
        snmp_class = select(self.vendor)
        return snmp_class(self.ip, self.community)

    def last_event(self):
        return self.events.order_by('-time').first()

    class Meta:
        ordering = ['name']


class Status(models.Model):
    ups = models.OneToOneField(Ups, on_delete=models.CASCADE, related_name='status')
    status_time = models.DateTimeField(auto_now=True)


class Event(models.Model):
    ups = models.ForeignKey(Ups, on_delete=models.CASCADE, related_name='events')
    time = models.DateTimeField(auto_now_add=True)
    event = models.TextField()
