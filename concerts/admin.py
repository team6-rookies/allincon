from django.contrib import admin
from .models import Concert, Location, Site

# Register your models here.
admin.site.register(Concert)
admin.site.register(Location)
admin.site.register(Site)
