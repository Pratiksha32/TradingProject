from django.db import models


# Create your models here.


class Candle(models.Model):
    id = models.AutoField(primary_key=True)
    BANKNIFTY = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    open = models.DecimalField(max_digits=10, decimal_places=2)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    close = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.PositiveIntegerField()
