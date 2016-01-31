from django.db import models

# Create your models here.

class Areas(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)

class Subareas(models.Model):
    area = models.ForeignKey(Areas, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)

class Atividades(models.Model):
    tipo = models.ForeignKey(Tipo)
    area = models.ForeignKey(Areas)
    subarea = models.ForeignKey(Subareas)
    espacos = models.ManyToManyField(Espacos)
    parceiros = models.CharField(max_length=255)
    faixas_etarias = models.ManyToManyField(FaixasEtarias)
    publico = models.ManyToManyField(Publicos)
    abrangencia = models.ForeignKey(Abrangencias)
    data_inicio = models.DateField()
    data_termino = models.DateField()
    periodicidade = models.ForeignKey(Periodicidades)
    hora_inicio = models.DateField()
    hora_termino = models.DateField()
    publico_esperado = models.IntegerField()
