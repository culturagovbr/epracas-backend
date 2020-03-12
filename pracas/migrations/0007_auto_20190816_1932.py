# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-08-16 19:32
from __future__ import unicode_literals

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pracas', '0006_auto_20190816_1135'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='praca',
            name='regimento_interno',
        ),
        migrations.AddField(
            model_name='grupogestor',
            name='regimento_interno',
            field=models.FileField(blank=True, null=True, upload_to=core.models.upload_grupogestor_to, verbose_name='Regimento Interno da Praça'),
        ),
    ]
