from rest_framework import serializers

from pracas.models import Praca

from .choices import ESPACOS_CHOICES
from .choices import TIPO_ATIVIDADE_CHOICES
from .choices import TERRITORIO_CHOICES

from .models import Agenda
from .models import Ocorrencia
from .models import Relatorio


class RelatorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relatorio
        fields = ('realizado', 'publico_presente', 'pontos_positivos',
                  'pontos_negativos', )


class OcorrenciaSerializer(serializers.Serializer):

    class Meta:
        model = Ocorrencia
        fields = (
            'event',
            'start',
            'end',
            'repeat',
        )


class AgendaDetailSerializer(serializers.Serializer):
    url = serializers.SerializerMethodField()
    id_pub = serializers.UUIDField(read_only=True)
    praca = serializers.PrimaryKeyRelatedField(queryset=Praca.objects.all())
    titulo = serializers.CharField()
    justificativa = serializers.CharField()
    espaco = serializers.ChoiceField(choices=ESPACOS_CHOICES)
    tipo = serializers.ChoiceField(choices=TIPO_ATIVIDADE_CHOICES)
    publico = serializers.CharField()
    carga_horaria = serializers.IntegerField()
    publico_esperado = serializers.IntegerField()
    territorio = serializers.ChoiceField(choices=TERRITORIO_CHOICES)
    descricao = serializers.CharField()
    # data_inicio = serializers.DateField()
    # data_encerramento = serializers.DateField()
    # repeat = serializers.CharField()

    def get_url(self, obj):
        return obj.get_absolute_url()

    def create(self, validated_data):
        praca = Praca.objects.get(id_pub=validated_data['praca'])
        agenda = Agenda(
            praca=praca,
            titulo=validated_data['titulo'],
            justificativa=validated_data['justificativa'],
            espaco=validated_data['espaco'],
            tipo=validated_data['tipo'],
            publico=validated_data['publico'],
            carga_horaria=validated_data['carga_horaria'],
            publico_esperado=validated_data['publico_esperado'],
            territorio=validated_data['territorio'],
            descricao=validated_data['descricao'])
        agenda.save()

        ocorrencia = Ocorrencia(
            event=agenda,
            start=validated_data['data_inicio'],
            end=validated_data['data_encerramento'])
        ocorrencia.save()

        return agenda
