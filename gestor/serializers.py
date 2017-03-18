from rest_framework import serializers

from authentication.serializers import UserSerializer

from .models import Gestor
from .models import ProcessoVinculacao
from .models import ArquivosProcessoVinculacao


class GestorSerializer(serializers.ModelSerializer):

    url = serializers.URLField(source='get_absolute_url', read_only=True)
    nome = serializers.CharField(source='user.full_name')
    email = serializers.EmailField(source='user.email')
    user_id_pub = serializers.CharField(source='user.id_pub')
    praca = serializers.SerializerMethodField()

    def get_praca(self, obj):
        from pracas.serializers import PracaListSerializer
        serializer = PracaListSerializer(
            obj.praca, fields=('nome', 'url', 'municipio', 'uf', 'regiao'))
        return serializer.data

    class Meta:
        model = Gestor
        fields = ('url', 'user_id_pub', 'nome', 'email', 'praca')


class ArquivosProcessoVinculacaoSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = ArquivosProcessoVinculacao
        fields = ('url', 'id_pub', 'data_envio', 'tipo', 'verificado',
                  'comentarios', 'verificado_por', 'arquivo')


class ProcessoVinculacaoListSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url', read_only=True)
    concluido = serializers.BooleanField(source='aprovado', read_only=True)
    praca = serializers.SerializerMethodField(read_only=True)
    user = UserSerializer(read_only=True)

    def get_praca(self, obj):
        from pracas.serializers import PracaListSerializer
        serializer = PracaListSerializer(obj.praca)
        return serializer.data

    class Meta:
        model = ProcessoVinculacao
        fields = ('url', 'id_pub', 'praca', 'user', 'data_abertura',
                  'concluido', )


class ProcessoVinculacaoDetailSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url', read_only=True)
    praca = serializers.SerializerMethodField(read_only=True)
    user = UserSerializer(read_only=True)
    files = ArquivosProcessoVinculacaoSerializer(many=True)

    def get_praca(self, obj):
        from pracas.serializers import PracaListSerializer
        serializer = PracaListSerializer(obj.praca)
        return serializer.data

    class Meta:
        model = ProcessoVinculacao
        fields = ('url', 'id_pub', 'praca', 'user', 'data_abertura',
                  'aprovado', 'files')


class ProcessoVinculacaoSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url', read_only=True)
    user = UserSerializer(
        read_only=True, default=serializers.CurrentUserDefault())
    files = ArquivosProcessoVinculacaoSerializer(many=True, required=False)

    class Meta:
        model = ProcessoVinculacao
        fields = ('url', 'id_pub', 'praca', 'user', 'data_abertura',
                  'aprovado', 'files', )
        read_only_fields = ('data_abertura', )
