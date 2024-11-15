from django.db import models
from decimal import Decimal  # Importamos Decimal

class Empleado(models.Model):
    TIPO_EMPLEADO = [
        ('Junior', 'Junior'),
        ('Senior', 'Senior'),
    ]
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=6, choices=TIPO_EMPLEADO)
    salario_diario = models.DecimalField(max_digits=10, decimal_places=2)
    dias_trabajo = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return f"{self.nombre}"

class Costo(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    recargo_porcentaje = models.DecimalField(max_digits=5, decimal_places=2)
    dias_vacaciones = models.IntegerField()

    def calcular_septimo(self):
        salarioSemanalSeptimo = self.empleado.salario_diario * Decimal(7)
        salarioDiarioSeptimo = salarioSemanalSeptimo / self.empleado.dias_trabajo
        return salarioSemanalSeptimo
    
    def calcular_vacaciones(self):
        # Asegurarse de que recargo_porcentaje sea un Decimal
        recargo_decimal = Decimal(self.recargo_porcentaje)
        # Hacemos las operaciones usando Decimal para precisión exacta
        pagoDiasVacaciones = Decimal(self.dias_vacaciones) * self.empleado.salario_diario
        recargo = pagoDiasVacaciones * recargo_decimal / Decimal(100)
        vacacionesAnuales = pagoDiasVacaciones + recargo
        vacacionesSemanal = vacacionesAnuales / Decimal(52)
        return vacacionesSemanal

    def calcular_aguinaldo(self):
        # empleado JUNIOR trabaja de 1 a 3 años
        if self.empleado.tipo == 'Junior':
            aguinaldoAnual = 15 * self.empleado.salario_diario
        elif self.empleado.tipo == 'Senior':
            aguinaldoAnual = 19 * self.empleado.salario_diario
        else:
            aguinaldoAnual = 0
        aguinaldoSemanal = aguinaldoAnual / Decimal(52)
        return aguinaldoSemanal

    def calcular_isss(self):
        semanaISSS = self.calcular_septimo() * Decimal(0.075)  # ISSS patronal 7.5%
        return semanaISSS

    def calcular_afp(self):
        semanaAFP = self.calcular_septimo() * Decimal(0.0875)  # AFP 8.75%
        return semanaAFP

    def calcular_salario_real_semanal(self):
        salario_semanal = self.calcular_septimo() + self.calcular_vacaciones() + self.calcular_aguinaldo() + self.calcular_isss() + self.calcular_afp()
        return salario_semanal

    def calcular_salario_semanal_por_hora(self):
        salario_semanal = self.calcular_salario_real_semanal()
        # Suponemos que la jornada diaria es de 8 horas
        horas_semanales = self.empleado.dias_trabajo * Decimal(8)
        return salario_semanal / horas_semanales
    
    def horasxTrabajador(self):
        horasxTrabajador = Decimal(1400) / Decimal(10)
        return horasxTrabajador
    def costoRealJunior(self):
        costoRealJunior = Decimal(140) * Decimal(4.58)
        return costoRealJunior
    def costoRealSenior(self):
        costoRealSenior = Decimal(140) * Decimal(6.47)
        return costoRealSenior
    def costo_total_mano_de_obra(self):
        costoTotalManoDeObra = (self.costoRealJunior() * Decimal(8)) + (self.costoRealSenior() * Decimal(2))
        return costoTotalManoDeObra

class Cif(models.Model):
    detalle = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=10,decimal_places=2)
    idProyecto = models.ForeignKey('Proyecto', on_delete=models.CASCADE)

class Proyecto(models.Model):
    nombre = models.CharField(max_length=200)
    imagen = models.CharField(max_length=200)  # El nombre de la imagen o el path relativo
    descripcion = models.TextField()
    meses_desarrollo = models.IntegerField()
    horas_totales = models.IntegerField()
    empleados = models.ManyToManyField(Empleado, related_name='proyectos')

    def __str__(self):
        return self.nombre
