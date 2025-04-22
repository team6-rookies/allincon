from django.contrib import admin

# Register your models here.

# model에 적재한 데이터를 확인하고 관리하는 interface
#그 방법 중 하나가 admin.py에 등록하는 것
from allincon.models import Concert, Location, Site
# admin.site.register(Concert)
# admin.site.register(Location)
# admin.site.register(Site)

# 이미 @admin.register(Concert)로 등록했기 때문에 admin.site.register()는 필요 없음
@admin.register(Concert)
class ConcertAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'location', 'start_date', 'end_date', 'site')
    search_fields = ('title',)
    list_filter = ('location', 'site')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'max_people')
    search_fields = ('name',)
    #list_filter = ('max_people',)

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('id','name',)
    search_fields = ('name',)
