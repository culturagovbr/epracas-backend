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
    start = serializers.DateTimeField()
    repeat_until = serializers.DateField()
    calendar = serializers.SerializerMethodField(read_only=True)

    def get_calendar(self, obj):
        if obj.repeat_until:
            generator = obj.all_occurrences()
            return [date for (date, end_date, occ) in generator]
        else:
            return None


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
    ocorrencia = OcorrenciaSerializer(read_only=True, many=True)

    def get_url(self, obj):
        return obj.get_absolute_url()
