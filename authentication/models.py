#coding: utf-8

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext as _

from core.models import IdPubIdentifier


class MyManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        user = self.model(
            email=self.normalize_email(email),
            name=kwargs.get('name')
        )

        user.set_password(password)
        user.save()

        return user


class User(AbstractBaseUser, IdPubIdentifier):
    email_verified = models.BooleanField(
        _(u'Email verificado'),
        default=False,
        )
    email = models.EmailField(
        _(u'Email'),
        blank=True,
        null=True
        )
    family_name = models.CharField(
        _(u'Sobrenome'),
        max_length=80,
        blank=True,
        null=True,
        )
    first_name = models.CharField(
        _(u'Nome'),
        max_length=80,
        blank=True,
        null=True,
        )
    full_name = models.CharField(
        _(u'Nome Completo'),
        max_length=200,
        blank=True,
        null=True,
        )
    given_name = models.CharField(
        _(u'Nome preferido'),
        max_length=80,
        blank=True,
        null=True,
        )
    name = models.CharField(
        _(u'Nome'),
        max_length=80,
        blank=True,
        null=True,
        )
    picture = models.URLField(
        _(u'Avatar'),
        blank=True,
        null=True,
        )
    profile_picture_url = models.URLField(
        _(u'URL do Avatar'),
        blank=True,
        null=True,
        )
    surname = models.CharField(
        _(u'Sobrenome'),
        max_length=80,
        blank=True,
        null=True,
        )
    sub = models.IntegerField(
        unique=True,
        blank=True,
        null=True
        )
    is_staff = models.BooleanField(
        default=False,
        )

    USERNAME_FIELD = 'sub'
    objects = MyManager()

    def __str__(self):
        return str("{} - {}").format(self.sub, self.full_name)
