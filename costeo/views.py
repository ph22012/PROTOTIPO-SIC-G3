# views.py

from django.shortcuts import render, redirect
from .forms import CostoForm, EmpleadoForm
from .models import Costo, Empleado, Cif, Proyecto
from decimal import Decimal

# Vista para registrar empleado
def registrar_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo empleado
            return redirect('registrar_costeo')  # Redirige a la vista de costeo
    else:
        form = EmpleadoForm()

    return render(request, 'registrar_empleado.html', {'form': form})


# Vista para calcular costeo
def registrar_costeo(request):
    if request.method == 'POST':
        costo_form = CostoForm(request.POST)
        empleado_id = request.POST.get('empleado')  # Suponiendo que el formulario de costo tiene un campo para seleccionar al empleado
        
        # Verificar si el empleado existe y está en la base de datos
        if empleado_id:
            empleado = Empleado.objects.get(id=empleado_id)
        else:
            # Si no existe el empleado, podemos mostrar un error o hacer otra acción
            empleado = None

        if costo_form.is_valid() and empleado:
            costo = costo_form.save(commit=False)
            costo.empleado = empleado  # Asignar el empleado seleccionado
            costo.save()

            # Realizar cálculos
            vacaciones = costo.calcular_vacaciones().quantize(Decimal('0.01'))
            aguinaldo = costo.calcular_aguinaldo().quantize(Decimal('0.01'))
            isss = costo.calcular_isss().quantize(Decimal('0.01'))
            afp = costo.calcular_afp().quantize(Decimal('0.01'))
            salario_real_semanal = costo.calcular_salario_real_semanal().quantize(Decimal('0.01'))
            salario_semanal_por_hora = costo.calcular_salario_semanal_por_hora().quantize(Decimal('0.01'))

            return render(request, 'resultados_costeo.html', {
                'empleado': empleado,
                'vacaciones': vacaciones,
                'aguinaldo': aguinaldo,
                'isss': isss,
                'afp': afp,
                'salario_real_semanal': salario_real_semanal,
                'salario_semanal_por_hora': salario_semanal_por_hora
            })
    else:
        costo_form = CostoForm()
        empleado_form = EmpleadoForm()

    return render(request, 'calcular_costeo.html', {
        'costo_form': costo_form,
        'empleado_form': empleado_form,
    })

def manoDeObra(request): 

    costoManoDeObra = Costo.objects.last()
    if not costoManoDeObra:
        return render(request, 'mano_de_obra.html', {'error': 'No se encontró un registro de Costo.'})

    horasTrabajadas = costoManoDeObra.horasxTrabajador().quantize(Decimal('0.01'))
    costoJunior = costoManoDeObra.costoRealJunior().quantize(Decimal('0.01'))
    costoSenior = costoManoDeObra.costoRealSenior().quantize(Decimal('0.01'))
    manoDeObraCosto = costoManoDeObra.costo_total_mano_de_obra().quantize(Decimal('0.01'))
    
    return render(request, 'mano_de_obra.html', {
        'horasTrabajadas': horasTrabajadas,
        'costoJunior': costoJunior,
        'costoSenior': costoSenior,
        'manoDeObraCosto': manoDeObraCosto,
    })


def seleccionar_Cif(request):
    return render(request, 'select_cif.html')

def costos_indirectos(request):
    cifAnteriores = Cif.objects.filter(idProyecto=1)
    proyectoAnterior = Proyecto.objects.filter(id = 1).first()
    proyectoCosteo = Proyecto.objects.filter(id = 2).first()
    cifActuales = []
    factor = 2800 / proyectoAnterior.horas_totales 
    sumOriginal = 0
    sumAdecuada = 0
    #factor = proyectoCosteo.horas_totales/ proyectoAnterior.horas_totales 
    for cif in cifAnteriores:
        cifNuevo = Cif()
        cifNuevo.detalle = cif.detalle
        cifNuevo.monto = cif.monto * Decimal(factor)
        sumOriginal += cif.monto
        sumAdecuada += cifNuevo.monto
        cifActuales.append(cifNuevo)

    return render(request, 'costos_indirectos.html',{'cifOriginales':cifAnteriores,'cifActuales':cifActuales,'factor':factor,'sumOriginal':sumOriginal,'sumAdecuada':sumAdecuada})

def proyectos_view(request):
    proyectos = Proyecto.objects.all() 
    return render(request, 'proyecto.html', {'proyectos': proyectos})

def proyecto_detalle(request, proyecto_id):

    proyecto = Proyecto.objects.get(id=proyecto_id)
    empleados = proyecto.empleados.all()
    
    return render(request, 'detalle_proyecto.html', {
        'proyecto': proyecto,
        'empleados': empleados,
    })

