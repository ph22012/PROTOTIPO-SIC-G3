from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import TransactionForm, SaldosTransaccionForm
from .models import Transaction, SaldosTransaccion
@login_required
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        form2 = SaldosTransaccionForm(request.POST)

        if form.is_valid() and form2.is_valid():

            transaction = form.save() 
            transaction2 = form2.save() # Guarda la transacción
            saldos_data = request.POST.getlist('saldos')
            
            for saldo in saldos_data:
                tipo = saldo.get('tipo')
                id_cuenta = saldo.get('idCuenta')  # ID de cuenta
                monto = saldo.get('monto')
                fecha = saldo.get('fecha')  # Fecha del saldo

                # Llama al método para registrar el saldo
                transaction2.registrar_saldo(id_cuenta, monto, tipo, fecha)
                
            return redirect('create_transaction')  # Redirige a la misma página para registrar otra transacción
    else:
        form = TransactionForm()

    return render(request, 'create_transaction.html', {'form': form} )









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