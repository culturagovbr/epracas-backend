from django.conf import settings

from rest_framework import serializers

from .models import GrupoGestor
from .models import Praca
from .models import Parceiro
from .models import ImagemPraca
from .models import MembroGestor


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class GrupoGestorSerializer(serializers.ModelSerializer):

    class Meta:
        model = GrupoGestor
        fields = '__all__'
        read_only_fields = ('praca',)


class MembroGestorSerializer(serializers.ModelSerializer):

    class Meta:
        model = MembroGestor
        fields = ('nome', 'origem')


class ImagemPracaSerializer(serializers.ModelSerializer):
    praca = serializers.PrimaryKeyRelatedField(required=False, read_only=True)
    url = serializers.URLField(source='get_absolute_url', read_only=True)
    header = serializers.BooleanField(default=False)
    titulo = serializers.CharField(default=' ')

    class Meta:
        model = ImagemPraca
        fields = ('url', 'id_pub', 'praca', 'arquivo', 'header', 'titulo',
                  'descricao')


class PracaBaseSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url', read_only=True)
    modelo_descricao = serializers.CharField(
            source='get_modelo_display',
            read_only=True)
    situacao_descricao = serializers.CharField(
            source='get_situacao_display',
            read_only=True)
    gestor = serializers.SerializerMethodField()
    grupo_gestor = serializers.SerializerMethodField()

    def get_gestor(self, obj):
        if obj.get_manager():
            from gestor.serializers import GestorSerializer
            serializer = GestorSerializer(obj.get_manager())
            return serializer.data
        else:
            return None

    def get_grupo_gestor(self, obj):
        if obj.get_grupogestor():
            serializer = GrupoGestorSerializer(obj.get_grupogestor())
            return serializer.data
        else:
            return None


class PracaListSerializer(PracaBaseSerializer, DynamicFieldsModelSerializer):

    class Meta:
        model = Praca
        fields = (
                'url',
                'id_pub',
                'nome',
                'municipio',
                'uf',
                'regiao',
                'modelo',
                'modelo_descricao',
                'situacao',
                'situacao_descricao',
                'header_img',
                'gestor',
                )
        read_only_fields = ('url', 'gestor', 'header_img')


class ParceiroBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parceiro
        fields = (
            'praca',
            'nome',
            'endereco',
            'contato',
            'telefone',
            'email',
            'ramo_atividade',
            'acoes',
            'tempo_parceria'
        )


class ParceiroDetailSerializer(ParceiroBaseSerializer):

    class Meta:
        model = Parceiro
        fields = (
            'praca',
            'nome',
            'endereco',
            'contato',
            'telefone',
            'email',
            'ramo_atividade',
            'acoes',
            'tempo_parceria',
            'lat',
            'long',
            'recursos_financeiros',
        )


class ParceiroListSerializer(ParceiroBaseSerializer):

    class Meta:
        model = Parceiro
        fields = (
            'nome',
            'email',
            'ramo_atividade',
        )


class PracaSerializer(PracaBaseSerializer):
    imagem = ImagemPracaSerializer(many=True, read_only=True)
    parceiros = ParceiroListSerializer(many=True, read_only=True)

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
                'header_img',
                'lat',
                'long',
                'gestor',
                'grupo_gestor',
                'parceiros',
                'imagem',
                )
        read_only_fields = ('gestor', 'grupo_gestor', 'imagem', 'parceiros')


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
                'header_img',
                'latlong',
                'distancia',
        )
