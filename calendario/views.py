from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Reserva
from .forms import ReservaForm


def reservar_data(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.reservado = True
            reserva.save()
            return redirect('listar_datas')
    else:
        form = ReservaForm()
    return render(request, 'reservar_data.html', {'form': form})

def apagar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        reserva.delete()
    return redirect('listar_datas')
