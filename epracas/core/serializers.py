from rest_framework import serializers

from .choices import MODELO_CHOICES, REGIOES_CHOICES, SITUACAO_CHOICES

class PracaSerializer(serializers.Serializer):
    pk = serializers.UUIDField(read_only=True)
    nome = serializers.CharField(max_length=150)
    regiao = serializers.ChoiceField(REGIOES_CHOICES)
    uf = serializers.CharField(max_length=2)
    cidade = serializers.CharField(max_length=150)
    modelo = serializers.ChoiceField(MODELO_CHOICES)
    situacao = serializers.ChoiceField(SITUACAO_CHOICES)


