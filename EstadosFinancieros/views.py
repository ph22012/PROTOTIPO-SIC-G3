from django.contrib.auth.decorators import login_required
from datetime import date
from django.shortcuts import render
from .models import periodos, estadosFinancieros
from catalogocuentas.models import SaldosCuentas

# Create your views here.
@login_required
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
    
    saldosPeriodo = saldosAll.filter(idPeriodo__idPeriodo=periodoActual.idPeriodo)
    saldosComprobacion = saldosPeriodo.filter(idEstado__idTipoEstado=1)

    for saldo in saldosComprobacion:
        sumDebe += saldo.debe
        sumHaber += saldo.haber

    
    return render(request, 'comprobacion.html', {'periodoActual':periodoActual, 'saldosComprobacion':saldosComprobacion, 'sumDebe':sumDebe,'sumHaber':sumHaber})

def general(request):
    fechaHoy = date.today();
    periodosContables = periodos.objects.all()
    periodoActual = None
    saldosAll = SaldosCuentas.objects.all()
    sumDebe = 0
    sumHaber = 0

    for periodo in periodosContables:
        if fechaHoy >= periodo.fechaInicio and fechaHoy <= periodo.fechaFin:
            periodoActual = periodo
            break
    
    saldosPeriodo = saldosAll.filter(idPeriodo__idPeriodo=periodoActual.idPeriodo)
    saldosGeneral = saldosPeriodo.filter(idEstado__idTipoEstado=5)

    for saldo in saldosGeneral:
        sumDebe += saldo.debe
        sumHaber += saldo.haber

    
    return render(request, 'general.html', {'periodoActual':periodoActual, 'saldosGeneral':saldosGeneral, 'sumDebe':sumDebe,'sumHaber':sumHaber})

def resultados(request):

    fechaHoy = date.today();
    periodosContables = periodos.objects.all()
    periodoActual = None
    saldosAll = SaldosCuentas.objects.all()

    for periodo in periodosContables:
        if fechaHoy >= periodo.fechaInicio and fechaHoy <= periodo.fechaFin:
            periodoActual = periodo
            break
    
    saldosPeriodo = saldosAll.filter(idPeriodo__idPeriodo=periodoActual.idPeriodo)
    saldosResultado = saldosPeriodo.filter(idEstado__idTipoEstado=3)
    
    ventasNetas = saldosResultado.filter(idCuenta__codCuenta__in=["5101", "4101","4102"])
    utilidadBruta = 0
    for saldo in ventasNetas:
        if saldo.idCuenta.codCuenta == "5101":
            utilidadBruta += saldo.haber
        else:
            utilidadBruta -= saldo.debe    
    
    gastosOperacion = saldosResultado.filter(idCuenta__codCuenta="4103")
    utilidadOperacion = utilidadBruta
    for saldo in gastosOperacion:
        utilidadOperacion -= saldo.debe

    gastosFinancieros = saldosResultado.filter(idCuenta__codMayor="4104")
    utilidadSinImpuestos = utilidadOperacion
    for saldo in gastosFinancieros:
        utilidadSinImpuestos -= saldo.debe


    
    return render(request, 'resultados.html', {'periodoActual':periodoActual, 'saldosResultado':saldosResultado, 'ventasNetas':ventasNetas,'utilidadBruta':utilidadBruta,'gastosOperacion':gastosOperacion,'utilidadOperacion':utilidadOperacion, 'gastosFinancieros':gastosFinancieros,'utilidadSinImpuestos':utilidadSinImpuestos})
