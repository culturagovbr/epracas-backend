from rest_framework import serializers

from .models import GrupoGestor
from .models import Praca
from .models import Parceiro
from .models import ImagemPraca
from .models import MembroGestor
from .models import MembroUgl
from .models import Rh
from .models import Ator


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


class MembroGestorSerializer(serializers.ModelSerializer):
    origem_descricao = serializers.CharField(
        source='get_origem_display', read_only=True)

    class Meta:
        model = MembroGestor
        fields = ('id_pub', 'nome', 'origem', 'origem_descricao', 'email', 'telefone')


class MembroGestorDetailSerializer(serializers.ModelSerializer):
    origem_descricao = serializers.CharField(
        source='get_origem_display', read_only=True)
    tipo_documento_descricao = serializers.CharField(
    source='get_tipo_documento_display', read_only='True')

    class Meta:
        model = MembroGestor
        fields = ('id_pub', 'nome', 'origem', 'origem_descricao',
                  'tipo_documento', 'tipo_documento_descricao', 'data_posse',
                  'titularidade', 'email', 'telefone', 'data_desligamento',
                  'documento_posse')


class GrupoGestorSerializer(serializers.ModelSerializer):
    url = serializers.URLField(read_only=True, source='get_absolute_url')
    membros = MembroGestorSerializer(source='get_membros_ativos', read_only=True, many=True)

    class Meta:
        model = GrupoGestor
        fields = ('url', 'id_pub', 'data_instituicao', 'data_finalizacao',
                  'tipo_documento', 'documento_constituicao', 'estatuto',
                  'previsao_espacos', 'membros')


class MembroUglSerializer(serializers.ModelSerializer):
    tipo_descricao = serializers.CharField(
    source='get_tipo_display', read_only=True)
    class Meta:
        model = MembroUgl
        fields = ('id_pub', 'nome', 'tipo', 'tipo_descricao', 'telefone', 'email')


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
        source='get_modelo_display', read_only=True)
    situacao_descricao = serializers.CharField(
        source='get_situacao_display', read_only=True)
    gestor = serializers.SerializerMethodField()
    grupo_gestor = serializers.SerializerMethodField()

    def get_gestor(self, obj):
        if obj.get_manager():
            from gestor.serializers import GestorBaseSerializer
            serializer = GestorBaseSerializer(obj.get_manager())
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
        fields = ('url', 'id_pub', 'nome', 'municipio', 'uf', 'regiao',
                  'modelo', 'modelo_descricao', 'situacao',
                  'situacao_descricao', 'repasse', 'contrato', 'header_img',
                  'gestor', 'data_inauguracao')
        read_only_fields = ('url', 'gestor', 'header_img', 'id_pub')


class ParceiroBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parceiro
        fields = ('praca', 'nome', 'endereco', 'contato', 'telefone', 'email',
                  'ramo_atividade', 'acoes', 'tempo_parceria', 'imagem')


class ParceiroDetailSerializer(ParceiroBaseSerializer):
    class Meta:
        model = Parceiro
        fields = ('id_pub', 'praca', 'nome', 'endereco', 'contato', 'telefone', 'email',
                  'ramo_atividade', 'acoes', 'tempo_parceria', 'recursos_financeiros', 'imagem')


class ParceiroListSerializer(ParceiroBaseSerializer):
    class Meta:
        model = Parceiro
        fields = ('id_pub', 'nome', 'email', 'ramo_atividade', 'imagem')


class RhListSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Rh
        fields = ('url', 'id_pub', 'nome', 'funcao', 'local_trabalho',
                  'data_entrada', 'data_saida')


class RhDetailSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url', read_only=True)
    escolaridade_descricao = serializers.CharField(source='get_escolaridade_display', read_only=True)
    formacao_descricao = serializers.CharField(source='get_formacao_display', read_only=True)
    vinculo_descricao = serializers.CharField(source='get_vinculo_display', read_only=True)
    local_trabalho_descricao = serializers.CharField(source='get_local_trabalho_display', read_only=True)

    class Meta:
        model = Rh
        fields = ('url', 'id_pub', 'nome', 'identificacao', 'sexo',
                  'escolaridade', 'escolaridade_descricao', 'formacao',
                  'formacao_descricao', 'vinculo', 'vinculo_descricao',
                  'funcao', 'carga_horaria', 'remuneracao', 'local_trabalho',
                  'local_trabalho_descricao', 'data_entrada', 'data_saida',)


class AtorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ator
        fields = ('id_pub', 'nome', 'area', 'imagem')


class AtorDetailSerializer(serializers.ModelSerializer):
    area_descricao = serializers.CharField(source='get_area_display',
                                           read_only=True)
    descricao_descricao = serializers.CharField(source='get_descricao_display',
                                                read_only=True)

    class Meta:
        model = Ator
        fields = ('id_pub', 'nome', 'area', 'area_descricao', 'descricao',
                  'descricao_descricao', 'endereco', 'cep', 'telefone1', 'telefone2',
                  'email', 'lat', 'long')


class PracaSerializer(PracaBaseSerializer):
    imagem = ImagemPracaSerializer(many=True, read_only=True)
    parceiros = ParceiroDetailSerializer(many=True, read_only=True)
    unidade_gestora = MembroUglSerializer(
        source='ugl', many=True, read_only=True)
    rh = RhListSerializer(source='get_rh_ativos', many=True, read_only=True)
    atores = AtorListSerializer(many=True, read_only=True)

    class Meta:
        model = Praca
        fields = ('url', 'nome', 'slug', 'id_pub', 'contrato', 'logradouro',
                  'cep', 'bairro', 'regiao', 'uf', 'municipio', 'modelo',
                  'modelo_descricao', 'situacao', 'situacao_descricao',
                  'repasse', 'bio', 'telefone1', 'telefone2', 'fax', 'email1',
                  'email2', 'pagina', 'data_inauguracao', 'header_img', 'lat',
                  'long', 'gestor', 'unidade_gestora', 'grupo_gestor',
                  'parceiros', 'rh', 'atores', 'imagem','funciona_dia_util',
                  'hora_abertura_dia_util', 'hora_fechamento_dia_util',
                  'funciona_sabado', 'hora_abertura_sabado', 'hora_fechamento_sabado',
                  'funciona_domingo', 'hora_abertura_domingo', 'hora_fechamento_domingo')
        read_only_fields = ('id_pub', 'gestor', 'unidade_gestora',
                            'grupo_gestor', 'imagem', 'parceiros', 'atores')


class DistanciaSerializer(PracaListSerializer):
    latlong = serializers.SerializerMethodField()
    distancia = serializers.SerializerMethodField()

    def get_latlong(self, obj):
        return "{}, {}".format(obj.lat, obj.long)

    def get_distancia(self, obj):
        return obj.get_distance(self.context['origem'])

    class Meta:
        model = Praca
        fields = ('url', 'id_pub', 'nome', 'municipio', 'uf', 'modelo',
                  'modelo_descricao', 'situacao', 'situacao_descricao',
                  'header_img', 'latlong', 'distancia', )
