from datetime import date

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext as _

from rest_framework.reverse import reverse
from rest_framework.serializers import ValidationError

from core.models import IdPubIdentifier
from core.models import upload_doc_to

from pracas.models import Praca

from core.choices import REGIOES_CHOICES

from .choices import SITUACAO

from rest_localflavor.br.br_states import STATE_CHOICES


class Gestor(IdPubIdentifier):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                             related_name='gestor')
    praca = models.ForeignKey(Praca, related_name='gestor', null=True)
    atual = models.BooleanField(_('Gestor Atual'), default=False)
    data_inicio_gestao = models.DateField(
        _('Data de Inicio da Gestão'),
        default=timezone.now)
    data_encerramento_gestao = models.DateField(
        _('Data de Encerramento da Gestão'),
        null=True)

    def save(self, *args, **kwargs):
        if self.atual:
            try:
                assert Gestor.objects.filter(atual=True).filter(praca=self.praca).count() == 0
            except AssertionError:
                raise Exception(_('Já existe um Gestor para esta Praça'))
        super(Gestor, self).save(*args, **kwargs)


class ProcessoVinculacao(IdPubIdentifier):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    praca = models.ForeignKey(Praca)
    data_abertura = models.DateTimeField(
        _('Data de Abertura do Processo'),
        auto_now_add=True,
        editable=False,
        blank=False)
    data_finalizacao = models.DateTimeField(
        _('Data de Conclusão do Processo de Vinculação'),
        default=timezone.now,
        null=True,
        blank=True)
    aprovado = models.BooleanField(
        _('Processo aprovado'),
        default=False)
    finalizado = models.BooleanField(
        _('Processo finalizado'),
        default=False)
    valido = models.BooleanField(
        _('Processo Válido'),
        default=True)
    despacho = models.TextField(
        _('Despacho do Processo'),
        null=True,
        blank=True)

    def get_documentation_status(self):
        arquivos = ArquivosProcessoVinculacao.objects.filter(processo=self)
        return [(arquivo.id_pub, arquivo.verificado) for arquivo in arquivos]


class ArquivosProcessoVinculacao(IdPubIdentifier):
    processo = models.ForeignKey(ProcessoVinculacao, related_name='files')
    data_envio = models.DateTimeField(
        _('Data de Envio do Arquivo'), auto_now_add=True, blank=False)
    tipo = models.CharField(_('Tipo de Arquivo'), max_length=15)
    arquivo = models.FileField(upload_to=upload_doc_to)
    verificado = models.BooleanField(
        _('Arquivo verificado pelo gestor do Ministério'),
        default=False, )
    comentarios = models.TextField(
        _('Comentários sobre o arquivo'), null=True, blank=True)
    verificado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True, )

    def get_absolute_url(self):
        app_name = self._meta.app_label
        basename = self._meta.object_name.lower()
        url = app_name + ':' + basename + '-detail'

        return reverse(url, kwargs={'processo_pk': self.processo.pk, 'pk': self.pk})


class RegistroProcessoVinculacao(models.Model):
    processo = models.ForeignKey(ProcessoVinculacao, related_name='registro')
    data = models.DateField(
        _('Data do Evento'),
        default=date.today)
    situacao = models.CharField(
        _('Situacao'),
        max_length=1,
        choices=SITUACAO)
    descricao = models.TextField(
        _('Descrição'),
        blank=True,
        null=True)

    class Meta:
        ordering = ['-data']
    

@receiver(pre_save, sender=ProcessoVinculacao)
def validate_process(sender, instance, **kwargs):
    """
    Verifica se existem documentos(ArquivosProcessoVinculacao) que ainda não
    foram verificados por um administrador.
    """
    if instance.aprovado:
        if True in [
                verificado
                for (id_pub, verificado) in instance.get_documentation_status()
        ]:
            instance.full_clean()
        else:
            raise ValidationError(
                _('Existem documentos não verificados impedindo a aprovação'))


@receiver(post_save, sender=ProcessoVinculacao)
def create_praca_manager(sender, instance, **kwargs):
    """
    Cria uma nova instancia de um gestor quando um Processo de Vinculação é
    aprovado.
    """
    if instance.aprovado:
        gestor = Gestor(praca=instance.praca, user=instance.user, atual=True)
        gestor.save()
