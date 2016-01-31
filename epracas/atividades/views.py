from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.core.urlresolvers import reverse_lazy
from atividades.models import Atividades

# Create your views here.
class CriarAtividade(CreateView):
    model = Atividades
    fields = '__all__'

class ModificarAtividade(UpdateView):
    model = Atividades
    fields = '__all__'
