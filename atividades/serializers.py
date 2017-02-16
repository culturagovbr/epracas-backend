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


class OcorrenciaSerializer(serializers.ModelSerializer):
    calendar = serializers.SerializerMethodField()

    def get_calendar(self, obj):
        if obj.repeat_until:
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

    def get_url(self, obj):
        return obj.get_absolute_url()

    def create(self, validated_data):
        ocorrencia = validated_data.pop('ocorrencia')
        agenda = Agenda.objects.create(**validated_data)
        Ocorrencia.objects.create(event=agenda, **ocorrencia)

        return agenda

    class Meta:
        model = Agenda
        fields = '__all__'
