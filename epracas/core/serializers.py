from rest_framework import serializers

from localflavor.br.br_states import STATE_CHOICES
from .choices import MODELO_CHOICES, REGIOES_CHOICES, SITUACAO_CHOICES

from .models import Praca, Gestor, ProcessoAdmissao


class PracaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Praca
        fields = ( 
                'id_pub',
                'contrato',
                'regiao',
                'uf',
                'municipio',
                'modelo',
                'situacao'
                )


class GestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gestor
        fields = (
                'id_pub',
                'nome',
                'endereco',
                'cidade',
                'uf',
                'regiao'
        )


class ProcessoAdmissaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessoAdmissao
        fields = (
                'id_pub',
        )

