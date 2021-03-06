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

    def create_superuser(self, email, password=None, **kwargs):
        user = self.model(
            email=self.normalize_email(email),
            name=kwargs.get('name'),
            is_staff=True,
        )

        user.set_password(password)
        user.save()

        return user


class User(AbstractBaseUser, IdPubIdentifier):
    email_verified = models.BooleanField(
        _('Email verificado'),
        default=False,
        )
    email = models.EmailField(
        _('Email'),
        blank=True,
        null=True
        )
    family_name = models.CharField(
        _('Sobrenome'),
        max_length=80,
        blank=True,
        null=True,
        )
    first_name = models.CharField(
        _('Nome'),
        max_length=80,
        blank=True,
        null=True,
        )
    full_name = models.CharField(
        _('Nome Completo'),
        max_length=200,
        blank=True,
        null=True,
        )
    given_name = models.CharField(
        _('Nome preferido'),
        max_length=80,
        blank=True,
        null=True,
        )
    name = models.CharField(
        _('Nome'),
        max_length=80,
        blank=True,
        null=True,
        )
    picture = models.URLField(
        _('Avatar'),
        blank=True,
        null=True,
        )
    profile_picture_url = models.URLField(
        _('URL do Avatar'),
        blank=True,
        null=True,
        )
    surname = models.CharField(
        _('Sobrenome'),
        max_length=80,
        blank=True,
        null=True,
        )
    sub = models.IntegerField(
        unique=True,
        blank=True,
        null=True
        )
    cpf = models.CharField(
        _('CPF'),
        max_length=11,
        blank=True,
        null=True,
        )
    is_staff = models.BooleanField(
        default=False,
        )

    USERNAME_FIELD = 'sub'
    objects = MyManager()

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return str("{} - {}").format(self.sub, self.full_name)

    def is_praca_manager(self):
        """
        Retorna a URL da Praça da qual este usuário é Gestor
        """
        try:
            gestor = self.gestor.get(atual=True)
            return gestor.praca.id_pub
        except:
            return None
