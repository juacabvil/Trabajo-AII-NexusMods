from django.db import models


class Juego(models.Model):
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
    game = models.ForeignKey(Juego, on_delete=models.CASCADE)


