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





    """date = models.DateField()
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    debit_account = models.ForeignKey(Account, related_name='debit_transactions', on_delete=models.CASCADE)
    credit_account = models.ForeignKey(Account, related_name='credit_transactions', on_delete=models.CASCADE)

    def _str_(self):
        return f"{self.date} - {self.description} - {self.amount}"


Logica de registro de transaccion 
tabla que contiene: idTransaccion 
                    numPartidad
                    idCuenta
                    monto_cargado
                    Monto_abonado
                    descripcion
                    fecha
"""