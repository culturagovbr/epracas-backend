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

class Atividades(models.Model):
    tipo = models.ForeignKey(Tipos)
    area = models.ForeignKey(Areas)
    subarea = models.ForeignKey(Subareas)
    espacos = models.ManyToManyField(Espacos)
    parceiros = models.CharField(max_length=255)
    faixas_etarias = models.ManyToManyField(FaixasEtarias)
    publico = models.ManyToManyField(Publico)
    abrangencia = models.ForeignKey(Abrangencia)
    data_inicio = models.DateField()
    data_termino = models.DateField()
    periodicidade = models.ForeignKey(Periodicidade)
    hora_inicio = models.TimeField()
    hora_termino = models.TimeField()
    publico_esperado = models.IntegerField()
