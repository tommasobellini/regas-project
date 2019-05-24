from django.db import models
from datetime import datetime


class Sensor(models.Model):
    name = models.CharField(max_length=40)
    location = models.CharField(max_length=40)


class SensorLine(models.Model):
    sensor = models.ForeignKey('Sensor', on_delete=models.DO_NOTHING)
    humidity = models.DecimalField(max_digits=4, decimal_places=2)
    temperature = models.DecimalField(max_digits=4, decimal_places=2)
    datetime = models.DateTimeField(default=datetime.today())
