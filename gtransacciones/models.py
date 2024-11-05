from django.db import models

# Create your models here.


class Account(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def _str_(self):
        return f"{self.code} - {self.name}"

class Transaction(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    debit_account = models.ForeignKey(Account, related_name='debit_transactions', on_delete=models.CASCADE)
    credit_account = models.ForeignKey(Account, related_name='credit_transactions', on_delete=models.CASCADE)

    def _str_(self):
        return f"{self.date} - {self.description} - {self.amount}"

class saldosTransaccion(models.Model):
    idSaldoTransaccion = models.AutoField(primary_key=True)
    idCuenta = models.CharField(max_length=2)
    debeTransaccion = models.IntegerField()
    haberTransaccion = models.IntegerField()
    fechaTransaccion = models.DateField()
