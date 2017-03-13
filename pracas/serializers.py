from django.conf import settings

from rest_framework import serializers

from .models import GrupoGestor
from .models import Praca
from .models import Parceiro


class GrupoGestorSerializer(serializers.ModelSerializer):

    class Meta:
        model = GrupoGestor
        fields = '__all__'


class HeaderUploadSerializer(serializers.Serializer):
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


class PracaBaseSerializer(serializers.ModelSerializer, HeaderUploadSerializer):
    url = serializers.URLField(source='get_absolute_url', read_only=True)
    modelo_descricao = serializers.CharField(
            source='get_modelo_display',
            read_only=True)
    situacao_descricao = serializers.CharField(
            source='get_situacao_display',
            read_only=True)
    gestor = serializers.SerializerMethodField()
    grupo_gestor = GrupoGestorSerializer(read_only=True)

    def get_gestor(self, obj):
        if obj.get_manager():
            from gestor.serializers import GestorSerializer
            serializer = GestorSerializer(obj.get_manager())
            return serializer.data
        else:
            return None


class PracaListSerializer(PracaBaseSerializer):

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
                'header_url',
                'gestor',
                )
        read_only_fields = ('gestor',)


class PracaSerializer(PracaBaseSerializer):

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
                'modelo',
                'modelo_descricao',
                'situacao',
                'situacao_descricao',
                'header_url',
                'lat',
                'long',
                'gestor',
                'grupo_gestor',
                )
        read_only_fields = ('gestor', 'grupo_gestor')


class ParceiroSerialier(serializers.ModelSerializer):

    class Meta:
        model = Parceiro
        fields = (
            'nome',
            'endereco',
            'contato',
            'telefone',
            'email',
            'ramo_atividade',
            'acoes',
            'tempo_parceria'
        )


class DistanciaSerializer(PracaListSerializer):
    latlong = serializers.SerializerMethodField()
    distancia = serializers.SerializerMethodField()

    def get_latlong(self, obj):
        return "{}, {}".format(obj.lat, obj.long)

    def get_distancia(self, obj):
        return obj.get_distance(self.context['origem'])

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
                'header_url',
                'latlong',
                'distancia',
        )
