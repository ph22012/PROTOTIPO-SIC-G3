from django.db import models

# Create your models here.
class Cuenta(models.Model):
    idCuenta = models.AutoField(unique=True, primary_key=True)
    codClase = models.IntegerField()
    rubro = models.IntegerField()
    codMayor = models.IntegerField()
    codCuenta = models.TextField()
    nameCuenta = models.TextField()
    codDetalle = models.TextField(unique=True)

    class Meta:
        db_table = 'cuentas'
        managed = False

    def __str__(self):
        return self.nameCuenta

class SaldosCuentas(models.Model):
    idSaldo = models.AutoField(unique=True,primary_key=True)
    idCuenta = models.ForeignKey('Cuenta', on_delete=models.CASCADE, db_column='idCuenta', to_field='idCuenta') 
    idPeriodo = models.ForeignKey('EstadosFinancieros.periodos',on_delete=models.CASCADE, db_column='idPeriodo',to_field='idPeriodo')
    idEstado = models.ForeignKey('EstadosFinancieros.estadosFinancieros', on_delete=models.CASCADE, db_column='idEstado', to_field='idEstado')
    debe = models.DecimalField(max_digits=30, decimal_places=2)
    haber = models.DecimalField(max_digits=30, decimal_places=2)
    fechaSaldo = models.DateField(); 
    esFinal = models.BooleanField();

    def __str__(self):
        return f'{self.idCuenta.nameCuenta} - {self.idEstado.idTipoEstado.nombreEstado} Periodo {self.idPeriodo}'