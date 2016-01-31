from django.db import models

# Create your models here.

class Tipos(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)

class Espacos(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)

class FaixasEtarias(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)

class Parceiros(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)

class Publico(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)

class Abrangencia(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)

class Periodicidade(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)


class Areas(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)

class Subareas(models.Model):
    area = models.ForeignKey(Areas, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)
