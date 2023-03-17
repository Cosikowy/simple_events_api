from django.contrib import admin

from events.models import Artist, Event, Performence

admin.site.register(Artist)
admin.site.register(Event)
admin.site.register(Performence)
