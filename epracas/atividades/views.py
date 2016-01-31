from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from atividades.models import Atividade
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils import timezone

# Create your views here.
class CriarAtividade(CreateView):
    model = Atividade
    fields = '__all__'
    success_url = '/atividade/'

class ModificarAtividade(UpdateView):
    model = Atividade
    fields = '__all__'
    success_url = '/atividade/'

class ListarAtividade(ListView):
    model = Atividade
    def get_context_data(self, **kwargs):
        context = super(ListarAtividade, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class ExcluirAtividade(DeleteView):
    model = Atividade
    success_url = reverse_lazy('atividade-list')
