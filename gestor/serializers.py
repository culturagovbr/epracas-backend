from rest_framework import serializers

from authentication.serializers import UserSerializer

from .models import Gestor
from .models import ProcessoVinculacao
from .models import ArquivosProcessoVinculacao


class GestorSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url', read_only=True)
    nome = serializers.CharField(source='user.full_name')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = Gestor
        fields = ('url', 'nome', 'email')


class ArquivosProcessoVinculacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArquivosProcessoVinculacao
        fields = ('id_pub', 'data_envio', 'tipo', 'verificado', 'comentarios',
                  'verificado_por', )


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
