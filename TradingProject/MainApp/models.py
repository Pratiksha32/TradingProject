from django.db import models
from datetime import datetime
# Create your models here.
class Candle(models.Model):
    id = models.AutoField(primary_key=True)
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    date = models.DateTimeField()

    def __str__(self):
        return f'Candle {self.id} - Date: {self.date}'