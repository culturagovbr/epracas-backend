import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from rest_framework.reverse import reverse
from localflavor.br.br_states import STATE_CHOICES

from .choices import REGIOES_CHOICES

# from pracas.models import Praca


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


# class ProcessoVinculacao(IdPubIdentifier):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL)
#     praca = models.ForeignKey(Praca)
#     data_abertura = models.DateTimeField(
#         _('Data de Abertura do Processo'),
#         auto_now_add=True,
#         editable=False,
#         blank=False
#         )
#     data_finalizacao = models.DateTimeField(
#         _('Data de Conclusão do Processo de Vinculação'),
#         null=True,
#         blank=True
#         )
#     aprovado = models.BooleanField(
#         _('Processo aprovado'),
#         default=False,
#         )
#     valido = models.BooleanField(
#         _('Processo Válido'),
#         default=True,
#         )


# class ArquivosProcessoVinculacao(IdPubIdentifier):
#     processo = models.ForeignKey(ProcessoVinculacao, related_name='files')
#     data_envio = models.DateTimeField(
#         _('Data de Envio do Arquivo'),
#         auto_now_add=True,
#         blank=False
#         )
#     tipo = models.CharField(
#         _('Tipo de Arquivo'),
#         max_length=8
#         )
#     arquivo = models.FileField(upload_to=upload_doc_to)
#     verificado = models.BooleanField(
#         _('Arquivo verificado pelo gestor do Ministério'),
#         default=False,
#         )
#     comentarios = models.TextField(
#         _('Comentários sobre o arquivo'),
#         null=True,
#         blank=True
#         )
#     verificado_por = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         null=True,
#         blank=True,
#         )
