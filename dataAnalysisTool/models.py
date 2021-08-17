from django.db import models

# Create your models here.


class DataHumTemp(models.Model):
    humidity = models.DecimalField(decimal_places=2, max_digits=5)
    temp = models.DecimalField(decimal_places=2, max_digits=5)
    time = models.TimeField()

