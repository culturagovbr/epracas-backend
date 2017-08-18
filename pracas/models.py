from datetime import date

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.utils.text import slugify

from django.contrib.postgres.fields import ArrayField

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
from .choices import MEMBRO_UGL_CHOICES
from .choices import ESCOLARIDADE_CHOICES
from .choices import FORMACAO_CHOICES
from .choices import VINCULO_CHOICES
from .choices import ATUACAO_CHOICES
from .choices import DESCRICAO_CHOICES

from atividades.choices import ESPACOS_CHOICES


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
    telefone1 = models.CharField(
        _('Telefone de Contato'),
        blank=True,
        null=True,
        max_length=15
        )
    telefone2 = models.CharField(
        _('Telefone de Contato'),
        blank=True,
        null=True,
        max_length=15
        )
    fax = models.CharField(
        _('Fax'),
        blank=True,
        null=True,
        max_length=15
        )
    email1 = models.CharField(
        _('Primeiro Email de Contato'),
        blank=True,
        null=True,
        max_length=200,
        )
    email2 = models.EmailField(
        _('Segundo Email de Contato'),
        blank=True,
        null=True,
        )
    pagina = models.URLField(
        _('Pagina do CEU nas redes sociais'),
        blank=True,
        null=True,
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

    def get_rh_ativos(self):
        """
        Retorna os Recursos Humanos ativos da Praça
        """

        try:
            return self.rh.filter(data_saida=None)
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
    email = models.CharField(
        _('Email de Contato'),
        blank=True,
        null=True,
        max_length=200,
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
    imagem = models.FileField(blank=True, upload_to=upload_image_to)


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
    estatuto = models.FileField(
        _('Estatuto do Grupo Gestor'),
        upload_to=upload_grupogestor_to,
        blank=True,
        null=True)
    tipo_documento = models.CharField(
        _('Tipo de documento de constituição'),
        max_length=1,
        blank=True,
        null=True,
        choices=DOCUMENTO_CHOICES)

    def get_absolute_url(self):
        app_name = self._meta.app_label
        basename = self._meta.object_name.lower()
        url = app_name + ':' + basename + '-detail'

        return reverse(url, kwargs={'praca_pk': self.praca.pk, 'pk': self.pk})

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

    def get_absolute_url(self):
        app_name = self._meta.app_label
        basename = self._meta.object_name.lower()
        url = app_name + ':' + basename + '-detail'

        return reverse(url, kwargs={'praca_pk': self.praca.pk, 'pk': self.pk})


class MembroUgl(IdPubIdentifier):
    praca = models.ForeignKey(Praca, related_name='ugl')
    nome = models.CharField(_('Nome do Membro'), max_length=250)
    tipo = models.CharField(_('Tipo de Membro'), max_length=3,
                            choices=MEMBRO_UGL_CHOICES,
                            default='cg')
    telefone = models.CharField(
        _('Telefone de Contato'),
        blank=True,
        null=True,
        max_length=15
        )
    email = models.CharField(
        _('Email de Contato'),
        blank=True,
        null=True,
        max_length=200,
        )

    def get_absolute_url(self):
        app_name = self._meta.app_label
        basename = self._meta.object_name.lower()
        url = app_name + ':' + basename + '-detail'

        return reverse(url, kwargs={'praca_pk': self.praca.pk, 'pk': self.pk})


class Rh(IdPubIdentifier):
    praca = models.ForeignKey(Praca, related_name='rh')
    nome = models.CharField(_('Nome'), max_length=300)
    identificacao = models.CharField(_('Documento Identidade'), max_length=14,
                                     blank=True, null=True)
    sexo = models.CharField(_('Sexo'), max_length=1, blank=True, null=True,
                            choices=(('f', 'Feminino'), ('m', 'Masculino')))
    escolaridade = models.CharField(_('Escolaridade'), max_length=3,
                                    choices=ESCOLARIDADE_CHOICES, blank=True,
                                    null=True)
    formacao = models.CharField(_('Formação'), max_length=3, blank=True,
                                choices=FORMACAO_CHOICES, null=True)
    vinculo = models.CharField(_('Tipo de vínculo'), max_length=3, blank=True,
                               null=True, choices=VINCULO_CHOICES)
    funcao = models.CharField(_('Função'), max_length=200, blank=True,
                              null=True)
    carga_horaria = models.CharField(_('Carga Horaria'), max_length=3,
                                     blank=True, null=True)
    remuneracao = models.DecimalField(_('Remuneração Mensal'), max_length=7,
                                      decimal_places=2, max_digits=2,
                                      blank=True, null=True)
    local_trabalho = ArrayField(
        models.IntegerField(_('Local de Trabalho no CEU'),
                            choices=ESPACOS_CHOICES, blank=True,
                            null=True), default=list)
    data_entrada = models.DateField(_('Data de Entrada'), default=date.today)
    data_saida = models.DateField(_('Data de Saída'), blank=True, null=True)

    def get_absolute_url(self):
        app_name = self._meta.app_label
        basename = self._meta.object_name.lower()
        url = app_name + ':' + basename + '-detail'

        return reverse(url, kwargs={'praca_pk': self.praca.pk, 'pk': self.pk})

    class Meta:
        ordering = ['nome', 'data_entrada']


class Ator(IdPubIdentifier):
    praca = models.ForeignKey(Praca, related_name='atores')
    nome = models.CharField(_('Nome do Ator'), max_length=350)
    area = models.CharField(_('Área de Atuação'), max_length=4,
                            choices=ATUACAO_CHOICES)
    descricao = models.IntegerField(_('Descrição da Atividade do Ator'),
                                    choices=DESCRICAO_CHOICES)
    imagem = models.FileField(blank=True, upload_to=upload_image_to)
    endereco = models.TextField(_('Endereço'), blank=True, null=True)
    telefone1 = models.CharField(
        _('Telefone de Contato'),
        blank=True,
        null=True,
        max_length=15
        )
    telefone2 = models.CharField(
        _('Telefone de Contato'),
        blank=True,
        null=True,
        max_length=15
        )
    email = models.CharField(
        _('Email de Contato'),
        blank=True,
        null=True,
        max_length=200
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

    def get_absolute_url(self):
        app_name = self._meta.app_label
        basename = self._meta.object_name.lower()
        url = app_name + ':' + basename + '-detail'

        return reverse(url, kwargs={'praca_pk': self.praca.pk, 'pk': self.pk})
