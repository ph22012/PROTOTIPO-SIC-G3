from django.shortcuts import render
from .models import Cuenta

# Create your views here.
def catalogoCuentas(request):
    #cuentas = Cuenta.objects.all()
    activos = Cuenta.objects.filter(codClase='1')  
    pasivos = Cuenta.objects.filter(codClase='2')  
    patrimonio = Cuenta.objects.filter(codClase='3')  
    resultado_deudor = Cuenta.objects.filter(codClase='4')  
    resultado_acreedor = Cuenta.objects.filter(codClase='5')  
    cuentas_cierre = Cuenta.objects.filter(codClase='6')
    return render(request, 'catalogocuentas.html',{
        'activos': activos,
        'pasivos': pasivos,
        'patrimonio': patrimonio,
        'resultado_deudor': resultado_deudor,
        'resultado_acreedor': resultado_acreedor,
        'cuentas_cierre': cuentas_cierre,
    })

#{'cuentas': cuentas}
