# coding: utf-8
from datetime import datetime, time

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from eventtools.models import BaseEvent, BaseOccurrence

from core.models import IdPubIdentifier
from core.choices import FAIXA_ETARIA_CHOICES

from pracas.models import Praca

from .choices import ESPACOS_CHOICES
from .choices import TIPO_ATIVIDADE_CHOICES
from .choices import TERRITORIO_CHOICES


class Area(IdPubIdentifier):
    nome = models.CharField(_('Área de Atividade'), max_length=200)
    parent = models.ForeignKey(
        'self',
        related_name="child",
        null=True,
        on_delete=models.CASCADE, )
    slug = models.SlugField(_('Slug'), max_length=400, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            if self.parent:
                self.slug = slugify("{} - {}".format(self.parent, self.nome))
                super(Area, self).save(*args, **kwargs)
            else:
                self.slug = slugify(self.nome)
                super(Area, self).save(*args, **kwargs)


class Agenda(IdPubIdentifier, BaseEvent):
    praca = models.ForeignKey(Praca, related_name='agenda')
    titulo = models.CharField(
        _('Titulo do Evento'),
        max_length=140,
        blank=False, )
    # area = models.ForeignKey(Area)
    justificativa = models.TextField(
        _('Justificativa da Atividade'), blank=True, null=True)
    # faixa_etaria = models.CharField(
    #     _('Faixa Etaria do Publico Alvo'),
    #     choices=FAIXA_ETARIA_CHOICES,
    #     max_length=1
    #     )
    espaco = models.IntegerField(
        _('Espaço de Realização do Atividade'),
        blank=True,
        null=True,
        choices=ESPACOS_CHOICES)
    tipo = models.IntegerField(
        _('Categoria da Atividade'), choices=TIPO_ATIVIDADE_CHOICES)
    publico = models.CharField(
        _('Publico alvo da atividade'),
        max_length=200, )
    carga_horaria = models.IntegerField(_('Carga Horaria da Atividade'))
    publico_esperado = models.IntegerField(
        _('Publico Esperado para a Atividade'))
    territorio = models.IntegerField(
        _('Qual é o espaço de abrangencia desta atividade'),
        blank=True,
        null=True,
        choices=TERRITORIO_CHOICES)
    descricao = models.TextField(
        _('Descrição da Atividade'), blank=True, null=True)


class Ocorrencia(BaseOccurrence):

    event = models.ForeignKey(Agenda, related_name='ocorrencia')


class Relatorio(IdPubIdentifier):
    agenda = models.ForeignKey(Agenda, related_name='relatorios')
    realizado = models.BooleanField(_('Evento Realizado com Sucesso'))
    publico_presente = models.IntegerField(_('Publico presente a atividade'))
    pontos_positivos = models.TextField(
        _('Pontos Positivos da Atividade'),
        blank=True,
        null=True, )
    pontos_negativos = models.TextField(
        _('Pontos Negativos da Atividade'),
        blank=True,
        null=True, )
    data_de_ocorrencia = models.DateField(default=timezone.now())


# class Atividade(models.Model):
#     nome = models.CharField(max_length=255)
#     descricao = models.TextField()
#     parceiros = models.CharField(max_length=255)
#     data_inicio = models.DateTimeField()
#     data_termino = models.DateTimeField()
#     # hora_inicio = models.TimeField()
#     # hora_termino = models.TimeField()
#     publico_esperado = models.IntegerField()
#     tipo = models.ForeignKey(Tipo)
#     area = models.ForeignKey(Area)
#     subarea = ChainedForeignKey(
#         Subarea,
#         chained_field='area',
#         chained_model_field='area',
#         show_all=False,
#         auto_choose=True,
#         blank=True,
#     )
#     espacos = models.ManyToManyField(Espaco)
#     faixas_etarias = models.ManyToManyField(FaixasEtaria)
#     publico = models.ManyToManyField(Publico)
#     abrangencia = models.ForeignKey(Abrangencia)
#     periodicidade = models.ForeignKey(Periodicidade)
#     ceu = models.ForeignKey(Ceu)

#     def __str__(self):
#         return self.nome
