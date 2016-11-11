import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify
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


def upload_header_to(instance, filename):
    ext = filename.split('.')[-1]
    id_pub = instance.id_pub
    return '{}/images/header.{}'.format(id_pub, ext)


def upload_doc_to(instance, filename):
    new_name = slugify(filename.split('.')[:-1])
    ext = filename.split('.')[-1]
    id_pub = instance.processo.praca.id_pub
    return '{id_pub}/docs/{new_name}.{ext}'.format(
        id_pub=id_pub,
        new_name=new_name,
        ext=ext)


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


class ProcessoVinculacao(IdPubIdentifier):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    praca = models.ForeignKey(Praca)
    data_abertura = models.DateTimeField(
        _('Data de Abertura do Processo'),
        auto_now_add=True,
        editable=False,
        blank=False
        )
    data_finalizacao = models.DateTimeField(
        _('Data de Conclusão do Processo de Vinculação'),
        null=True,
        blank=True
        )
    aprovado = models.BooleanField(
        _('Processo aprovado'),
        default=False,
        )
    valido = models.BooleanField(
        _('Processo Válido'),
        default=True,
        )


class ArquivosProcessoVinculacao(IdPubIdentifier):
    processo = models.ForeignKey(ProcessoVinculacao, related_name='files')
    data_envio = models.DateTimeField(
        _('Data de Envio do Arquivo'),
        auto_now_add=True,
        blank=False
        )
    tipo = models.CharField(
        _('Tipo de Arquivo'),
        max_length=8
        )
    arquivo = models.FileField(upload_to=upload_doc_to)
    verificado = models.BooleanField(
        _('Arquivo verificado pelo gestor do Ministério'),
        default=False,
        )
    comentarios = models.TextField(
        _('Comentários sobre o arquivo'),
        null=True,
        blank=True
        )
    verificado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        )


class Agenda(IdPubIdentifier):
    praca = models.ForeignKey(Praca, related_name='agenda')
    titulo = models.CharField(
            _('Titulo do Evento'),
            max_length=140,
            blank=False,
            )
    data_inicio = models.DateTimeField(
            _('Data de Inicio da atividade'),
            )
    data_encerramento = models.DateTimeField(
            _('Data de Encerramento da atividade'),
            blank=True,
            null=True,
            )
    hora_inicio = models.TimeField(
            _('Horario de Inicio da atividade'),
            blank=False,
            null=True
            )
    hora_encerramento = models.TimeField(
            _('Horario de encerramento da atividade'),
            blank=False,
            null=True
            )
    local = models.CharField(
            _('Esta atividade será realizada em que parte da Praça?'),
            max_length=100,
            blank=True,
            null=True
            )
    descricao = models.TextField(
            _('Descrição da Atividade'),
            blank=True,
            null=True
            )

    class Meta:
        ordering = ['data_inicio', 'hora_inicio', 'data_encerramento']
