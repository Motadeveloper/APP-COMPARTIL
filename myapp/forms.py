from django import forms
from .models import Equipamento, Agendamento, Cliente, Categoria, FAQ

class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = ['nome', 'fotos', 'descricao', 'preco_diaria', 'categoria']
 


class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['data_inicio', 'data_fim', 'hora_inicio', 'frete_total', 'frete_entrega', 'frete_coleta', 'opcao_frete', 'logradouro', 'numero', 'complemento','valor_total']
        widgets = {
            'hora_inicio': forms.TimeInput(format='%H:%M')
        }

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cpf', 'nome_completo', 'data_nascimento', 'email', 'telefone', 'documento_oficial', 'comprovante_residencia']


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'cor']
        widgets = {
            'cor': forms.TextInput(attrs={'type': 'color'}),
        }


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['titulo', 'descricao']
        widgets = {
            'titulo': forms.TextInput(attrs={'maxlength': '65'}),
        }
