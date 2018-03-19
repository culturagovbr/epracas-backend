from rest_framework import serializers

from pracas.serializers import PracaListSerializer
from .models import Agenda
from .models import Ocorrencia
from .models import Relatorio
from .models import RelatorioImagem

from .choices import ESPACOS_CHOICES


class RelatorioImagemSerializer(serializers.ModelSerializer):

    class Meta:
        model = RelatorioImagem
        fields = '__all__'


class RelatorioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Relatorio
        fields = (
            'realizado',
            'publico_presente',
            'pontos_positivos',
            'pontos_negativos',
            'data_prevista',
            'data_de_ocorrencia',
        )


class OcorrenciaSerializer(serializers.ModelSerializer):
    calendar = serializers.SerializerMethodField()

    def get_calendar(self, obj):
        if obj.frequency_type == "daily":
            generator = obj.all_occurrences()
            return [date for (date, end_date, occ) in generator]
        else:
            return None

    class Meta:
        model = Ocorrencia
        fields = '__all__'
        read_only_fields = ('event',)


class AgendaDetailSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    ocorrencia = OcorrenciaSerializer()
    praca_detail = PracaListSerializer(source='praca',read_only=True)

    def get_url(self, obj):
        return obj.get_absolute_url()

    def create(self, validated_data):
        ocorrencia = validated_data.pop('ocorrencia')
        agenda = Agenda.objects.create(**validated_data)
        Ocorrencia.objects.create(event=agenda, **ocorrencia)

        return agenda

    def update(self, instance, validated_data):
        ocorrencia_data = validated_data.pop('ocorrencia')
        ocorrencia = OcorrenciaSerializer(instance, data=ocorrencia_data)

        if ocorrencia.is_valid(raise_exception=True):
            ocorrencia.save()
            validated_data['ocorrencia'] = ocorrencia_data
            return instance
        raise serializers.ValidationError

    class Meta:
        model = Agenda
        fields = '__all__'
