from rest_framework import serializers

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


class ProcessoVinculacaoSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())
    files = ArquivosProcessoVinculacaoSerializer(many=True, required=False)

    class Meta:
        model = ProcessoVinculacao
        fields = ('id_pub', 'praca', 'user', 'data_abertura', 'aprovado',
                  'files', )
        read_only_fields = ('data_abertura', )
