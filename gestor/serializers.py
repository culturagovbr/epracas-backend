from rest_framework import serializers

from authentication.serializers import UserSerializer

from pracas.serializers import PracaListSerializer

from .models import Gestor
from .models import ProcessoVinculacao
from .models import ArquivosProcessoVinculacao


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
