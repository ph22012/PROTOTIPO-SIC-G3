from datetime import date
from django.shortcuts import render
from .models import periodos, estadosFinancieros
from catalogocuentas.models import SaldosCuentas

# Create your views here.

def gestionar(request):
    fechaHoy = date.today();
    periodosContables = periodos.objects.all()
    periodoActual = None
    for periodo in periodosContables:
        if fechaHoy >= periodo.fechaInicio and fechaHoy <= periodo.fechaFin:
            periodoActual = periodo
            break
    return render(request, 'gestion.html', {'periodoActual':periodoActual})

def comprobacion(request):
    fechaHoy = date.today();
    periodosContables = periodos.objects.all()
    periodoActual = None
    saldosAll = SaldosCuentas.objects.all()
    sumDebe = 0
    sumHaber =0

    for periodo in periodosContables:
        if fechaHoy >= periodo.fechaInicio and fechaHoy <= periodo.fechaFin:
            periodoActual = periodo
            break
    
    saldosComprobacion = saldosAll.exclude(idPeriodo__idPeriodo=periodoActual.idPeriodo)
    for saldo in saldosComprobacion:
        sumDebe += saldo.debe
        sumHaber += saldo.haber

    
    return render(request, 'comprobacion.html', {'periodoActual':periodoActual, 'saldosComprobacion':saldosComprobacion, 'sumDebe':sumDebe,'sumHaber':sumHaber})

def resultados(request):

    fechaHoy = date.today();
    periodosContables = periodos.objects.all()
    periodoActual = None
    saldosAll = SaldosCuentas.objects.all()
    sumDebe = 0
    sumHaber =0

    for periodo in periodosContables:
        if fechaHoy >= periodo.fechaInicio and fechaHoy <= periodo.fechaFin:
            periodoActual = periodo
            break
    
    saldosResultado = saldosAll.exclude(idPeriodo__idPeriodo=periodoActual.idPeriodo)
    for saldo in saldosResultado:
        sumDebe += saldo.debe
        sumHaber += saldo.haber

    
    return render(request, 'resultados.html', {'periodoActual':periodoActual, 'saldosResultado':saldosResultado, 'sumDebe':sumDebe,'sumHaber':sumHaber})
