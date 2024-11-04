from django.shortcuts import render

# Create your views here.
def gestionar(request):
    return render(request, 'gestion.html')

def comprobacion(request):
    return render(request, 'comprobacion.html')