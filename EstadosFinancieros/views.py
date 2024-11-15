from django.contrib.auth.decorators import login_required
from datetime import date
from django.shortcuts import render, redirect
from .models import periodos, estadosFinancieros, tiposEstados
from catalogocuentas.models import SaldosCuentas, Cuenta
from decimal import Decimal


# Create your views here.

#VISTA PRINCIPAL DE LISTA DE ESTADOS FINANCIEROS
@login_required
def gestionar(request):
    fechaHoy = date.today();
    periodosContables = periodos.objects.all()
    periodoActual = None
    if 'periodoSelected' not in request.session:
        request.session['periodoSelected'] = "2"
    balanceComprobacion = estadosFinancieros.objects.filter(idTipoEstado = 1, idPeriodo__idPeriodo = int(request.session['periodoSelected'])).first()
    if  balanceComprobacion == None:
        estadosFinancieros.objects.create(
            idTipoEstado = tiposEstados.objects.get(idTipoEstado = 1),
            idPeriodo = periodos.objects.get(idPeriodo =  int(request.session['periodoSelected']))
        )
    if request.method == 'POST':
        selected = request.POST.get('seleccion')
        request.session['periodoSelected'] = selected
        return redirect('/gestionar')
    else:
        if request.session['periodoSelected'] != None:
            for periodo in periodosContables:
                if str(periodo.idPeriodo) == request.session['periodoSelected']:
                    periodoActual = periodo
        #Aqui se buscan
        estadoAjustes = estadosFinancieros.objects.filter(idTipoEstado = 2, idPeriodo__idPeriodo = int(request.session['periodoSelected'])).first()   
        comprobacion2 = estadosFinancieros.objects.filter(idTipoEstado = 3, idPeriodo__idPeriodo = int(request.session['periodoSelected'])).first()   
        resultados = estadosFinancieros.objects.filter(idTipoEstado = 4, idPeriodo__idPeriodo = int(request.session['periodoSelected'])).first()   
        general = estadosFinancieros.objects.filter(idTipoEstado = 6, idPeriodo__idPeriodo = int(request.session['periodoSelected'])).first()   
        #Aqui se registra el resultado de la busqueda
        ajustesExiste = True if estadoAjustes != None else False
        comprobacion2Existe = True if comprobacion2 != None else False
        resultadosExiste = True if resultados != None else False
        generalExiste = True if general != None else False
    return render(request, 'gestion.html', {'periodoActual':periodoActual, 'periodos':periodosContables,'ajustesExiste':ajustesExiste,'comprobacion2Existe':comprobacion2Existe,'resultadosExiste':resultadosExiste,'generalExiste':generalExiste})
#VISTA DEL BALANCE DE COMPROBACIÓN SIN AJUSTAR
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
#VISTA DE LA VENTANA DE AJUSTES
def ajustes(request):
    if 'periodoSelected' not in request.session:
        request.session['periodoSelected'] = "2"
    balanceAjustes = estadosFinancieros.objects.filter(idTipoEstado = 2, idPeriodo__idPeriodo = int(request.session['periodoSelected'])).first()
    if balanceAjustes == None:
        estadosFinancieros.objects.create(
            idTipoEstado = tiposEstados.objects.get(idTipoEstado = 2),
            idPeriodo = periodos.objects.get(idPeriodo =  int(request.session['periodoSelected']))
        )
    
    balanceAjustado = estadosFinancieros.objects.filter(idTipoEstado = 3, idPeriodo__idPeriodo = int(request.session['periodoSelected'])).first()
    if balanceAjustado == None:
        estadosFinancieros.objects.create(
            idTipoEstado = tiposEstados.objects.get(idTipoEstado = 3),
            idPeriodo = periodos.objects.get(idPeriodo =  int(request.session['periodoSelected']))
        )
    balanceGeneral = estadosFinancieros.objects.filter(idTipoEstado = 6, idPeriodo__idPeriodo = int(request.session['periodoSelected'])).first()
    if balanceGeneral == None:
        estadosFinancieros.objects.create(
            idTipoEstado = tiposEstados.objects.get(idTipoEstado = 6),
            idPeriodo = periodos.objects.get(idPeriodo =  int(request.session['periodoSelected']))
        )

    period = periodos.objects.get(idPeriodo = int(request.session['periodoSelected']))
    if request.method == 'POST':
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
                            saldo.debe = Decimal(value)
                        if parts[1]=='haber' and value:
                            saldo.haber = Decimal(value)
                        saldo.fechaSaldo = date.today()
                        saldo.esFinal = False
                        saldo.save()
                    else:
                        SaldosCuentas.objects.create(
                            debe = (Decimal(value)) if parts[1]=="Debito" and value else 0,
                            haber = (Decimal(value)) if parts[1]=="haber" and value else 0,
                            fechaSaldo = date.today(),
                            esFinal = False,
                            idCuenta = saldoAfectado.idCuenta,
                            idEstado = balanceAjustes,
                            idPeriodo = period
                            )
                        #Para el reporte
                    saldoAjustado = SaldosCuentas.objects.filter(idCuenta = saldoAfectado.idCuenta, idEstado__idTipoEstado =3).first()
                    if saldoAjustado != None:
                        if parts[1]=="Debito" and value: 
                            saldoAjustado.debe = saldoAfectado.debe + Decimal(value)
                        if parts[1]=='haber' and value:
                            saldoAjustado.haber = saldoAfectado.haber + Decimal(value)
                        saldoAjustado.fechaSaldo = date.today()
                        saldoAjustado.esFinal = False
                        saldoAjustado.save()
                    else:
                        SaldosCuentas.objects.create(
                        debe = (saldoAfectado.debe + Decimal(value)) if parts[1]=="Debito" and value else 0,
                        haber = (saldoAfectado.haber + Decimal(value)) if parts[1]=="haber" and value else 0,
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
                            haber = (Decimal(value)) if parts[1]=="haber" and value else 0,
                            fechaSaldo = date.today(),
                            esFinal = False,
                            idCuenta = cuentaAfectadaAjuste,
                            idEstado = balanceAjustes,
                            idPeriodo = period
                        )
                    saldoAjustado = SaldosCuentas.objects.filter(idCuenta = cuentaAfectadaAjuste, idEstado__idTipoEstado =3).first()
                    if saldoAjustado != None:
                        if parts[1]=="Debito" and value: 
                            saldoAjustado.debe = Decimal(value)
                        if parts[1]=='haber' and value:
                            saldoAjustado.haber = Decimal(value)
                        saldoAjustado.fechaSaldo = date.today()
                        saldoAjustado.esFinal = False
                        saldoAjustado.save()
                    else:
                        SaldosCuentas.objects.create(
                        debe = (Decimal(value)) if parts[1]=="Debito" and value else 0,
                        haber = (Decimal(value)) if parts[1]=="haber" and value else 0,
                        fechaSaldo = date.today(),
                        esFinal = False,
                        idCuenta = cuentaAfectadaAjuste,
                        idEstado = balanceAjustado,
                        idPeriodo = period
                        )
        AjustesRealizados = SaldosCuentas.objects.filter(idEstado__idTipoEstado = 3, idPeriodo__idPeriodo = int(request.session['periodoSelected']))
        if AjustesRealizados != None:
            for ajustada in AjustesRealizados:
                if ajustada.debe > ajustada.haber:
                    ajustada.debe -= ajustada.haber
                    ajustada.haber = 0
                elif ajustada.debe < ajustada.haber: 
                    ajustada.haber -= ajustada.debe
                    ajustada.debe = 0
                elif ajustada.debe == ajustada.haber:
                    ajustada.debe = 0
                    ajustada.haber = 0
                ajustada.save()
                saldoGeneral = SaldosCuentas.objects.filter(idCuenta = ajustada.idCuenta ,idEstado__idTipoEstado = 6, idPeriodo = period).first()
                if saldoGeneral != None and ajustada.idCuenta.codClase <= 3:
                    saldoGeneral.debe = ajustada.debe
                    saldoGeneral.haber = ajustada.haber
                    saldoGeneral.fechaSaldo = ajustada.fechaSaldo
                    saldoGeneral.esFinal = True
                    saldoGeneral.idCuenta = ajustada.idCuenta
                    saldoGeneral.save()
                elif saldoGeneral == None and ajustada.idCuenta.codClase<=3:
                    SaldosCuentas.objects.create(
                        debe = ajustada.debe,
                        haber = ajustada.haber,
                        fechaSaldo = ajustada.fechaSaldo,
                        esFinal = True,
                        idCuenta = ajustada.idCuenta,
                        idEstado = estadosFinancieros.objects.get(idTipoEstado = 6, idPeriodo = period),
                        idPeriodo = period
                    )
        

        return redirect('/gestionar/balance_ajustado')   

    balanceComprobacion = SaldosCuentas.objects.filter(idPeriodo_id = int(request.session['periodoSelected']), idEstado__idTipoEstado = 1 )
    sumDebeComp = 0
    sumHaberComp = 0
    for dato in balanceComprobacion:
        sumDebeComp += dato.debe
        sumHaberComp += dato.haber
    cuentasAjustes = Cuenta.objects.filter(codClase = 4)
    
    return render(request, 'ajustes.html',{'sinAjustar':balanceComprobacion, 'cuentasAjustes': cuentasAjustes, 'sumDebeComp':sumDebeComp,'sumHaberComp':sumHaberComp,'periodoActual':period})

#VISTA DEL BALANCE DE COMPROBACION AJUSTADO
def comprobacionAjustado(request):
    if 'periodoSelected' not in request.session:
        request.session['periodoSelected'] = '2'
    periodo = periodos.objects.get(idPeriodo = int(request.session['periodoSelected']))
    cuentas = Cuenta.objects.all()
    saldosSinAjustar = []
    ajustes = []
    saldosAjustados = []
    debe1 = 0
    haber1= 0
    debe2 = 0
    debe3 = 0
    haber2 = 0
    haber3 = 0
    for cuenta in cuentas:
        #1° Saldo sin ajustar
        saldoNoAjustado = SaldosCuentas.objects.filter(idCuenta = cuenta, idPeriodo_id = int(request.session['periodoSelected']), idEstado__idTipoEstado = 1).first()
        if saldoNoAjustado != None:
            debe1 += Decimal(saldoNoAjustado.debe)
            haber1 += Decimal(saldoNoAjustado.debe)
            saldosSinAjustar.append(saldoNoAjustado)
        #2° Ajustes realizados
        ajusteRealizado = SaldosCuentas.objects.filter(idCuenta = cuenta, idPeriodo_id = int(request.session['periodoSelected']), idEstado__idTipoEstado = 2).first()
        if ajusteRealizado != None:
            debe2 += Decimal(ajusteRealizado.debe)
            haber2 += Decimal(ajusteRealizado.debe)
            ajustes.append(ajusteRealizado)
        #3° Saldos ajustados
        saldoAjustado = SaldosCuentas.objects.filter(idCuenta = cuenta, idPeriodo_id = int(request.session['periodoSelected']), idEstado__idTipoEstado = 3).first()
        if saldoAjustado != None:
            debe3 += Decimal(saldoAjustado.debe)
            haber3 += Decimal(saldoAjustado.debe)
            saldosAjustados.append(saldoAjustado)

    return render(
        request, 'comprobacion_Ajustado.html',
        {'saldosSinAjustar': saldosSinAjustar,'ajustesRealizados':ajustes ,
         'saldosAjustados':saldosAjustados,'debe1':debe1,'haber1':haber1,
         'debe2':debe2,'haber2':haber2,'debe3':debe3,'haber3':haber3,'periodoActual':periodo})

#VISTA DEL BALANCE GENERAL
def general(request):
    if 'periodoSelected' not in request.session:
        request.session['periodoSelected'] = "2"
    balanceGeneral = estadosFinancieros.objects.filter(idTipoEstado = 6, idPeriodo__idPeriodo = int(request.session['periodoSelected'])).first()
    if balanceGeneral == None:
        estadosFinancieros.objects.create(
            idTipoEstado = tiposEstados.objects.get(idTipoEstado = 6),
            idPeriodo = periodos.objects.get(idPeriodo =  int(request.session['periodoSelected']))
        )
    
    
    periodoActual = periodos.objects.get(idPeriodo = int(request.session['periodoSelected']))
    sumDebe = 0
    sumHaber = 0
    saldosGeneral = SaldosCuentas.objects.filter(idEstado__idTipoEstado=6, idPeriodo = periodoActual)

    for saldo in saldosGeneral:
        sumDebe += saldo.debe
        sumHaber += saldo.haber

    
    return render(request, 'general.html', {'periodoActual':periodoActual, 'saldosGeneral':saldosGeneral, 'sumDebe':sumDebe,'sumHaber':sumHaber})

#VISTA DEL ESTADO DE RESULTADOS
def resultados(request):
    if 'periodoSelected' not in request.session:
        request.session['periodoSelected'] = "2"
    estadoResultado = estadosFinancieros.objects.filter(idTipoEstado = 4, idPeriodo__idPeriodo = int(request.session['periodoSelected'])).first()
    if estadoResultado == None:
        estadosFinancieros.objects.create(
            idTipoEstado = tiposEstados.objects.get(idTipoEstado = 4),
            idPeriodo = periodos.objects.get(idPeriodo =  int(request.session['periodoSelected']))
        )
    periodoActual = periodos.objects.get(idPeriodo = int(request.session['periodoSelected']))
    saldosResultado = SaldosCuentas.objects.filter(idPeriodo = periodoActual, idEstado__idTipoEstado =3)
    
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