import uuid

from django.db import models
from django.utils.translation import ugettext as _
from localflavor.br.br_states import STATE_CHOICES

from .choices import MODELO_CHOICES, REGIOES_CHOICES, SITUACAO_CHOICES

class Praca(models.Model):
    id_pub = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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


class Gestor(models.Model):
    id_pub = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            editable=False
    )
    nome = models.CharField(_('Nome'), max_length=250, blank=False, null=False)
    endereco = models.TextField(_('Endereço'), blank=True)
    cidade = models.CharField(_('Cidade'), max_length=140, blank=True)
    uf = models.CharField(
            _('UF(Estado)'),
            max_length=2,
            choices=STATE_CHOICES,
            blank=True
    )
    regiao = models.CharField(
            _('Região'),
            max_length=2,
            choices=REGIOES_CHOICES,
            blank=True
    )


class ProcessoAdmissao(models.Model):
    id_pub = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            editable=False
    )

