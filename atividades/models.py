#coding: utf-8

from django.db import models
from django.utils.translation import ugettext as _

from core.models import IdPubIdentifier
from core.choices import FAIXA_ETARIA_CHOICES
import datetime

from schedule.models import Event

from pracas.models import Praca


class Area(IdPubIdentifier):
    nome = models.CharField(
        _('Área de Atividade'),
        max_length=200
        )
    parent = models.ForeignKey(
        'self',
        related_name="child",
        null=True,
        on_delete=models.CASCADE,
        )
    slug = models.SlugField(
        _('Slug'),
        max_length=400,
        blank=True
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            if self.parent:
                self.slug = slugify("{} - {}".format(self.parent, self.nome))
                super(Area, self).save(*args, **kwargs)
            else:
                self.slug = slugify(self.nome)
                super(Area, self).save(*args, **kwargs)


class Agenda(IdPubIdentifier):
    praca = models.ForeignKey(Praca, related_name='agenda')
    titulo = models.CharField(
            _('Titulo do Evento'),
            max_length=140,
            blank=False,
            )
    # area = models.ForeignKey(Area)
    justificativa = models.TextField(
            _('Justificativa da Atividade'),
            blank=True,
            null=True
            )
    # faixa_etaria = models.CharField(
    #     _('Faixa Etaria do Publico Alvo'),
    #     choices=FAIXA_ETARIA_CHOICES,
    #     max_length=1
    #     )
    espaco = models.CharField(
        _('Espaço de Realização do Atividade'),
        blank=True,
        null=True,
        max_length=200,
        )
    tipo = models.CharField(
        _('Categoria da Atividade'),
        max_length=200,
        )
    publico = models.CharField(
        _('Publico alvo da atividade'),
        max_length=200,
        )
    carga_horaria = models.IntegerField(
        _('Carga Horaria da Atividade')
        )
    publico_esperado = models.IntegerField(
        _('Publico Esperado para a Atividade')
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


    def save(self, force_insert=False, force_update=False):
        nova_agenda = False
        if not self.id:
            nova_agenda = True
        super(Agenda, self).save(force_insert, force_update)

        start = datetime.combine(self.data_inicio, self.hora_inicio)
        end = datetime.combine(self.data_encerramento, self.hora_encerramento)

        if nova_agenda:
            event = Event(  start = start,
                            end   = end,
                            title = self.titulo,
                            description = self.descricao)
            event.save()

            rel = EventRelation.objects.create_relation(event, self)
            rel.save()

            cal = null
            try:
                cal = Calendar.objects.get(pk=1)
            except Calendar.DoesNotExist:
                cal = Calendar(name = "epracas")
                cal.save()
            cal.events.add(event)
        else:
            event = Event.objects.get_for_object(self)[0]
            event.start = start
            event.end = end
            event.title = title
            event.description = self.description
            event.save()


class Relatorio(IdPubIdentifier):
    agenda = models.OneToOneField(Agenda, related_name='relatorio')
    realizado = models.BooleanField(
        _('Evento Realizado com Sucesso')
        )
    publico_presente = models.IntegerField(
        _('Publico presente a atividade')
        )
    pontos_positivos = models.TextField(
        _('Pontos Positivos da Atividade'),
        blank=True,
        null=True,
        )
    pontos_negativos = models.TextField(
        _('Pontos Negativos da Atividade'),
        blank=True,
        null=True,
        )


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
