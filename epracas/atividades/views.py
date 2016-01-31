from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.core.urlresolvers import reverse_lazy
from atividades.models import Atividade

# Create your views here.
class CriarAtividade(CreateView):
    model = Atividade
    fields = '__all__'

class ModificarAtividade(UpdateView):
    model = Atividade
    fields = '__all__'
