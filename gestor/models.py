from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _

from rest_framework.serializers import ValidationError

from core.models import IdPubIdentifier
from core.models import upload_doc_to

from pracas.models import Praca

from core.choices import REGIOES_CHOICES

from rest_localflavor.br.br_states import STATE_CHOICES


class Gestor(IdPubIdentifier):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    praca = models.ForeignKey(Praca, related_name='gestor')


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
        null=True,
        blank=True)
    aprovado = models.BooleanField(
        _('Processo aprovado'),
        default=False, )
    valido = models.BooleanField(
        _('Processo Válido'),
        default=True, )

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
                _("Existem documentos não verificados impedindo a aprovação"))


@receiver(post_save, sender=ProcessoVinculacao)
def create_praca_manager(sender, instance, **kwargs):
    """
    Cria uma nova instancia de um gestor quando um Processo de Vinculação é
    aprovado.
    """
    if instance.aprovado:
        gestor = Gestor(praca=instance.praca, user=instance.user)
        gestor.save()
