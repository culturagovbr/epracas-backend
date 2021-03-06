# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-04-03 16:00
from __future__ import unicode_literals

import core.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pracas', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArquivosProcessoVinculacao',
            fields=[
                ('id_pub', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID Público')),
                ('data_envio', models.DateTimeField(auto_now_add=True, verbose_name='Data de Envio do Arquivo')),
                ('tipo', models.CharField(max_length=15, verbose_name='Tipo de Arquivo')),
                ('arquivo', models.FileField(upload_to=core.models.upload_doc_to)),
                ('verificado', models.BooleanField(default=False, verbose_name='Arquivo verificado pelo gestor do Ministério')),
                ('comentarios', models.TextField(blank=True, null=True, verbose_name='Comentários sobre o arquivo')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Gestor',
            fields=[
                ('id_pub', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID Público')),
                ('atual', models.BooleanField(default=False, verbose_name='Gestor Atual')),
                ('data_inicio_gestao', models.DateField(default=django.utils.timezone.now, verbose_name='Data de Inicio da Gestão')),
                ('data_encerramento_gestao', models.DateField(null=True, verbose_name='Data de Encerramento da Gestão')),
                ('praca', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gestor', to='pracas.Praca')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gestor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProcessoVinculacao',
            fields=[
                ('id_pub', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID Público')),
                ('data_abertura', models.DateField(auto_now_add=True, verbose_name='Data de Abertura do Processo')),
                ('data_finalizacao', models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Data de Conclusão do Processo de Vinculação')),
                ('aprovado', models.BooleanField(default=False, verbose_name='Processo aprovado')),
                ('finalizado', models.BooleanField(default=False, verbose_name='Processo finalizado')),
                ('despacho', models.TextField(blank=True, null=True, verbose_name='Despacho do Processo')),
                ('praca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pracas.Praca')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegistroProcessoVinculacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(default=datetime.date.today, verbose_name='Data do Evento')),
                ('situacao', models.CharField(choices=[('c', 'Cancelado'), ('p', 'Pendente'), ('a', 'Aprovado')], max_length=1, verbose_name='Situacao')),
                ('descricao', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                ('processo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registro', to='gestor.ProcessoVinculacao')),
            ],
            options={
                'ordering': ['-data'],
            },
        ),
        migrations.AddField(
            model_name='arquivosprocessovinculacao',
            name='processo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='gestor.ProcessoVinculacao'),
        ),
        migrations.AddField(
            model_name='arquivosprocessovinculacao',
            name='verificado_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
