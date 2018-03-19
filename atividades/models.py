from uuid import uuid4

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from django.contrib.postgres.fields import ArrayField

from eventtools.models import BaseEvent, BaseOccurrence

from core.models import IdPubIdentifier
from core.choices import FAIXA_ETARIA_CHOICES

from pracas.models import Praca

from .choices import ESPACOS_CHOICES
from .choices import FAIXA_ETARIA_CHOICES
from .choices import TIPO_ATIVIDADE_CHOICES
from .choices import TERRITORIO_CHOICES
from .choices import PUBLICO_CHOICES


def upload_image_to(instance, filename):
    ext = filename.split('.')[-1]
    id_pub = instance.id_pub
    uuid_filename = uuid4()
    return '{}/images/atividades/{}.{}'.format(id_pub, uuid_filename, ext)


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
    faixa_etaria = ArrayField(
        models.IntegerField(
            choices=FAIXA_ETARIA_CHOICES,
            null=True),
        null=True,
        default=list())
    espaco = ArrayField(
        models.IntegerField(
            choices=ESPACOS_CHOICES,
            null=True),
        null=True,
        default=list())
    tipo = models.IntegerField(
        _('Categoria da Atividade'), choices=TIPO_ATIVIDADE_CHOICES)
    publico = models.CharField(
        _('Publico alvo da atividade'),
        choices=PUBLICO_CHOICES,
        max_length=2,
        null=True,
        blank=True)
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

    def get_manager(self):
        """
        Retorna o atual gestor da Praça
        """
        return self.praca.get_manager()


class Ocorrencia(BaseOccurrence):

    REPEAT_CHOICES = (("once", 'Apenas uma vez'), ("daily", 'Diariamente'),
                      ("weekly", 'Semanalmente'), ("monthly", 'Mensalmente'),
                      ("yearly", 'Anualmente'), )

    event = models.OneToOneField(Agenda, related_name='ocorrencia')
    frequency_type = models.CharField(choices=REPEAT_CHOICES, max_length=19,
                                      default='once')
    weekday = models.CharField(max_length=20, blank=True, null=True)

    def get_count_value(self):
        if self.frequency_type == 'daily':
            weeks = ((self.repeat_until - self.start.date()) // 7).days + 1
            if weeks > 1 and self.weekday:
                count = weeks * len(self.weekday.split(','))
            elif self.weekday:
                count = len(self.weekday.split(','))
            else:
                count = (self.repeat_until - self.start.date()).days + 1

            return count

    def save(self, *args, **kwargs):
        if self.frequency_type == "daily" and self.weekday:
            self.count = self.get_count_value()
            self.repeat = "RRULE:FREQ={freq};BYDAY={weekday};COUNT={count}".format(
                freq=self.frequency_type.upper(),
                weekday=self.weekday.upper(),
                count=self.count)
            super(Ocorrencia, self).save(*args, **kwargs)
        elif self.frequency_type == "daily" and not self.weekday:
            self.count = self.get_count_value()
            self.repeat = "RRULE:FREQ={freq};COUNT={count}".format(
                freq=self.frequency_type.upper(),
                count=self.count)
            super(Ocorrencia, self).save(*args, **kwargs)
        else:
            super(Ocorrencia, self).save(*args, **kwargs)


class Relatorio(IdPubIdentifier):
    agenda = models.ForeignKey(Agenda, related_name='relatorios')
    realizado = models.BooleanField(_('Evento Realizado com Sucesso'), default=False)
    publico_presente = models.IntegerField(_('Publico presente a atividade'),
                                           null=True, blank=True)
    pontos_positivos = models.TextField(
        _('Pontos Positivos da Atividade'),
        blank=True,
        null=True, )
    pontos_negativos = models.TextField(
        _('Pontos Negativos da Atividade'),
        blank=True,
        null=True, )
    data_de_ocorrencia = models.DateField(default=timezone.now)
    data_prevista = models.DateTimeField(blank=True, null=True)


class RelatorioImagem(IdPubIdentifier):
    relatorio = models.ForeignKey(Relatorio, related_name='imagens', null=True)
    agenda = models.ForeignKey(Agenda, related_name='imagens', null=True)
    arquivo = models.FileField(upload_to=upload_image_to)
    anotacoes = models.TextField(null=True, blank=True)
