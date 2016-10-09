from django.conf import settings
from rest_framework import serializers

from localflavor.br.br_states import STATE_CHOICES
from .choices import MODELO_CHOICES, REGIOES_CHOICES, SITUACAO_CHOICES

from .models import Praca, Gestor, Agenda, ProcessoVinculacao


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
    header_url = serializers.SerializerMethodField()

    def get_header_url(self, obj):
        request = self.context.get('request')
        is_secure = request.is_secure()
        host = request.get_host()
        media_url = settings.MEDIA_URL
        path = obj.header_img
        if path:
            if is_secure:
                return "https://{}{}{}".format(host, media_url, path)
            else:
                return "http://{}{}{}".format(host, media_url, path)
        return ""


    class Meta:
        model = Praca
        fields = ( 
                'url',
                'nome',
                'slug',
                'id_pub',
                'contrato',
                'regiao',
                'uf',
                'municipio',
                'modelo',
                'modelo_descricao',
                'situacao',
                'situacao_descricao',
                'header_url'
                )


class PracaUploadSerializer(serializers.ModelSerializer):
    header_url = serializers.SerializerMethodField()

    def get_header_url(self, obj):
        request = self.context.get('request')
        is_secure = request.is_secure()
        host = request.get_host()
        media_url = settings.MEDIA_URL
        path = obj.header_img
        if is_secure:
            return "https://{}{}{}".format(host, media_url, path)
        else:
            return "http://{}{}{}".format(host, media_url, path)

    class Meta:
        model = Praca
        fields = ('id_pub', 'header_img', 'header_url')



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


class ProcessoVinculacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessoVinculacao
        fields = (
                'id_pub',
                'gestor',
                'data_abertura',
                'aprovado',
        )

