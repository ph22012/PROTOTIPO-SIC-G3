from django.db import models
class saldosTransaccion(models.Model):
    idSaldoTransaccion = models.AutoField(unique=True,primary_key=True)
    idTransaccion = models.ForeignKey('Transaction', on_delete=models.CASCADE)
    idCuenta = models.CharField(max_length=2)
    debeTransaccion = models.DecimalField(max_digits=30, decimal_places=2)
    haberTransaccion = models.DecimalField(max_digits=30, decimal_places=2)
    fechaTransaccion = models.DateField()


# Create your models here.
class Transaction(models.Model):
    idTransaccion = models.AutoField(unique=True, primary_key=True)
    numPartida = models.CharField(max_length=50) 
    idCuenta = models.ForeignKey('catalogocuentas.Cuenta', on_delete=models.CASCADE) 
    """monto_cargado = models.DecimalField(max_digits=10, decimal_places=2)  
    monto_abonado = models.DecimalField(max_digits=10, decimal_places=2)"""
    #  Aqui se reemplaza la logica, ya no lleva id de saldo, si no que saldo lleva id de transaccion
    # idSaldoTransaccion = models.ForeignKey('saldosTransaccion', on_delete=models.CASCADE)
    descripcion = models.TextField()
    fecha = models.DateField()

    class Meta:
        db_table = 'gtransacciones_transaction'
        ordering = ['fecha']

    def __str__(self):
        return f'Transacción {self.idTransaccion} - {self.descripcion}'


#Logica de registro de transaccion 
#tabla que contiene: idTransaccion 
#                    numPartidad
#                    idCuenta
#                    monto_cargado
#                    Monto_abonado
#                   descripcion
#                    fecha
#/date = models.DateField()
#    description = models.CharField(max_length=255)
#    amount = models.DecimalField(max_digits=10, decimal_places=2)
#    debit_account = models.ForeignKey(Account, related_name='debit_transactions', on_delete=models.CASCADE)
#    credit_account = models.ForeignKey(Account, related_name='credit_transactions', on_delete=models.CASCADE)

    #def _str_(self):
     #   return f"{self.date} - {self.description} - {self.amount}"""


