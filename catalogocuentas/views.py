from django.shortcuts import render
from .models import Cuenta

# Create your views here.
def catalogoCuentas(request):
    #cuentas = Cuenta.objects.all()
    activos = Cuenta.objects.filter(clase='1')  
    pasivos = Cuenta.objects.filter(clase='2')  
    patrimonio = Cuenta.objects.filter(clase='3')  
    resultado_deudor = Cuenta.objects.filter(clase='4')  
    resultado_acreedor = Cuenta.objects.filter(clase='5')  
    cuentas_cierre = Cuenta.objects.filter(clase='6')
    return render(request, 'catalogocuentas.html',{
        'activos': activos,
        'pasivos': pasivos,
        'patrimonio': patrimonio,
        'resultado_deudor': resultado_deudor,
        'resultado_acreedor': resultado_acreedor,
        'cuentas_cierre': cuentas_cierre,
    })

#{'cuentas': cuentas}
