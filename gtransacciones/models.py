from django.db import models

# Create your models here.
class Transaction(models.Model):
    idTransaccion = models.AutoField(unique=True, primary_key=True)
    numPartida = models.CharField(max_length=50) 
    idCuenta = models.ForeignKey('Cuenta', on_delete=models.CASCADE) 
    """monto_cargado = models.DecimalField(max_digits=10, decimal_places=2)  
    monto_abonado = models.DecimalField(max_digits=10, decimal_places=2)"""
    idSaldoTransaccion = models.ForeignKey('SaldoTransaccion', on_delete=models.CASCADE)
    descripcion = models.TextField()
    fecha = models.DateField()

    class Meta:
        db_table = 'gtransacciones_transaction'
        ordering = ['fecha']

    def __str__(self):
        return f'Transacción {self.idTransaccion} - {self.descripcion}'
