from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from atividades.models import Atividade
from atividades.forms import AtividadesForm
from django.views.generic.list import ListView

import json


# Create your views here.
class CriarAtividade(CreateView):
    form_class = AtividadesForm
    template_name = 'atividades/atividade_form.html'
    success_url = reverse_lazy('atividade-list')


class ModificarAtividade(UpdateView):
    model = Atividade
    success_url = reverse_lazy('atividade-list')


class ListarAtividade(ListView):
    model = Atividade

    def get_context_data(self, **kwargs):
        context = super(ListarAtividade, self).get_context_data(**kwargs)
        atividades_data = Atividade.objects.all().values('nome', 'data_inicio', 'data_termino')
        atividades = list(map(lambda a: {'title': a['nome'], 'start': a['data_inicio'].strftime('%Y-%m-%d'), 'end': a['data_termino'].strftime('%Y-%m-%d')} , atividades_data))
        context['atividades'] = json.dumps(atividades)
        return context


class ExcluirAtividade(DeleteView):
    model = Atividade
    success_url = reverse_lazy('atividade-list')
