import uuid

from django.db import models
from rest_framework.reverse import reverse
from django.utils.translation import ugettext as _
from localflavor.br.br_states import STATE_CHOICES

from .choices import MODELO_CHOICES, REGIOES_CHOICES, SITUACAO_CHOICES

class IdPubIdentifier(models.Model):
    id_pub = models.UUIDField(
            _('ID Público'),
            primary_key=True,
            default=uuid.uuid4,
            editable=False
    )

    def get_absolute_url(self):
        app_name = self._meta.app_label
        basename = self._meta.object_name.lower()
        url = app_name + ':' + basename + '-detail'

        return reverse(url, kwargs={'pk': self.id_pub})

    class Meta:
        abstract = True



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
    lat = models.DecimalField(
            _('Latitude'),
            max_digits=9,
            decimal_places=6,
            null=True,
            )
    long = models.DecimalField(
            _('Longitutde'),
            max_digits=9,
            decimal_places=6,
            null=True
            )

    def get_latlong(self):
        return (self.lat, self.long)

    def get_distance(self, origin):
        from geopy.distance import vincenty
        return vincenty(origin, self.get_latlong()).meters

    def save(self, *args, **kwargs):
        if not self.nome:
            self.nome = "CEU de {} - {}".format(self.municipio, self.uf.upper())
            super(Praca, self).save(*args, **kwargs)
        else:
            super(Praca, self).save(*args, **kwargs)



class Gestor(IdPubIdentifier):
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


class ProcessoAdmissao(IdPubIdentifier):
    gestor = models.ForeignKey(Gestor)
    data_abertura = models.DateTimeField(
            _('Data de Abertura do Processo'),
            auto_now_add=True,
            editable=False,
            blank=False
    )
    aprovado = models.BooleanField(
            _('Processo aprovado'),
            default=False,
            )

