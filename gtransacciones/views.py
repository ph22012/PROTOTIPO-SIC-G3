from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import TransactionForm
from .models import Transaction, SaldosTransaccion#, Cuenta
from catalogocuentas.models import SaldosCuentas, Cuenta
from EstadosFinancieros.models import periodos, estadosFinancieros
from decimal import Decimal

@login_required
def create_transaction(request):
    cuentas = Cuenta.objects.all()
    #saldosCuentas = SaldosCuentas.objects.all()
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save()


            cuentas_list = request.POST.getlist('idCuenta')
            montos_list = request.POST.getlist('monto')
            tipos_list = request.POST.getlist('tipo')
            #fechas_list = request.POST.getlist('fecha')


            for cuenta, monto, tipo in zip(cuentas_list, montos_list, tipos_list):
            # Itera a través de las listas de saldos y crea cada registro
                cuentaAct = Cuenta.objects.get(pk=cuenta)
                period = periodos.objects.get(idPeriodo = int(request.session['periodoSelected']))
                estadoComprobacion = estadosFinancieros.objects.get(idEstado=1)
                
                #for account in cuentas:
                #    if account.idCuenta == cuentaAct.idCuenta:
                #        cuentaAct = account
                #        print('La encontre')

                SaldosTransaccion.objects.create(
                    idTransaccion=transaction,
                    idCuenta_id=cuenta,
                    monto_cargo=monto if tipo == 'cargo' else 0,
                    monto_haber=monto if tipo == 'haber' else 0,
                    #fecha=fecha
                )
                messages.success(request, '¡La transacción se ha registrado con éxito!')
                saldo = SaldosCuentas.objects.filter(idCuenta = cuentaAct.idCuenta, idEstado = estadoComprobacion.idEstado).first()                        
                if saldo != None :
                    print('si existe')
                    saldo.debe +=  Decimal(monto if tipo == 'cargo' else 0)
                    saldo.haber += Decimal(monto if tipo == 'haber' else 0)
                    #saldo.fechaSaldo = fecha
                    saldo.esFinal = False
                    saldo.idPeriodo = period
                    saldo.save()
                else :
                    print('No se encontro, se creo otro')
                    SaldosCuentas.objects.create(
                        debe = monto if tipo == 'cargo' else 0,
                        haber = monto if tipo == 'haber' else 0,
                        #fechaSaldo = fecha,
                        esFinal = False,
                        idCuenta = cuentaAct,
                        idEstado = estadoComprobacion,
                        idPeriodo = period
                    )
            return redirect('create_transaction')
    else:
        form = TransactionForm()
    return render(request, 'create_transaction.html', {'form': form, 'cuentas': cuentas})

"""
ULTIMO CODIGO ACTUALIZADO OFICIAL
****************************************************************************************************
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import TransactionForm, SaldosTransaccionForm
from .models import Transaction, SaldosTransaccion, Cuenta
@login_required
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        #form2 = SaldosTransaccionForm(request.POST)

        if form.is_valid():

            transaction = form.save()  # Guarda la transacción
            #saldos_data = request.POST.getlist('saldos')
            
            # Obtener los datos de los saldos desde el formulario
            saldos_data = []
            for i in range(len(request.POST.getlist('saldos[0][idCuenta]'))):
                saldo = {
                    'idCuenta': request.POST.getlist('saldos[0][idCuenta]')[i],
                    'monto': request.POST.getlist('saldos[0][monto]')[i],
                    'tipo': request.POST.getlist('saldos[0][tipo]')[i],
                    'fecha': request.POST.getlist('saldos[0][fecha]')[i]
                }
                saldos_data.append(saldo)

            # Registrar cada saldo asociado a la transacción
            for saldo in saldos_data:
                # Crear un objeto SaldoTransaccion y asociarlo con la transacción
                SaldosTransaccion.objects.create(
                    transaction=transaction,
                    idCuenta=saldo['idCuenta'],
                    monto=saldo['monto'],
                    tipo=saldo['tipo'],
                    fecha=saldo['fecha']
                )
            try:
                cuenta = Cuenta.objects.get(id=saldo['idCuenta'])  # Obtener la cuenta por ID
            except Cuenta.DoesNotExist:
                    form.add_error(None, f'Cuenta con ID {saldo["idCuenta"]} no existe.')
            return redirect('create_transaction')  # Redirige a la misma página para registrar otra transacción
    else:
        form = TransactionForm()

    return render(request, 'create_transaction.html', {'form': form} )
    *************************************************************************************************
"""







"""from django.shortcuts import render, redirect
from .forms import TransactionForm
from .models import Transaction


# Create your views here.
def transacciones(request):
    return render(request, 'rtransacciones.html')


def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save()  # Guarda la transacción
            saldos_data = request.POST.getlist('saldos')
            
            for saldo in saldos_data:
                tipo = saldo.get('tipo')
                id_cuenta = saldo.get('idCuenta')  # ID de cuenta
                monto = saldo.get('monto')
                fecha = saldo.get('fecha')  # Fecha del saldo

                # Llama al método para registrar el saldo
                transaction.registrar_saldo(id_cuenta, monto, tipo, fecha)
                
            #form.save()
            return redirect('create_transaction')  # Redirige a la misma página para registrar otra transacción
    else:
        form = TransactionForm()
    return render(request, 'create_transaction.html', {'form': form})
"""