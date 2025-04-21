from django.contrib import admin
from .models import Concert, Location

class ConcertAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'location', 'start_date', 'end_date')
    list_filter = ('location', 'start_date')
    search_fields = ('title', 'location__name')

admin.site.register(Concert, ConcertAdmin)
admin.site.register(Location)