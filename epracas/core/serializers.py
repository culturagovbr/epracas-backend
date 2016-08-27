from rest_framework import serializers

from localflavor.br.br_states import STATE_CHOICES
from .choices import MODELO_CHOICES, REGIOES_CHOICES, SITUACAO_CHOICES

class PracaSerializer(serializers.Serializer):
    id_pub = serializers.UUIDField(read_only=True)
    regiao = serializers.ChoiceField(REGIOES_CHOICES)
    uf = serializers.ChoiceField(STATE_CHOICES)
    municipio = serializers.CharField(max_length=150)
    modelo = serializers.ChoiceField(MODELO_CHOICES)
    situacao = serializers.ChoiceField(SITUACAO_CHOICES)


