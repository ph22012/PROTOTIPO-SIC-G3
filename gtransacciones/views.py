from django.shortcuts import render, redirect
#from .forms import TransactionForm

# Create your views here.
"""def transacciones(request):
    return render(request, 'rtransacciones.html')"""


"""def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_transaction')  # Redirige a la misma página para registrar otra transacción
    else:
        form = TransactionForm()
    return render(request, 'create_transaction.html', {'form': form})"""