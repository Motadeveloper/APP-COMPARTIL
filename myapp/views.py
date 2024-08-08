from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import EquipamentoForm, AgendamentoForm, ClienteForm, CategoriaForm, FAQForm, Cliente
from .models import Equipamento, Disponibilidade, Agendamento, Categoria, FAQ
from datetime import date, timedelta, datetime, time
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
import re
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

def mysite(request):
    categorias = Categoria.objects.all()
    equipamentos = Equipamento.objects.all()
    faqs = FAQ.objects.all()
    return render(request, 'home.html', {'categorias': categorias, 'equipamentos': equipamentos, 'faqs': faqs})

@login_required
def painel(request):
    return render(request, 'index.html')

@login_required
def adicionar_equipamento(request):
    if request.method == 'POST':
        form = EquipamentoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('equipamento_sucesso')
    else:
        form = EquipamentoForm()
    return render(request, 'adicionar_equipamento.html', {'form': form})

def equipamento_sucesso(request):
    return render(request, 'equipamento_sucesso.html')

@login_required
def listar_equipamentos(request):
    equipamentos = Equipamento.objects.all()
    hoje = date.today()
    for equipamento in equipamentos:
        disponibilidades = Disponibilidade.objects.filter(equipamento=equipamento, disponivel=True, data__gte=hoje).order_by('data')
        equipamento.disponibilidade_inicio = disponibilidades.first().data if disponibilidades.exists() else None
        equipamento.disponibilidade_fim = disponibilidades.last().data if disponibilidades.exists() else None
    return render(request, 'lista_equipamentos.html', {'equipamentos': equipamentos})

@login_required
def editar_equipamento(request, id):
    equipamento = get_object_or_404(Equipamento, id=id)
    if request.method == 'POST':
        form = EquipamentoForm(request.POST, request.FILES, instance=equipamento)
        if form.is_valid():
            form.save()
            return redirect('lista_equipamentos')
    else:
        form = EquipamentoForm(instance=equipamento)
    return render(request, 'editar_equipamento.html', {'form': form})

@login_required
def apagar_equipamento(request, id):
    equipamento = get_object_or_404(Equipamento, id=id)
    if request.method == 'POST':
        equipamento.delete()
        return redirect('lista_equipamentos')
    return render(request, 'apagar_equipamento.html', {'equipamento': equipamento})

def get_preco_diaria(request, equipamento_id):
    equipamento = Equipamento.objects.get(id=equipamento_id)
    return JsonResponse({'preco_diaria': equipamento.preco_diaria})

def get_disponibilidade(request, equipamento_id):
    equipamento = get_object_or_404(Equipamento, id=equipamento_id)
    disponibilidades = Disponibilidade.objects.filter(equipamento=equipamento)
    disponibilidade_dict = {str(d.data): {'disponivel': d.disponivel, 'horario_final_locacao': d.horario_final_locacao} for d in disponibilidades}
    
    ultima_reserva = Disponibilidade.objects.filter(equipamento=equipamento, disponivel=False).order_by('-data').first()
    ultima_reserva_info = None
    if ultima_reserva:
        data_fim = ultima_reserva.data
        if ultima_reserva.horario_final_locacao:
            hora_fim = datetime.combine(data_fim, ultima_reserva.horario_final_locacao) + timedelta(hours=2)
            ultima_reserva_info = {
                'data_fim': data_fim.isoformat(),
                'hora_fim': hora_fim.time().isoformat()
            }
        else:
            ultima_reserva_info = {
                'data_fim': data_fim.isoformat(),
                'hora_fim': None
            }

    return JsonResponse({
        'disponibilidades': disponibilidade_dict,
        'ultima_reserva': ultima_reserva_info
    })

def verificar_cliente(request):
    cpf = request.GET.get('cpf')
    cliente = Cliente.objects.filter(cpf=cpf).first()
    if cliente:
        return JsonResponse({
            'cliente_id': cliente.id,
            'nome_completo': cliente.nome_completo,
            'data_nascimento': cliente.data_nascimento.isoformat(),
            'email': cliente.email,
            'telefone': cliente.telefone
        })
    else:
        return JsonResponse({'error': 'Cliente não encontrado'}, status=404)

def sucesso(request):
    return render(request, 'sucesso.html')

def detalhes_equipamento(request, id):
    equipamento = get_object_or_404(Equipamento, id=id)
    if request.method == 'POST':
        form = AgendamentoForm(request.POST, request.FILES)
        cliente_id = request.POST.get('cliente_id')
        cpf = request.POST.get('cpf')
        
        if cliente_id:
            cliente = get_object_or_404(Cliente, id=cliente_id)
        else:
            cliente = Cliente.objects.filter(cpf=cpf).first()
            if not cliente:
                cliente_form = ClienteForm(request.POST, request.FILES)
                if cliente_form.is_valid():
                    cliente = cliente_form.save()
                else:
                    return render(request, 'detalhes_equipamento.html', {'equipamento': equipamento, 'form': form, 'cliente_form': cliente_form})

        if not cliente:
            cliente_form = ClienteForm(request.POST, request.FILES)
            if cliente_form.is_valid():
                cliente = cliente_form.save()
            else:
                return render(request, 'detalhes_equipamento.html', {'equipamento': equipamento, 'form': form, 'cliente_form': cliente_form})

        if form.is_valid():
            agendamento = form.save(commit=False)
            agendamento.equipamento = equipamento
            agendamento.cliente = cliente
            
            if agendamento.hora_inicio:
                agendamento.hora_fim = agendamento.hora_inicio
            else:
                return render(request, 'detalhes_equipamento.html', {'equipamento': equipamento, 'form': form, 'error': 'Hora de início não definida.'})

            agendamento.valor_total = form.cleaned_data['valor_total']

            agendamento.save()
            
            data_atual = agendamento.data_inicio
            while data_atual <= agendamento.data_fim:
                Disponibilidade.objects.update_or_create(
                    equipamento=equipamento,
                    data=data_atual,
                    defaults={'disponivel': False}
                )
                data_atual += timedelta(days=1)
            
            proxima_data = agendamento.data_fim
            horario_final = (datetime.combine(proxima_data, agendamento.hora_fim) + timedelta(hours=2)).time()
            if horario_final < time(17, 0):
                Disponibilidade.objects.update_or_create(
                    equipamento=equipamento,
                    data=proxima_data,
                    defaults={'disponivel': True, 'horario_final_locacao': horario_final}
                )

            messages.success(request, f'Você acabou de alugar uma {equipamento.nome}. Nossa equipe entrará em contato para mais informações.')
            return render(request, 'detalhes_equipamento.html', {'equipamento': equipamento, 'form': form, 'success': True})
    else:
        form = AgendamentoForm()
    
    return render(request, 'detalhes_equipamento.html', {'equipamento': equipamento, 'form': form})

def get_disponibilidade(request, equipamento_id):
    equipamento = get_object_or_404(Equipamento, id=equipamento_id)
    disponibilidades = Disponibilidade.objects.filter(equipamento=equipamento)
    disponibilidade_dict = {str(d.data): {'disponivel': d.disponivel, 'horario_final_locacao': d.horario_final_locacao} for d in disponibilidades}
    
    ultima_reserva = Disponibilidade.objects.filter(equipamento=equipamento, disponivel=False).order_by('-data').first()
    ultima_reserva_info = None
    if ultima_reserva:
        data_fim = ultima_reserva.data
        if ultima_reserva.horario_final_locacao:
            hora_fim = datetime.combine(data_fim, ultima_reserva.horario_final_locacao) + timedelta(hours=0)
            ultima_reserva_info = {
                'data_fim': data_fim.isoformat(),
                'hora_fim': hora_fim.time().isoformat()
            }
        else:
            ultima_reserva_info = {
                'data_fim': data_fim.isoformat(),
                'hora_fim': None
            }

    return JsonResponse({
        'disponibilidades': disponibilidade_dict,
        'ultima_reserva': ultima_reserva_info
    })

def get_valor_diaria(request, equipamento_id):
    equipamento = Equipamento.objects.get(id=equipamento_id)
    return JsonResponse({'preco_diaria': equipamento.preco_diaria})

def consultarcliente(request):
    return render(request, 'cliente.html')

def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11 or cpf == cpf[0] * len(cpf):
        return False
    for i in range(9, 11):
        value = sum((int(cpf[num]) * ((i+1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != int(cpf[i]):
            return False
    return True

@require_GET
def verificar_cpf(request):
    cpf = request.GET.get('cpf')
    if cpf and validar_cpf(cpf):
        return JsonResponse({'valid': True})
    else:
        return JsonResponse({'valid': False, 'error': 'CPF inválido'}, status=400)

def cliente(request):
    agendamentos = None
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        cliente = Cliente.objects.filter(cpf=cpf).first()
        if cliente:
            agendamentos = Agendamento.objects.filter(cliente=cliente)
    
    return render(request, 'cliente.html', {'agendamentos': agendamentos})

def cancelar_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)
    datas_disponibilidade = Disponibilidade.objects.filter(equipamento=agendamento.equipamento, data__gte=agendamento.data_inicio, data__lte=agendamento.data_fim)
    datas_disponibilidade.update(disponivel=True)
    agendamento.delete()
    messages.success(request, 'Agendamento cancelado com sucesso.')
    return HttpResponseRedirect(reverse('cliente'))

@login_required
def adicionar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria criada com sucesso!')
            return redirect('adicionar_categoria')
    else:
        form = CategoriaForm()
    
    categorias = Categoria.objects.all()
    return render(request, 'adicionar_categoria.html', {'form': form, 'categorias': categorias})

@login_required
def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria atualizada com sucesso!')
            return redirect('adicionar_categoria')
    else:
        form = CategoriaForm(instance=categoria)
    
    categorias = Categoria.objects.all()
    return render(request, 'adicionar_categoria.html', {'form': form, 'categorias': categorias})

@login_required
def apagar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoria apagada com sucesso!')
        return redirect('adicionar_categoria')
    
    categorias = Categoria.objects.all()
    return render(request, 'adicionar_categoria.html', {'form': CategoriaForm(), 'categorias': categorias})

@login_required
def gerenciar_faqs(request):
    if request.method == 'POST':
        if 'criar' in request.POST:
            form = FAQForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('gerenciar_faqs')
        elif 'editar' in request.POST:
            id = request.POST.get('id')
            faq = get_object_or_404(FAQ, id=id)
            form = FAQForm(request.POST, instance=faq)
            if form.is_valid():
                form.save()
                return redirect('gerenciar_faqs')
        elif 'apagar' in request.POST:
            id = request.POST.get('id')
            faq = get_object_or_404(FAQ, id=id)
            faq.delete()
            return redirect('gerenciar_faqs')
    else:
        form = FAQForm()
        faqs = FAQ.objects.all()
    return render(request, 'gerenciar_faqs.html', {'form': form, 'faqs': faqs})


def listar_faqs(request):
    faqs = FAQ.objects.all()
    return render(request, 'faq.html', {'faqs': faqs})

@login_required
def listar_agendamentos(request):
    agendamentos = Agendamento.objects.all().order_by('data_inicio', 'hora_inicio')
    return render(request, 'agendamento.html', {'agendamentos': agendamentos})

@login_required
def editar_agendamento(request, id):
    agendamento = get_object_or_404(Agendamento, id=id)
    if request.method == 'POST':
        form = AgendamentoForm(request.POST, instance=agendamento)
        if form.is_valid():
            datas_antigas = [(agendamento.data_inicio + timedelta(days=dia)) for dia in range((agendamento.data_fim - agendamento.data_inicio).days + 1)]
            novo_agendamento = form.save(commit=False)

            for data in datas_antigas:
                disponibilidade = Disponibilidade.objects.filter(equipamento=agendamento.equipamento, data=data).first()
                if disponibilidade:
                    outros_agendamentos = Agendamento.objects.filter(equipamento=agendamento.equipamento, data_inicio__lte=data, data_fim__gte=data).exclude(id=agendamento.id)
                    if not outros_agendamentos.exists():
                        disponibilidade.disponivel = True
                        disponibilidade.save()

            novo_agendamento.save()

            for dia in range((novo_agendamento.data_fim - novo_agendamento.data_inicio).days + 1):
                data = novo_agendamento.data_inicio + timedelta(days=dia)
                disponibilidade, created = Disponibilidade.objects.get_or_create(equipamento=novo_agendamento.equipamento, data=data)
                disponibilidade.disponivel = False
                disponibilidade.save()

            return redirect('listar_agendamentos')
    else:
        form = AgendamentoForm(instance=agendamento)
    return render(request, 'editar_agendamento.html', {'form': form})

@login_required
def apagar_agendamento(request, id):
    agendamento = get_object_or_404(Agendamento, id=id)
    if request.method == 'POST':
        for dia in range((agendamento.data_fim - agendamento.data_inicio).days + 1):
            data = agendamento.data_inicio + timedelta(days=dia)
            disponibilidade = Disponibilidade.objects.filter(equipamento=agendamento.equipamento, data=data).first()
            if disponibilidade:
                disponibilidade.disponivel = True
                disponibilidade.save()

        agendamento.delete()
        return redirect('listar_agendamentos')
    return render(request, 'apagar_agendamento.html', {'agendamento': agendamento})

def get_cliente_details(request):
    cliente_id = request.GET.get('cliente_id')
    cliente = get_object_or_404(Cliente, id=cliente_id)
    data = {
        'nome_completo': cliente.nome_completo,
        'cpf': cliente.cpf,
        'data_nascimento': cliente.data_nascimento,
        'email': cliente.email,
        'telefone': cliente.telefone,
        'documento_oficial': cliente.documento_oficial.url if cliente.documento_oficial else None,
        'comprovante_residencia': cliente.comprovante_residencia.url if cliente.comprovante_residencia else None,
    }
    return JsonResponse(data)

@login_required
def listar_disponibilidades(request):
    disponibilidades = Disponibilidade.objects.all()
    return render(request, 'disponibilidade.html', {'disponibilidades': disponibilidades})

@login_required
def toggle_disponibilidade(request, id):
    disponibilidade = get_object_or_404(Disponibilidade, id=id)
    disponibilidade.disponivel = not disponibilidade.disponivel
    disponibilidade.save()
    return redirect('listar_disponibilidades')

@login_required
def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'clientes': clientes})


def apagar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('listar_clientes')
    return render(request, 'clientes.html', {'cliente': cliente})

def detalhes_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    return render(request, 'detalhes_cliente.html', {'cliente': cliente})
