from django.forms import ModelForm

from atividades.models import Atividade


class AtividadesForm(ModelForm):
    class Meta:
        model = Atividade
        exclude = ['ceu']
