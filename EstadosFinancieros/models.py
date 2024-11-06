from django.db import models


# Create your models here.


class periodos(models.Model) :
    idPeriodo = models.AutoField(primary_key=True)
    fechaInicio = models.DateField()
    fechaFin = models.DateField()

    class Meta: 
        db_table = 'periodos'
        managed = False
    def __str__(self):
        return str( self.idPeriodo)
    
class tiposEstados(models.Model) :
    idTipoEstado = models.AutoField(primary_key=True)
    nombreEstado = models.CharField(max_length=200)
    class Meta: 
        db_table = 'tiposEstados'
        managed = False
    def __str__(self):
        return self.nombreEstado

class estadosFinancieros(models.Model):
    idEstado = models.AutoField(primary_key=True, unique=True)
    idTipoEstado = models.ForeignKey('tiposEstados',on_delete=models.CASCADE,db_column='idTipoEstado',to_field='idTipoEstado')
    idPeriodo = models.ForeignKey('periodos',on_delete=models.CASCADE, db_column='idPeriodo',to_field='idPeriodo')
    
    def __str__(self):
        return f'{self.idTipoEstado.nombreEstado} - Periodo {self.idPeriodo}'
#class saldosEstados(models.Model):
#    idSaldoEstado = models.AutoField(primary_key=True)
#    idEstado = models.ForeignKey('estadosFinancieros',on_delete=models.CASCADE, db_column='idEstado', to_field='idEstado')
#    idSaldo = models.ForeignKey('catalogocuentas.SaldosCuentas', on_delete=models.CASCADE, db_column='idSaldo',to_field='idSaldo')