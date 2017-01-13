#coding: utf-8
import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from rest_framework.reverse import reverse
from rest_localflavor.br.br_states import STATE_CHOICES

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
