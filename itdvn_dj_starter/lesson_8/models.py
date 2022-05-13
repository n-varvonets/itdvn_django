from django.db import models


# Create your models here.
class GameModel(models.Model):
    """Модель игры"""
    name = models.CharField(max_length=64)
    platform = models.CharField(max_length=64)
    year = models.DateField()
    genre = models.CharField(max_length=64)
    publisher = models.CharField(max_length=64)
    na_sales = models.FloatField()
    eu_sales = models.FloatField()
    jp_sales = models.FloatField()
    other_sales = models.FloatField()
    global_sales = models.FloatField()


