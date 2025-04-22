from django.db import models

# superuser: xnote, password: myk12345
# 장소 모델
class Location(models.Model):
    id = models.AutoField(primary_key=True)  # 자동 증가 id
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# 사이트 모델
class Site(models.Model):
    id = models.AutoField(primary_key=True)  # 자동 증가 id
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# 콘서트 모델
class Concert(models.Model):
    id = models.AutoField(primary_key=True)  # 자동 증가 id
    title = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
