from django.conf import settings

from rest_framework import serializers

from .models import Praca
from .models import Gestor
from .models import Agenda
from .models import ProcessoVinculacao
from .models import ArquivosProcessoVinculacao

from authentication.serializers import UserSerializer


class PracaListSerializer(serializers.ModelSerializer):
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
                'id_pub',
                'nome',
                'municipio',
                'uf',
                'modelo',
                'modelo_descricao',
                'situacao',
                'situacao_descricao',
                'header_url'
                )


class AgendaSerializer(serializers.ModelSerializer):
    id_pub = serializers.UUIDField(read_only=True)
    url = serializers.URLField(source='get_absolute_url', read_only=True)
    praca_url = serializers.URLField(
            source='praca.get_absolute_url',
            read_only=True
        )
    praca = serializers.PrimaryKeyRelatedField(queryset=Praca.objects.all())

    # def create(self, validated_data):
    #     praca_id = validated_data.pop('praca')
    #     praca = Praca.objects.get(id_pub=praca_id)
        
    #     evento = Agenda(praca=praca, **validated_data)
    #     serializer = AgendaSerializer(evento).is_valid()
    #     return serializer.data


    class Meta:
        model = Agenda
        fields = (
                'url',
                'id_pub',
                'praca_url',
                'praca',
                'titulo',
                'data_inicio',
                'data_encerramento',
                'hora_inicio',
                'hora_encerramento',
                'descricao',
                'local'
        )
        depth = 1


class PracaSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url', read_only=True)
    modelo_descricao = serializers.CharField(
            source='get_modelo_display',
            read_only=True)
    situacao_descricao = serializers.CharField(
            source='get_situacao_display',
            read_only=True)
    header_url = serializers.SerializerMethodField()
    agenda = AgendaSerializer(many=True, read_only=True)

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
                'logradouro',
                'cep',
                'bairro',
                'regiao',
                'uf',
                'municipio',
                'agenda',
                'modelo',
                'modelo_descricao',
                'situacao',
                'situacao_descricao',
                'header_url',
                'lat',
                'long',
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


class ArquivosProcessoVinculacaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArquivosProcessoVinculacao
        fields = (
            'id_pub',
            'data_envio',
            'tipo',
            'verificado',
            'comentarios',
            'verificado_por',
        )


class ProcessoVinculacaoSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    praca = PracaListSerializer()
    files = ArquivosProcessoVinculacaoSerializer(many=True)

    class Meta:
        model = ProcessoVinculacao
        fields = (
                'id_pub',
                'user',
                'praca',
                'data_abertura',
                'aprovado',
                'files',
        )
