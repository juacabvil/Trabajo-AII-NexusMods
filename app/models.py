from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=255)
    mods = models.IntegerField()
    downloads = models.IntegerField()

class Mod(models.Model):
    name = models.CharField(max_length=255)
    last_update = models.DateField()
    uploader = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    downloads = models.IntegerField()
    categories = models.CharField(max_length=255)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

class Colection(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    likes = models.IntegerField()
    mods = models.IntegerField()



