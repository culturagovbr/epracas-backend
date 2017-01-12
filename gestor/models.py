#coding: utf-8

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _

from core.models import IdPubIdentifier
from core.models import upload_doc_to

from pracas.models import Praca

from core.choices import REGIOES_CHOICES

from rest_localflavor.br.br_states import STATE_CHOICES


class Gestor(IdPubIdentifier):
    nome = models.CharField(_(u'Nome'), max_length=250, blank=False, null=False)
    endereco = models.TextField(_(u'Endereço'), blank=True)
    cidade = models.CharField(_(u'Cidade'), max_length=140, blank=True)
    uf = models.CharField(
            _(u'UF(Estado)'),
            max_length=2,
            choices=STATE_CHOICES,
            blank=True
    )
    regiao = models.CharField(
            _(u'Região'),
            max_length=2,
            choices=REGIOES_CHOICES,
            blank=True
    )


class ProcessoVinculacao(IdPubIdentifier):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    praca = models.ForeignKey(Praca)
    data_abertura = models.DateTimeField(
        _(u'Data de Abertura do Processo'),
        auto_now_add=True,
        editable=False,
        blank=False
        )
    data_finalizacao = models.DateTimeField(
        _(u'Data de Conclusão do Processo de Vinculação'),
        null=True,
        blank=True
        )
    aprovado = models.BooleanField(
        _(u'Processo aprovado'),
        default=False,
        )
    valido = models.BooleanField(
        _(u'Processo Válido'),
        default=True,
        )


class ArquivosProcessoVinculacao(IdPubIdentifier):
    processo = models.ForeignKey(ProcessoVinculacao, related_name='files')
    data_envio = models.DateTimeField(
        _(u'Data de Envio do Arquivo'),
        auto_now_add=True,
        blank=False
        )
    tipo = models.CharField(
        _(u'Tipo de Arquivo'),
        max_length=8
        )
    arquivo = models.FileField(upload_to=upload_doc_to)
    verificado = models.BooleanField(
        _(u'Arquivo verificado pelo gestor do Ministério'),
        default=False,
        )
    comentarios = models.TextField(
        _(u'Comentários sobre o arquivo'),
        null=True,
        blank=True
        )
    verificado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        )
