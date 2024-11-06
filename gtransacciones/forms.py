from django import forms
from .models import Transaction, SaldosTransaccion

class SaldosTransaccionForm(forms.ModelForm):
    class Meta:
        model = SaldosTransaccion
        fields = ['idCuenta', 'monto_cargo', 'monto_haber', 'fecha']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['fecha', 'descripcion']



# Crear un formset para los saldos
from django.forms import modelformset_factory
SaldosTransaccionFormSet = modelformset_factory(SaldosTransaccion, form=SaldosTransaccionForm, extra=1)








"""from django import forms
from .models import Transaction, Cuenta

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['fecha', 'descripcion', 'monto', 'idCuenta']  
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'idCuenta': forms.Select(attrs={'class': 'form-control'}), 
        }
"""






"""from django import forms
from .models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['date', 'description', 'amount', 'debit_account', 'credit_account']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'debit_account': forms.Select(attrs={'class': 'form-control'}),
            'credit_account': forms.Select(attrs={'class': 'form-control'}),
}"""

