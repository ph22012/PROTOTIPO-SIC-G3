from django.contrib.auth.decorators import login_required
from datetime import date
from django.shortcuts import render, redirect
from .models import periodos, estadosFinancieros
from catalogocuentas.models import SaldosCuentas, Cuenta
from decimal import Decimal

# Create your views here.
@login_required
def gestionar(request):
    fechaHoy = date.today();
    periodosContables = periodos.objects.all()
    periodoActual = None
    if 'periodoSelected' not in request.session:
        request.session['periodoSelected'] = "2" 
    if request.method == 'POST':
        selected = request.POST.get('seleccion')
        request.session['periodoSelected'] = selected
        return redirect('/gestionar')
    else:
        if request.session['periodoSelected'] != None:
            print('vamosbien')
            print(request.session['periodoSelected'])
            for periodo in periodosContables:
                if str(periodo.idPeriodo) == request.session['periodoSelected']:
                    periodoActual = periodo
                    print(periodoActual)
                    print(periodo)
                    
                else:
                    print('iteracion' + str(periodo.idPeriodo))
                    print('no hay pipipi')
        else:
             for periodo in periodosContables:
                if fechaHoy >= periodo.fechaInicio and fechaHoy <= periodo.fechaFin:
                  periodoActual = periodo
                break

    return render(request, 'gestion.html', {'periodoActual':periodoActual, 'periodos':periodosContables})

def comprobacion(request):
    #fechaHoy = date.today();
    periodosContables = periodos.objects.all()
    periodoActual = None
    saldosAll = SaldosCuentas.objects.all()
    sumDebe = 0
    sumHaber =0

    for periodo in periodosContables:
        if periodo.idPeriodo == int(request.session['periodoSelected']):
            periodoActual = periodo
            break
    
    saldosPeriodo = saldosAll.filter(idPeriodo__idPeriodo=periodoActual.idPeriodo)
    saldosComprobacion = saldosPeriodo.filter(idEstado__idTipoEstado=1)

    for saldo in saldosComprobacion:
        sumDebe += saldo.debe
        sumHaber += saldo.haber

    
    return render(request, 'comprobacion.html', {'periodoActual':periodoActual, 'saldosComprobacion':saldosComprobacion, 'sumDebe':sumDebe,'sumHaber':sumHaber})

def ajustes(request):
    if 'periodoSelected' not in request.session:
        request.session['periodoSelected'] = "2"
    balanceAjustado = estadosFinancieros.objects.get(idTipoEstado = 2, idPeriodo__idPeriodo = int(request.session['periodoSelected']))
    period = periodos.objects.get(idPeriodo = int(request.session['periodoSelected']))
    if request.method == 'POST':
        ajustes = []
        #print(request.POST)
        # Extraer los datos de cada campo
        for key, value in request.POST.items():
            if key.startswith('ajuste_Debito') or key.startswith('ajuste_haber'):
                # Obtener el id de la cuenta o ajuste desde el nombre del campo
                parts = key.split('_')
                 # Si es un campo de cuenta, el id está en la penúltima posición (ajuste_debe_1)
                if len(parts) == 3:
                    saldoAfectado = SaldosCuentas.objects.get(pk = int(parts[-1]))
                    saldo = SaldosCuentas.objects.filter(idCuenta = saldoAfectado.idCuenta, idEstado__idTipoEstado =2).first()
                    if saldo != None:
                        if parts[1]=="Debito" and value: 
                            saldo.debe = saldoAfectado.debe + Decimal(value)
                        if parts[1]=='haber' and value:
                            saldo.haber = saldoAfectado.haber + Decimal(value)
                        saldo.fechaSaldo = date.today()
                        saldo.esFinal = False
                        saldo.save()
                    else:
                        SaldosCuentas.objects.create(
                            debe = (saldoAfectado.debe + Decimal(value)) if parts[1]=="Debito" and value else 0,
                            haber = (saldoAfectado.debe + Decimal(value)) if parts[1]=="haber" and value else 0,
                            fechaSaldo = date.today(),
                            esFinal = False,
                            idCuenta = saldoAfectado.idCuenta,
                            idEstado = balanceAjustado,
                            idPeriodo = period
                    )
                # Si es un campo de ajuste, el id está en la última posición (ajuste_debe_ajuste_1)
                elif len(parts) == 4:
                    print('1- tipo: '+parts[1] )
                    cuentaAfectadaAjuste = Cuenta.objects.get(pk = int(parts[-1]))
                    print('2- monto: '+str(value))
                    saldo = SaldosCuentas.objects.filter(idCuenta = cuentaAfectadaAjuste, idEstado__idTipoEstado=2).first()
                    if saldo != None:
                        if parts[1]=="Debito" and value:
                            saldo.debe =  Decimal(value)
                        if parts[1]=="haber" and value: 
                            saldo.haber = Decimal(value) 
                        saldo.fechaSaldo = date.today()
                        saldo.esFinal = False
                        saldo.save()
                    else:
                        SaldosCuentas.objects.create(
                            debe = (Decimal(value)) if parts[1]=="Debito" and value else 0,
                            haber = Decimal(value) if parts[1]=="haber" and value else 0,
                            fechaSaldo = date.today(),
                            esFinal = False,
                            idCuenta = cuentaAfectadaAjuste,
                            idEstado = balanceAjustado,
                            idPeriodo = period
                        )

    balanceComprobacion = SaldosCuentas.objects.filter(idPeriodo_id = int(request.session['periodoSelected']), idEstado__idTipoEstado = 1 )
    sumDebeComp = 0
    sumHaberComp = 0
    for dato in balanceComprobacion:
        sumDebeComp += dato.debe
        sumHaberComp += dato.haber
    cuentasAjustes = Cuenta.objects.filter(codClase = 4)
    
    return render(request, 'ajustes.html',{'sinAjustar':balanceComprobacion, 'cuentasAjustes': cuentasAjustes, 'sumDebeComp':sumDebeComp,'sumHaberComp':sumHaberComp})

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