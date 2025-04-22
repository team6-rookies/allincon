from django.db import models

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Site(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Concert(models.Model):
    title = models.CharField(max_length=200)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='concerts')
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
    
