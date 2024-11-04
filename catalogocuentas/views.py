from django.shortcuts import render

# Create your views here.
def catalogoCuentas(request):
    return render(request, 'catalogocuentas.html')