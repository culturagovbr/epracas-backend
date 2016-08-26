from django.db import models
from localflavor.br.br_states import STATE_CHOICES

from .choices import MODELO_CHOICES, REGIOES_CHOICES, SITUACAO_CHOICES

class Praca(models.Model):
    contrato = models.IntegerField('Nº de Contrato', max_length=10)
    regiao = models.CharField(
            'Região',
            max_length=2,
            choices=REGIOES_CHOICES
            )
    uf = models.CharField('UF', max_length=2, choices=STATE_CHOICES)
    municipio = models.CharField('Municipio', max_length=140)
    modelo = models.CharField(
            'Modelo de Praça',
            max_length=1,
            choices=MODELO_CHOICES
            )
    situacao = models.CharField(
            'Situação',
            max_length=1,
            choices=SITUACAO_CHOICES
            )
