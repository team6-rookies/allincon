from django.db import models
from django.shortcuts import render

# superuser: xnote, password: myk12345
# 장소 모델
class Location(models.Model):
    location_id = models.AutoField(primary_key=True)  # 자동 증가 id
    location_name = models.CharField(max_length=200)

    def __str__(self):
        return self.location_name

# 사이트 모델
class Site(models.Model):
    site_id = models.AutoField(primary_key=True)  # 자동 증가 id
    site_name = models.CharField(max_length=200)

    def __str__(self):
        return self.site_name

# 콘서트 모델
class Concert(models.Model):
    concert_id = models.AutoField(primary_key=True)  # 자동 증가 id
    title = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

