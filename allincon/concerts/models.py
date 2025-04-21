import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin



class Site(models.Model):
    id = models.IntegerField(primary_key=True)  # 기본 id 대신 명시적으로 설정
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Location(models.Model):
    id = models.IntegerField(primary_key=True)  # 기본 id 대신 명시적으로 설정
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class Concert(models.Model):
    # id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.title