import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from rest_framework.reverse import reverse
from rest_localflavor.br.br_states import STATE_CHOICES

from .choices import REGIOES_CHOICES


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
    return f'{id_pub}/images/header.{ext}'


def upload_doc_to(instance, filename):
    ext = slugify(filename.split('.').pop(-1))
    new_name = slugify(filename.rsplit('.', 1)[0])
    id_pub = instance.processo.praca.id_pub
    basename = instance.processo._meta.object_name.lower()
    return f'{id_pub}/docs/{basename}/{new_name}.{ext}'


def upload_grupogestor_to(instance, filename):
    ext = slugify(filename.split('.').pop(-1))
    new_name = slugify(filename.rsplit('.', 1)[0])
    id_pub = instance.praca.id_pub
    basename = instance._meta.object_name.lower()
    return f'{id_pub}/docs/{basename}/{new_name}.{ext}'
