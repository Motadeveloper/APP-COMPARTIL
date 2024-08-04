from django.shortcuts import render
from django.http import JsonResponse
from .forms import EnderecoForm
from core.utils import get_coordinates, get_distance_driving, calcular_frete
import requests

def calcular_entrega(request):
    if request.method == 'GET':
        cep = request.GET.get('cep')
        if cep:
            # Consulta a API ViaCEP para obter o logradouro
            response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
            data = response.json()
            
            if 'erro' in data:
                return JsonResponse({'error': 'Informe um CEP Válido!'}, status=400)

            logradouro = data.get('logradouro', 'N/A')

            endereco_fixo = "Rua Vicencia 47, Pina, Recife - PE"
            origin = "Rua Vicencia 47, Pina, Recife - PE"
            destination = cep

            distancia = get_distance_driving(origin, destination)
            
            if distancia is None:
                return JsonResponse({'error': 'Informe um CEP Válido!'}, status=400)
            else:
                frete = calcular_frete(distancia)
                return JsonResponse({'valor_frete': frete, 'distancia': distancia, 'logradouro': logradouro})
        else:
            return JsonResponse({'error': 'Informe um CEP Válido!'}, status=400)
    else:
        form = EnderecoForm()
        return render(request, 'frete/calcular_entrega.html', {'form': form})