from django.forms import ModelForm

from atividades.models import Atividades

class AtividadesForm(ModelForm):
    class Meta:
        model = Atividades
        fields = '__all__'
