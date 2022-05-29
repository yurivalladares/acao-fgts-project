from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from acao_fgts.apps.calculo.services import CalularAcaoFgts
from acao_fgts.apps.calculo.models import CalculoFgts
from acao_fgts.apps.calculo.forms import CalculoFgtsForms
from acao_fgts.apps.common.services import render_to_pdf
from django.views.decorators.http import require_POST
from json2html import *
from django.http import HttpResponse
from django.views.generic.base import View



def index(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    id = request.user.id
    calculo_fgts = CalculoFgts.objects.order_by('-created_at').filter(user_id=id, hide=False)
    form = CalculoFgtsForms()
    contexto = {
        'calculo_fgts': calculo_fgts,
        'form': form,
    }
    return render(request, 'dashboard.html', contexto)

def como_funciona(request):
    return render(request, 'como_funciona.html')

@login_required
@require_POST
def calcular_fgts(request):
    nome_completo = request.POST['nome_completo']
    empregador = request.POST['empregador']
    arquivo_extrato = request.FILES['arquivo_extrato']
    user = get_object_or_404(User, pk=request.user.id)
    service = CalularAcaoFgts(
        nome_completo=nome_completo,
        empregador=empregador,
        arquivo_extrato=arquivo_extrato,
        user=user,
    )

    calculo_fgts = service.criar_calculo_fgts()

    return redirect('index')

@login_required
@require_POST
def deletar_calculo(request):
    obj = CalculoFgts.objects.get(pk=request.POST['id'])
    obj.hide = True
    obj.save()
    return redirect('index')

@login_required
@require_POST
def memoria_calculo(request):
    obj = CalculoFgts.objects.get(pk=request.POST['id'])
    table = json2html.convert(json=obj.df_json, clubbing=True,
                              table_attributes="id=\"table_json\" class=\"table table-light table-striped\"")
    contexto = {
        'calculo_fgts': obj,
        'table_json': table
    }
    return render(request, 'memoria_calculo.html', contexto)


class MemoriaPdf(View):
    def post(self, request, *args, **kwargs):

        obj = CalculoFgts.objects.get(pk=request.POST['id'])

        contexto = {
            'calculo_fgts': obj,
            'table_json': json2html.convert(
                json=obj.df_json,
                clubbing=True,
                table_attributes="id=\"table_json\" class=\"table table-sm table-bordered\""
            )
        }
        template = 'memoria_calculo.html'
        pdf = render_to_pdf(template, contexto)
        return HttpResponse(pdf, content_type='application/pdf')