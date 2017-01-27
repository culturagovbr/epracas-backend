from django.db import models
from django.utils.translation import ugettext as _
from rest_localflavor.br.br_states import STATE_CHOICES

from core.choices import MODELO_CHOICES
from core.choices import REGIOES_CHOICES
from core.choices import SITUACAO_CHOICES

from .choices import PARCEIRO_RAMO_ATIVIDADE

from core.models import IdPubIdentifier


def upload_header_to(instance, filename):
    ext = filename.split('.')[-1]
    id_pub = instance.id_pub
    return '{}/images/header.{}'.format(id_pub, ext)


class Praca(IdPubIdentifier):
    nome = models.CharField(
            _('Nome da Praça'),
            max_length=250,
            blank=True,
            )
    slug = models.SlugField(
            _('Nome Publico'),
            max_length=250,
            blank=True,
            )
    contrato = models.IntegerField('Nº de Contrato', max_length=10)
    logradouro = models.CharField(
            _('Logradouro'),
            max_length=200,
            blank=True, null=True
    )
    cep = models.IntegerField(_('CEP'), blank=True, null=True)
    bairro = models.CharField(
            _('Bairro'),
            max_length=100,
            blank=True,
            null=True
    )
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
    data_inauguracao = models.DateField(
        _('Data de Inauguração'),
        blank=True,
        null=True
        )
    lat = models.DecimalField(
        _('Latitude'),
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
        )
    long = models.DecimalField(
        _('Longitutde'),
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
        )
    header_img = models.FileField(
        blank=True,
        upload_to=upload_header_to,
        )

    def get_latlong(self):
        return (self.lat, self.long)

    def get_distance(self, origin):
        from geopy.distance import vincenty
        return vincenty(origin, self.get_latlong()).meters

    def save(self, *args, **kwargs):
        if not self.nome:
            self.nome = "Praça CEU de {} - {}".format(
                self.municipio, self.uf.upper())
            if not self.slug:
                from django.utils.text import slugify
                self.slug = slugify(self.nome)
                super(Praca, self).save(*args, **kwargs)
        elif not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.nome)
            super(Praca, self).save(*args, **kwargs)
        else:
            super(Praca, self).save(*args, **kwargs)

    class Meta:
        ordering = ['uf', 'municipio']
        verbose_name = 'praca'
        verbose_name_plural = 'pracas'


class Parceiro(IdPubIdentifier):
    nome = models.CharField(
        _('Nome Institucional do Parceiro'),
        max_length=300,
        )
    endereco = models.TextField(
        _('Endereço')
        )
    contato = models.CharField(
        _('Nome do Contato'),
        max_length=200,
        blank=True,
        null=True,
        )
    telefone = models.IntegerField(
        _('Telefone de Contato'),
        blank=True,
        null=True,
        )
    email = models.EmailField(
        _('Email de Contato'),
        blank=True,
        null=True,
        )
    ramo_atividade = models.IntegerField(
        _('Ramo de Atividade'),
        choices=PARCEIRO_RAMO_ATIVIDADE,
        )
    acoes = models.TextField(
        _('Açoes realizadas em parceria'),
        blank=True,
        null=True,
        )
    tempo_parceria = models.IntegerField(
        _('Tempo previsto para a parceria'),
        blank=True,
        null=True
        )
    lat = models.DecimalField(
        _('Latitude'),
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
        )
    long = models.DecimalField(
        _('Longitutde'),
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
        )
