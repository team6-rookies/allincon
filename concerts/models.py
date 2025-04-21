from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='공연장 이름')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '공연장'
        verbose_name_plural = '공연장 목록'
        ordering = ['name']

class Site(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='사이트 이름')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '출처 사이트'
        verbose_name_plural = '출처 사이트 목록'
        ordering = ['id']

class Concert(models.Model):
    title = models.CharField(max_length=200, verbose_name='콘서트 제목')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='concerts', verbose_name='공연 장소')
    start_date = models.DateField(null=True, blank=True, verbose_name='시작일')
    end_date = models.DateField(null=True, blank=True, verbose_name='종료일')
    source = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True,  related_name='concerts', verbose_name='출처사이트')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = '콘서트'
        verbose_name_plural = '콘서트 목록'
        ordering = ['start_date', 'title']