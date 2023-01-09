from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=255)
    mods = models.FloatField()
    downloads = models.FloatField()

class Mod(models.Model):
    name = models.CharField(max_length=255)
    last_update = models.DateField()
    uploader = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    likes = models.FloatField(default=0.0)
    category = models.CharField(max_length=255)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

class Colection(models.Model):
    name = models.CharField(max_length=255)
    downloads = models.FloatField(default=0.0)
    likes = models.FloatField(default=0.0)
    mods = models.FloatField(default=0.0)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)



