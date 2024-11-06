from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

# Create your views here.
def login_sesion(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        # Autenticar al usuario
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  
            return redirect('/create-transaction/') 
        else:
            return HttpResponse("Credenciales incorrectas. Por favor, intenta de nuevo.")
    return render(request, 'iniciosesion.html')