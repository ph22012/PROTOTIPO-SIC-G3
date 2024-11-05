from django import forms
from .models import Transaction

#class TransactionForm(forms.ModelForm):
#    class Meta:
#        model = Transaction
#        fields = ['date', 'description', 'amount', 'debit_account', 'credit_account']
#        widgets = {
#            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#            'description': forms.TextInput(attrs={'class': 'form-control'}),
#            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
#            'debit_account': forms.Select(attrs={'class': 'form-control'}),
#            'credit_account': forms.Select(attrs={'class': 'form-control'}),
#}