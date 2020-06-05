from django.db import models

from ups.rfc import RfcUps
from ups.select import select


class Ups(models.Model):
    ip = models.GenericIPAddressField()
    community = models.CharField(default='public', max_length=200)
    vendor = models.CharField(choices=[['APC', 'APC']], default='APC', max_length=20)
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        if self.name:
            return '%s (%s)' % (self.name, self.ip)
        else:
            return self.ip

    def snmp(self):
        snmp_class = select(self.vendor)
        return snmp_class(self.ip, self.community)

    def snmp_rfc(self):
        return RfcUps(self.ip, self.community)


class Status(models.Model):
    ups = models.OneToOneField(Ups, on_delete=models.CASCADE)
    status_time = models.DateTimeField(auto_now=True)


class Event(models.Model):
    ups = models.ForeignKey(Ups, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    event = models.TextField()
