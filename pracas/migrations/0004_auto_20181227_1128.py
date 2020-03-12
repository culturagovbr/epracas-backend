# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-12-27 11:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pracas', '0003_ativa_unaccent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ator',
            name='descricao',
            field=models.IntegerField(choices=[(0, 'não se aplica'), (1, 'artes cênicas, espetáculos e atividades complementares'), (2, 'criação artística'), (3, 'gestão de espaços para artes cênicas, espetáculos e outras atividades artísticas'), (4, 'atividades de bibliotecas e arquivos'), (5, 'atividades de museus e de exploração, restauração artística e conservação de lugares e prédios históricos e atrações similares'), (6, 'atividades de jardins botânicos, zoológicos, parques nacionais, reservas ecológicas e áreas de proteção ambiental'), (7, 'gestão de instalações de esportes'), (8, 'clubes sociais, esportivos e similares'), (9, 'atividades de condicionamento físico'), (10, 'atividades esportivas não especificadas anteriormente'), (11, 'parques de diversão e parques temáticos'), (12, 'atividades de recreação e lazer não especificadas anteriormente'), (13, 'educação infantil e ensino fundamental'), (14, 'ensino médio'), (15, 'educação superior'), (16, 'educação profissional de nível técnico e tecnológico'), (17, 'atividades de apoio à educação'), (18, 'outras atividades de ensino'), (19, 'atividades cinematográficas, produção de vídeos e de programas de televisão'), (20, 'atividades de gravação de som e de edição de música'), (21, 'atividades de televisão'), (22, 'atividades de atenção à saúde humana integradas com assistência social, prestadas em residências coletivas e particulares')], verbose_name='Descrição da Atividade do Ator'),
        ),
    ]