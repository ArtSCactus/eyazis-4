from django.db import models


# Create your models here.
class EngToGerDict(models.Model):
    source = models.TextField()
    translation = models.TextField()
