from django.contrib import admin

from events.forms import EventForm
from events.models import Event, EventStatus


class EventAdmin(admin.ModelAdmin):
    form = EventForm
    ordering = ("-id",)  # Ordonner les évènements par id par ordre décroissant pour avoir les plus récents en haut
    list_display = ('client', 'id')  # Informations qui seront affichées dans la rubrique évènements


# Register your models here.
admin.site.register(Event, EventAdmin)


class EventStatusAdmin(admin.ModelAdmin):
    ordering = ("-id",)  # Ordonner les utilisateurs par id par ordre décroissant pour avoir les plus récents en haut
    list_display = ('name', 'id')  # Informations qui seront affichées dans la rubrique des status


# Register your models here.
admin.site.register(EventStatus, EventStatusAdmin)
