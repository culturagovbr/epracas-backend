from rest_framework import serializers

from pracas.models import Praca

from .models import Agenda
from .models import Relatorio


class RelatorioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Relatorio
        fields = (
            'realizado',
            'publico_presente',
            'pontos_positivos',
            'pontos_negativos',
        )


class AgendaSerializer(serializers.ModelSerializer):
    id_pub = serializers.UUIDField(read_only=True)
    url = serializers.URLField(source='get_absolute_url', read_only=True)
    praca_url = serializers.URLField(
            source='praca.get_absolute_url',
            read_only=True
        )
    praca = serializers.PrimaryKeyRelatedField(queryset=Praca.objects.all())
    #relatorio = RelatorioSerializer(allow_null=True, read_only=True)

    class Meta:
        model = Agenda
        fields = (
                'url',
                'id_pub',
                'praca_url',
                'praca',
                'titulo',
                'descricao',
                'justificativa',
                'tipo',
                #'area', TODO: fix models.py
                'espaco',
                #'faixa_etaria', TODO: fix models.py
                'publico',
                'carga_horaria',
                'publico_esperado',
                'data_inicio',
                'data_encerramento',
                'hora_inicio',
                'hora_encerramento',
                'local'
        )
        depth = 1

    def partial_update(self, instance, validated_data):
        relatorio = validated_data.pop('relatorio')
        Relatorio.objects.create(agenda=instance, **relatorio)

        return relatorio
