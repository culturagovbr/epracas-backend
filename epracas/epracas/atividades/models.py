from django.db import models

# Create your models here.

class Areas(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)

class Subareas(models.Model):
    area = models.ForeignKey(Areas, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)
