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

    # def __str__(self):
    #     return f"{self.id}_{self.name}"


class GamerLibraryModel(models.Model):
    """Библиотека игр"""
    game = models.ManyToManyField("GameModel")  # M2M к играм
    gamer = models.ForeignKey("GamerModel", on_delete=models.DO_NOTHING)  # отношение к игроку(один игрок может иметь много игр)
    size = models.IntegerField()  # размер нашей библиотеки

    def __str__(self):
        return f"{self.id}_{self.gamer.nickname}"


class GamerModel(models.Model):
    """Модель нашего игрока"""
    nickname = models.CharField(max_length=64)
    email = models.EmailField()

    # def __str__(self):
    #     return f"{self.id}_{self.nickname}"



