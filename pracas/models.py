from datetime import date

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.utils.text import slugify

from rest_framework.reverse import reverse
from rest_localflavor.br.br_states import STATE_CHOICES

from core.choices import MODELO_CHOICES
from core.choices import REGIOES_CHOICES
from core.choices import SITUACAO_CHOICES

from core.models import IdPubIdentifier
from core.models import upload_grupogestor_to

from .choices import PARCEIRO_RAMO_ATIVIDADE
from .choices import ORIGEM_CHOICES
from .choices import DOCUMENTO_CHOICES


def upload_image_to(instance, filename):
    ext = filename.split('.').pop(-1)
    filename = slugify(filename.split('.').remove(ext))
    try:
        praca = instance.praca.id_pub
        id_pub = instance.id_pub
    except:
        praca = instance.id_pub
        id_pub = 'header'
    return f'{praca}/images/{id_pub}.{ext}'


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
    contrato = models.IntegerField('Nº de Contrato')
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
    bio = models.TextField(
        _('Descrição/Biografia da Praça'),
        null=True,
        blank=True
        )
    header_img = models.FileField(
        blank=True,
        upload_to=upload_image_to,
        )
    repasse = models.DecimalField(
        _('Repasses do Ministério'),
        decimal_places=2,
        max_digits=12,
        null=True,
        blank=True,
        )

    def get_latlong(self):
        """
        Retorna latitude e longitude no formato (lat, long)
        """
        return (self.lat, self.long)

    def get_distance(self, origin):
        """
        Dado um determinado ponto, calcula a distancia até a Praça
        """
        from geopy.distance import vincenty
        return round(vincenty(origin, self.get_latlong()).meters, -2)

    def get_manager(self):
        """
        Retorna o atual gestor da Praça
        """
        try:
            return self.gestor.filter(data_encerramento_gestao=None).get(atual=True)
        except:
            return None

    def get_grupogestor(self):
        """
        Retorna o grupo gestor vigente da Praça
        """
        try:
            return self.grupo_gestor.get(data_finalizacao=None)
        except:
            return None

    def save(self, *args, **kwargs):
        if not self.nome:
            self.nome = "Praça CEU de {} - {}".format(
                self.municipio, self.uf.upper())
            if not self.slug:
                self.slug = slugify(self.nome)
                super(Praca, self).save(*args, **kwargs)
        elif not self.slug:
            self.slug = slugify(self.nome)
            super(Praca, self).save(*args, **kwargs)
        else:
            super(Praca, self).save(*args, **kwargs)

    class Meta:
        ordering = ['uf', 'municipio']
        verbose_name = 'praca'
        verbose_name_plural = 'pracas'


class ImagemPraca(IdPubIdentifier):
    praca = models.ForeignKey(Praca, related_name='imagem')
    arquivo = models.FileField(blank=True, upload_to=upload_image_to)
    header = models.BooleanField(default=False)
    titulo = models.CharField(blank=True, null=True, max_length=140)
    descricao = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        app_name = self._meta.app_label
        basename = self._meta.object_name.lower()
        url = app_name + ':' + basename + '-detail'

        return reverse(url, kwargs={'praca_pk': self.praca.pk, 'pk': self.pk})


class Parceiro(IdPubIdentifier):
    praca = models.ForeignKey(Praca, related_name='parceiros', null=True)
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
    telefone = models.CharField(
        _('Telefone de Contato'),
        blank=True,
        null=True,
        max_length=15
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
    recursos_financeiros = models.DecimalField(
        _('Recursos Financeiros'),
        max_digits=12,
        decimal_places=2,
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
        blank=True)


class GrupoGestor(IdPubIdentifier):
    praca = models.ForeignKey(Praca, related_name='grupo_gestor')
    previsao_espacos = models.IntegerField(
        _('Qtde de membros previstos no Grupo Gestor'), max_length=2)
    data_instituicao = models.DateField(
        _('Data de Instituição do Grupo Gestor'),
        default=timezone.now)
    data_finalizacao = models.DateField(
        _('Data de Finalização do Grupo Gestor'),
        blank=True,
        null=True)
    documento_constituicao = models.FileField(
        _('Documento de Constituição do Grupo Gestor'),
        upload_to=upload_grupogestor_to,
        blank=True,
        null=True)
    tipo_documento = models.CharField(
        _('Tipo de documento de constituição'),
        max_length=1,
        blank=True,
        null=True,
        choices=DOCUMENTO_CHOICES)

    class Meta:
        ordering = ['-data_instituicao']


class MembroGestor(IdPubIdentifier):
    grupo_gestor = models.ForeignKey(GrupoGestor, related_name='membros')
    nome = models.CharField(_('Nome do Gestor'), max_length=120)
    origem = models.CharField(_('Origem do Membro'),
                              max_length=2, choices=ORIGEM_CHOICES)
    data_posse = models.DateField(
        _('Data de Posse do Membro Gestor'),
        default=date.today
        )
    data_desligamento = models.DateField(
        _('Data de Desligamento do Membro Gestor'),
        blank=True,
        null=True,
        )
    documento_posse = models.FileField(
        _('Documento de Posse do Membro Gestor'),
        upload_to=upload_grupogestor_to,
        blank=True,
        null=True)
    tipo_documento = models.CharField(
        _('Tipo de documento de posse'),
        max_length=1,
        blank=True,
        null=True,
        choices=DOCUMENTO_CHOICES)


class MembroUgl(IdPubIdentifier):
    praca = models.ForeignKey(Praca, related_name='ugl')
    nome = models.CharField(_('Nome do Membro'), max_length=150)
