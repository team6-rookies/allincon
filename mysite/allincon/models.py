from django.db import models
from django.utils import timezone
from django.contrib import admin
import datetime

# Create your models here.


class Concert(models.Model):
    title = models.CharField(max_length=200)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    site=models.ForeignKey('Site', on_delete=models.CASCADE, null=True, blank=True)

    

    def __str__(self):
        return self.title
    

class Location(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=255, null=True, blank=True)  # 예시 필드
    max_people = models.IntegerField(null=True, blank=True)  # null 허용
    def __str__(self):
        return self.name
    
class Site(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name