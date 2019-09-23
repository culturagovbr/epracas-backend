# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-04-03 16:00
from __future__ import unicode_literals

import core.models
import datetime
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import pracas.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ator',
            fields=[
                ('id_pub', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID Público')),
                ('nome', models.CharField(max_length=350, verbose_name='Nome do Ator')),
                ('area', models.CharField(choices=[('asso', 'Assistencia Social'), ('cmrc', 'Comércio, Serviço e Produção'), ('comu', 'Comunidade'), ('cult', 'Cultura'), ('ens', 'Ensino e Pesquisa'), ('espt', 'Esporte'), ('saud', 'Saúde'), ('com', 'Veículos de Comunicação Local'), ('otr', 'Outros')], max_length=4, verbose_name='Área de Atuação')),
                ('descricao', models.IntegerField(choices=[(1, 'artes cênicas, espetáculos e atividades complementares'), (2, 'criação artística'), (3, 'gestão de espaços para artes cênicas, espetáculos e outras atividades artísticas'), (4, 'atividades de bibliotecas e arquivos'), (5, 'atividades de museus e de exploração, restauração artística e conservação de lugares e prédios históricos e atrações similares'), (6, 'atividades de jardins botânicos, zoológicos, parques nacionais, reservas ecológicas e áreas de proteção ambiental'), (7, 'gestão de instalações de esportes'), (8, 'clubes sociais, esportivos e similares'), (9, 'atividades de condicionamento físico'), (10, 'atividades esportivas não especificadas anteriormente'), (11, 'parques de diversão e parques temáticos'), (12, 'atividades de recreação e lazer não especificadas anteriormente'), (13, 'educação infantil e ensino fundamental'), (14, 'ensino médio'), (15, 'educação superior'), (16, 'educação profissional de nível técnico e tecnológico'), (17, 'atividades de apoio à educação'), (18, 'outras atividades de ensino'), (19, 'atividades cinematográficas, produção de vídeos e de programas de televisão'), (20, 'atividades de gravação de som e de edição de música'), (21, 'atividades de televisão'), (22, 'atividades de atenção à saúde humana integradas com assistência social, prestadas em residências coletivas e particulares')], verbose_name='Descrição da Atividade do Ator')),
                ('imagem', models.FileField(blank=True, upload_to=pracas.models.upload_image_to)),
                ('endereco', models.TextField(blank=True, null=True, verbose_name='Endereço')),
                ('cep', models.CharField(blank=True, max_length=9, null=True, verbose_name='CEP')),
                ('telefone1', models.CharField(blank=True, max_length=15, null=True, verbose_name='Telefone de Contato')),
                ('telefone2', models.CharField(blank=True, max_length=15, null=True, verbose_name='Telefone de Contato')),
                ('email', models.CharField(blank=True, max_length=200, null=True, verbose_name='Email de Contato')),
                ('lat', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Latitude')),
                ('long', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Longitutde')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GrupoGestor',
            fields=[
                ('id_pub', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID Público')),
                ('previsao_espacos', models.IntegerField(max_length=2, verbose_name='Qtde de membros previstos no Grupo Gestor')),
                ('data_instituicao', models.DateField(default=django.utils.timezone.now, verbose_name='Data de Instituição do Grupo Gestor')),
                ('data_finalizacao', models.DateField(blank=True, null=True, verbose_name='Data de Finalização do Grupo Gestor')),
                ('documento_constituicao', models.FileField(blank=True, null=True, upload_to=core.models.upload_grupogestor_to, verbose_name='Documento de Constituição do Grupo Gestor')),
                ('estatuto', models.FileField(blank=True, null=True, upload_to=core.models.upload_grupogestor_to, verbose_name='Estatuto do Grupo Gestor')),
                ('tipo_documento', models.CharField(blank=True, choices=[('d', 'Decreto'), ('p', 'Portaria'), ('l', 'Lei'), ('n', 'Não Formalizado')], max_length=1, null=True, verbose_name='Tipo de documento de constituição')),
            ],
            options={
                'ordering': ['-data_instituicao'],
            },
        ),
        migrations.CreateModel(
            name='ImagemPraca',
            fields=[
                ('id_pub', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID Público')),
                ('arquivo', models.FileField(blank=True, upload_to=pracas.models.upload_image_to)),
                ('header', models.BooleanField(default=False)),
                ('titulo', models.CharField(blank=True, max_length=140, null=True)),
                ('descricao', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MembroGestor',
            fields=[
                ('id_pub', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID Público')),
                ('nome', models.CharField(max_length=120, verbose_name='Nome do Gestor')),
                ('origem', models.CharField(choices=[('pp', 'Poder Publico'), ('sc', 'Sociedade Civil'), ('me', 'Moradores do Entorno')], max_length=2, verbose_name='Origem do Membro')),
                ('data_posse', models.DateField(default=datetime.date.today, verbose_name='Data de Posse do Membro Gestor')),
                ('data_desligamento', models.DateField(blank=True, null=True, verbose_name='Data de Desligamento do Membro Gestor')),
                ('documento_posse', models.FileField(blank=True, null=True, upload_to=core.models.upload_grupogestor_to, verbose_name='Documento de Posse do Membro Gestor')),
                ('tipo_documento', models.CharField(blank=True, choices=[('d', 'Decreto'), ('p', 'Portaria'), ('l', 'Lei'), ('n', 'Não Formalizado')], max_length=1, null=True, verbose_name='Tipo de documento de posse')),
                ('titularidade', models.CharField(choices=[('t', 'Titular'), ('s', 'Suplente')], default='s', max_length=1, verbose_name='Titularidade')),
                ('email', models.CharField(blank=True, max_length=200, null=True, verbose_name='Email de Contato')),
                ('telefone', models.CharField(blank=True, max_length=15, null=True, verbose_name='Telefone de Contato')),
                ('grupo_gestor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='membros', to='pracas.GrupoGestor')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MembroUgl',
            fields=[
                ('id_pub', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID Público')),
                ('nome', models.CharField(max_length=250, verbose_name='Nome do Membro')),
                ('tipo', models.CharField(choices=[('cg', 'Coordenador Geral'), ('ce', 'Coordenador de Engenharia (responsável pela obra)'), ('cc', 'Coordenador de Cultura'), ('ces', 'Coordenador de Esporte'), ('cas', 'Coordenador de Assistência Social'), ('cds', 'Coordenador de Desenvolvimento Econômico'), ('csc', 'Coordenador de Segurança Cidadã'), ('cid', 'Coordenador de Inclusão Digital')], default='cg', max_length=3, verbose_name='Tipo de Membro')),
                ('telefone', models.CharField(blank=True, max_length=15, null=True, verbose_name='Telefone de Contato')),
                ('email', models.CharField(blank=True, max_length=200, null=True, verbose_name='Email de Contato')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Parceiro',
            fields=[
                ('id_pub', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID Público')),
                ('nome', models.CharField(max_length=300, verbose_name='Nome Institucional do Parceiro')),
                ('endereco', models.TextField(verbose_name='Endereço')),
                ('contato', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nome do Contato')),
                ('telefone', models.CharField(blank=True, max_length=15, null=True, verbose_name='Telefone de Contato')),
                ('email', models.CharField(blank=True, max_length=200, null=True, verbose_name='Email de Contato')),
                ('ramo_atividade', models.IntegerField(choices=[(1, 'agricultura, pecuária, produção florestal, pesca e aqüicultura'), (2, 'indústrias extrativas'), (3, 'indústrias de transformação'), (4, 'eletricidade e gás'), (5, 'água, esgoto, atividades de gestão de resíduos e descontaminação'), (6, 'construção'), (7, 'comércio; reparação de veículos automotores e motocicletas'), (8, 'transporte, armazenagem e correio'), (9, 'alojamento e alimentação'), (10, 'informação e comunicação'), (11, 'atividades financeiras, de seguros e serviços relacionados'), (12, 'atividades imobiliárias'), (13, 'atividades profissionais, científicas e técnicas'), (14, 'atividades administrativas e serviços complementares'), (15, 'administração pública, defesa e seguridade social'), (16, 'educação'), (17, 'saúde humana e serviços sociais'), (18, 'artes, cultura, esporte e recreação'), (19, 'outras atividades de serviços'), (20, 'serviços domésticos'), (21, 'organismos internacionais e outras instituições extraterritoriais')], verbose_name='Ramo de Atividade')),
                ('acoes', models.TextField(blank=True, null=True, verbose_name='Açoes realizadas em parceria')),
                ('tempo_parceria', models.IntegerField(blank=False, null=False, verbose_name='Tempo previsto para a parceria')),
                ('recursos_financeiros', models.DecimalField(decimal_places=2, max_digits=12, null=True, verbose_name='Recursos Financeiros')),
                ('lat', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Latitude')),
                ('long', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Longitutde')),
                ('imagem', models.FileField(blank=True, upload_to=pracas.models.upload_image_to)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Praca',
            fields=[
                ('id_pub', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID Público')),
                ('nome', models.CharField(blank=True, max_length=250, verbose_name='Nome da Praça')),
                ('slug', models.SlugField(blank=True, max_length=250, verbose_name='Nome Publico')),
                ('contrato', models.IntegerField(verbose_name='Nº de Contrato')),
                ('logradouro', models.CharField(blank=True, max_length=200, null=True, verbose_name='Logradouro')),
                ('cep', models.IntegerField(blank=True, null=True, verbose_name='CEP')),
                ('bairro', models.CharField(blank=True, max_length=100, null=True, verbose_name='Bairro')),
                ('regiao', models.CharField(choices=[('N', 'Norte'), ('NE', 'Nordeste'), ('CO', 'Centro-Oeste'), ('SE', 'Sudeste'), ('S', 'Sul')], max_length=2, verbose_name='Região')),
                ('uf', models.CharField(choices=[('ac', 'Acre'), ('al', 'Alagoas'), ('ap', 'Amapá'), ('am', 'Amazonas'), ('ba', 'Bahia'), ('ce', 'Ceará'), ('df', 'Distrito Federal'), ('es', 'Espírito Santo'), ('go', 'Goiás'), ('ma', 'Maranhão'), ('mt', 'Mato Grosso'), ('ms', 'Mato Grosso do Sul'), ('mg', 'Minas Gerais'), ('pa', 'Pará'), ('pb', 'Paraíba'), ('pr', 'Paraná'), ('pe', 'Pernambuco'), ('pi', 'Piauí'), ('rj', 'Rio de Janeiro'), ('rn', 'Rio Grande do Norte'), ('rs', 'Rio Grande do Sul'), ('ro', 'Rondônia'), ('rr', 'Roraima'), ('sc', 'Santa Catarina'), ('sp', 'São Paulo'), ('se', 'Sergipe'), ('to', 'Tocantins')], max_length=2, verbose_name='UF')),
                ('municipio', models.CharField(max_length=140, verbose_name='Municipio')),
                ('modelo', models.CharField(choices=[('p', '700m2'), ('m', '3000m2'), ('g', '7000m2')], max_length=1, verbose_name='Modelo de Praça')),
                ('situacao', models.CharField(choices=[('c', 'Obras Concluidas'), ('a', 'Obras em Andamento'), ('i', 'Inaugurada')], max_length=1, verbose_name='Situação')),
                ('data_inauguracao', models.DateField(blank=True, null=True, verbose_name='Data de Inauguração')),
                ('lat', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Latitude')),
                ('long', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Longitutde')),
                ('bio', models.TextField(blank=True, null=True, verbose_name='Descrição/Biografia da Praça')),
                ('header_img', models.FileField(blank=True, upload_to=pracas.models.upload_image_to)),
                ('repasse', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Repasses do Ministério')),
                ('telefone1', models.CharField(blank=True, max_length=15, null=True, verbose_name='Telefone de Contato')),
                ('telefone2', models.CharField(blank=True, max_length=15, null=True, verbose_name='Telefone de Contato')),
                ('fax', models.CharField(blank=True, max_length=15, null=True, verbose_name='Fax')),
                ('email1', models.CharField(blank=True, max_length=200, null=True, verbose_name='Primeiro Email de Contato')),
                ('email2', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Segundo Email de Contato')),
                ('pagina', models.URLField(blank=True, null=True, verbose_name='Pagina do CEU nas redes sociais')),
                ('funciona_dia_util', models.NullBooleanField(verbose_name='Segunda - Sexta')),
                ('hora_abertura_dia_util', models.TimeField(blank=True, null=True, verbose_name='Abre')),
                ('hora_fechamento_dia_util', models.TimeField(blank=True, null=True, verbose_name='Fecha')),
                ('funciona_sabado', models.NullBooleanField(verbose_name='Sábado')),
                ('hora_abertura_sabado', models.TimeField(blank=True, null=True, verbose_name='Abre')),
                ('hora_fechamento_sabado', models.TimeField(blank=True, null=True, verbose_name='Fecha')),
                ('funciona_domingo', models.NullBooleanField(verbose_name='Domingo')),
                ('hora_abertura_domingo', models.TimeField(blank=True, null=True, verbose_name='Abre')),
                ('hora_fechamento_domingo', models.TimeField(blank=True, null=True, verbose_name='Fecha')),
            ],
            options={
                'verbose_name': 'praca',
                'verbose_name_plural': 'pracas',
                'ordering': ['uf', 'municipio'],
            },
        ),
        migrations.CreateModel(
            name='Rh',
            fields=[
                ('id_pub', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID Público')),
                ('nome', models.CharField(max_length=300, verbose_name='Nome')),
                ('identificacao', models.CharField(blank=True, max_length=30, null=True, verbose_name='Documento Identidade')),
                ('sexo', models.CharField(blank=True, choices=[('f', 'Feminino'), ('m', 'Masculino')], max_length=1, null=True, verbose_name='Sexo')),
                ('escolaridade', models.CharField(blank=True, choices=[('se', 'Sem Escolaridade'), ('efi', 'Ensino Fundamental Incompleto'), ('efc', 'Ensino Fundamental Completo'), ('emi', 'Ensino Médio Incompleto'), ('emc', 'Ensino Médio Completo'), ('eti', 'Ensino Técnico Incompleto'), ('etc', 'Ensino Técnico Completo'), ('esi', 'Ensino Superior Incompleto'), ('esc', 'Ensino Superior Completo'), ('esp', 'Especialização'), ('mes', 'Mestrado'), ('doc', 'Doutorado')], max_length=3, null=True, verbose_name='Escolaridade')),
                ('formacao', models.CharField(blank=True, choices=[('bib', 'Biblioteconomia'), ('edf', 'Educação física'), ('ss', 'Serviço Social'), ('psi', 'Psicologia'), ('ped', 'Pedagogia'), ('son', 'Sonoplastia e iluminação'), ('aud', 'Audiovisual'), ('otr', 'Outros')], max_length=3, null=True, verbose_name='Formação')),
                ('vinculo', models.CharField(blank=True, choices=[('se', 'Servidor Estatutário'), ('st', 'Servidor Temporário'), ('ep', 'Empregado Público (CLT)'), ('com', 'Comissionado'), ('ter', 'Terceirizado'), ('coo', 'Trabalhador de Empresa , Cooperativa ou Entidade Prestadora de Serviços'), ('vol', 'Voluntário'), ('otr', 'Outro vínculo não permanente')], max_length=3, null=True, verbose_name='Tipo de vínculo')),
                ('funcao', models.CharField(blank=True, max_length=200, null=True, verbose_name='Função')),
                ('carga_horaria', models.CharField(blank=True, max_length=3, null=True, verbose_name='Carga Horaria')),
                ('remuneracao', models.DecimalField(blank=True, decimal_places=2, max_digits=10, max_length=10, null=True, verbose_name='Remuneração Mensal')),
                ('local_trabalho', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, choices=[(1, 'Cineteatro'), (2, 'Biblioteca'), (3, 'Laboratório Multimídia'), (4, 'Quadra'), (5, 'Sala Multiuso'), (6, 'CRAS'), (7, 'Pista de Skate'), (8, 'Areas Externas')], null=True, verbose_name='Local de Trabalho no CEU'), default=list, size=None)),
                ('data_entrada', models.DateField(default=datetime.date.today, verbose_name='Data de Entrada')),
                ('data_saida', models.DateField(blank=True, null=True, verbose_name='Data de Saída')),
                ('praca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rh', to='pracas.Praca')),
            ],
            options={
                'ordering': ['nome', 'data_entrada'],
            },
        ),
        migrations.AddField(
            model_name='parceiro',
            name='praca',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parceiros', to='pracas.Praca'),
        ),
        migrations.AddField(
            model_name='membrougl',
            name='praca',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ugl', to='pracas.Praca'),
        ),
        migrations.AddField(
            model_name='imagempraca',
            name='praca',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagem', to='pracas.Praca'),
        ),
        migrations.AddField(
            model_name='grupogestor',
            name='praca',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grupo_gestor', to='pracas.Praca'),
        ),
        migrations.AddField(
            model_name='ator',
            name='praca',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='atores', to='pracas.Praca'),
        ),
    ]
