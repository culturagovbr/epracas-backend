from rest_framework import serializers

from localflavor.br.br_states import STATE_CHOICES
from .choices import MODELO_CHOICES, REGIOES_CHOICES, SITUACAO_CHOICES

from .models import Praca, Gestor, ProcessoAdmissao


class PracaListSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url', read_only=True)
    modelo_descricao = serializers.CharField(
            source='get_modelo_display',
            read_only=True)
    situacao_descricao = serializers.CharField(
            source='get_situacao_display',
            read_only=True)

    class Meta:
        model = Praca
        fields = (
                'url',
                'id_pub',
                'nome',
                'municipio',
                'uf',
                'modelo',
                'modelo_descricao',
                'situacao',
                'situacao_descricao'
                )


class PracaSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url', read_only=True)
    modelo_descricao = serializers.CharField(
            source='get_modelo_display',
            read_only=True)
    situacao_descricao = serializers.CharField(
            source='get_situacao_display',
            read_only=True)

    class Meta:
        model = Praca
        fields = ( 
                'url',
                'nome',
                'id_pub',
                'contrato',
                'regiao',
                'uf',
                'municipio',
                'modelo',
                'modelo_descricao',
                'situacao',
                'situacao_descricao'
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
                'gestor',
                'data_abertura',
                'aprovado',
        )

