from django.contrib import admin
from .models import Ups, Event


@admin.register(Ups)
class UpsAdmin(admin.ModelAdmin):
    list_display = ['name', 'ip', 'vendor']
    list_filter = ['vendor']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['ups', 'time', 'event']
    list_filter = ['ups']
