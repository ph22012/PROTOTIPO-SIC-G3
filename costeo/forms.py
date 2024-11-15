from django import forms
from .models import Costo, Empleado

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'tipo', 'salario_diario', 'dias_trabajo']
        
class CostoForm(forms.ModelForm):
    class Meta:
        model = Costo
        fields = ['empleado', 'recargo_porcentaje', 'dias_vacaciones']


