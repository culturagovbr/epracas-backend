# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-31 18:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('atividades', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Atividade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('descricao', models.TextField()),
                ('parceiros', models.CharField(max_length=255)),
                ('data_inicio', models.DateField()),
                ('data_termino', models.DateField()),
                ('hora_inicio', models.TimeField()),
                ('hora_termino', models.TimeField()),
                ('publico_esperado', models.IntegerField()),
                ('abrangencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='atividades.Abrangencia')),
            ],
        ),
        migrations.RenameModel(
            old_name='Espacos',
            new_name='Area',
        ),
        migrations.RenameModel(
            old_name='Tipos',
            new_name='Espaco',
        ),
        migrations.RenameModel(
            old_name='Areas',
            new_name='FaixasEtaria',
        ),
        migrations.RenameModel(
            old_name='FaixasEtarias',
            new_name='Parceiro',
        ),
        migrations.RenameModel(
            old_name='Subareas',
            new_name='Subarea',
        ),
        migrations.RenameModel(
            old_name='Parceiros',
            new_name='Tipo',
        ),
        migrations.RemoveField(
            model_name='atividades',
            name='abrangencia',
        ),
        migrations.RemoveField(
            model_name='atividades',
            name='area',
        ),
        migrations.RemoveField(
            model_name='atividades',
            name='espacos',
        ),
        migrations.RemoveField(
            model_name='atividades',
            name='faixas_etarias',
        ),
        migrations.RemoveField(
            model_name='atividades',
            name='periodicidade',
        ),
        migrations.RemoveField(
            model_name='atividades',
            name='publico',
        ),
        migrations.RemoveField(
            model_name='atividades',
            name='subarea',
        ),
        migrations.RemoveField(
            model_name='atividades',
            name='tipo',
        ),
        migrations.DeleteModel(
            name='Atividades',
        ),
        migrations.AddField(
            model_name='atividade',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='atividades.Area'),
        ),
        migrations.AddField(
            model_name='atividade',
            name='espacos',
            field=models.ManyToManyField(to='atividades.Espaco'),
        ),
        migrations.AddField(
            model_name='atividade',
            name='faixas_etarias',
            field=models.ManyToManyField(to='atividades.FaixasEtaria'),
        ),
        migrations.AddField(
            model_name='atividade',
            name='periodicidade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='atividades.Periodicidade'),
        ),
        migrations.AddField(
            model_name='atividade',
            name='publico',
            field=models.ManyToManyField(to='atividades.Publico'),
        ),
        migrations.AddField(
            model_name='atividade',
            name='subarea',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='atividades.Subarea'),
        ),
        migrations.AddField(
            model_name='atividade',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='atividades.Tipo'),
        ),
    ]
