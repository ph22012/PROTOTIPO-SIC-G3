from django.db import models

class periodos(models.Model):
    idPeriodo = models.AutoField(primary_key=True)
    fechaInicio = models.DateField()
    fechaFin = models.DateField()

    class Meta: 
        db_table = 'periodos'
        managed = False
        
    def __str__(self):
        return str(self.idPeriodo)

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

# MODELO DE REGISTRO DE TRANSACCIÓN   
class Transaction(models.Model):
    idTransaccion = models.AutoField(primary_key=True)
    #idPeriodo = models.ForeignKey('periodos', on_delete=models.CASCADE)
    numPartida = models.CharField(max_length=50) 
    idCuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)   
    descripcion = models.TextField()
    fecha = models.DateField()

    class Meta:
        db_table = 'gtransacciones_transaction'
        ordering = ['fecha']

    def __str__(self):
        return f'Transacción {self.idTransaccion}'

    def registrar_saldo(self, id_cuenta, monto, tipo, fecha):
        saldo_transaccion = SaldosTransaccion(
            idCuenta=id_cuenta,
            idTransaccion=self,
            fecha=fecha
        )
        if tipo.lower() == 'cargo':
            saldo_transaccion.monto_cargo = monto
        elif tipo.lower() == 'haber':
            saldo_transaccion.monto_haber = monto
        else:
            raise ValueError("El tipo de saldo debe ser 'cargo' o 'haber'.")

        saldo_transaccion.save()

class SaldosTransaccion(models.Model):
    idSaldoTransaccion = models.AutoField(primary_key=True)
    idCuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    idTransaccion = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    monto_cargo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    monto_haber = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fecha = models.DateField()

    class Meta:
        db_table = 'gtransacciones_saldostransaccion'

    def __str__(self):
        return f'Saldo {self.idSaldoTransaccion} - Cuenta: {self.idCuenta}'








"""from django.db import models

class periodos(models.Model) :
    idPeriodo = models.AutoField(primary_key=True)
    fechaInicio = models.DateField()
    fechaFin = models.DateField()

    class Meta: 
        db_table = 'periodos'
        managed = False
    def __str__(self):
        return str( self.idPeriodo)

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

#MODELO DE REGISTRO DE TRANSACCIÓN   
class Transaction(models.Model):
    idTransaccion = models.AutoField(primary_key=True)
    idPeriodo = models.ForeignKey('periodos', on_delete=models.CASCADE)
    numPartida = models.CharField(max_length=50) 
    idCuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)   
    descripcion = models.TextField()
    fecha = models.DateField()

    class Meta:
        db_table = 'gtransacciones_transaction'
        ordering = ['fecha']

    def __str__(self):
        return f'Transacción {self.idTransaccion}'

    def registrar_saldo(self, id_cuenta, monto, tipo, fecha):
        cuenta = Cuenta.objects.get(id=id_cuenta)
        saldo_transaccion = SaldosTransaccion(
            idCuenta=id_cuenta,
            idTransaccion=self,
            fecha=fecha
        )
        if tipo.lower() == 'cargo':
            saldo_transaccion.monto_cargo = monto
        elif tipo.lower() == 'haber':
            saldo_transaccion.monto_haber = monto
        else:
            raise ValueError("El tipo de saldo debe ser 'cargo' o 'haber'.")

        saldo_transaccion.save()


class SaldosTransaccion(models.Model):
    idSaldoTransaccion = models.AutoField(primary_key=True)
    idCuenta = models.ForeignKey('Cuenta', on_delete=models.CASCADE)
    idTransaccion = models.ForeignKey('Transaction', on_delete=models.CASCADE)
    monto_cargo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    monto_haber = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fecha = models.DateField()

    class Meta:
        db_table = 'gtransacciones_saldostransaccion'

    def __str__(self):
        return f'Saldo {self.idSaldoTransaccion} - Cuenta: {self.idCuenta}'




































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
    
class Transaction(models.Model):
    idTransaccion = models.AutoField(unique=True, primary_key=True)
    idPeriodo = models.ForeignKey('periodos', on_delete=models.CASCADE)
    numPartida = models.CharField(max_length=50) 
    idCuenta = models.ForeignKey('Cuenta', on_delete=models.CASCADE) 
    monto = models.DecimalField(max_digits=10, decimal_places=2)  
    #idSaldoTransaccion = models.ForeignKey('SaldoTransaccion', on_delete=models.CASCADE)
    descripcion = models.TextField()
    fecha = models.DateField()

    class Meta:
        db_table = 'gtransacciones_transaction'
        ordering = ['fecha']

    def __str__(self):
        return f'Transacción {self.idTransaccion}'
    
class saldosTransaccion(models.Model):
    idSaldoTransaccion = models.AutoField(unique=True, primary_key=True)
    idCuenta = models.ForeignKey('Cuenta', on_delete=models.CASCADE)
    idTransaccion = models.ForeignKey('Transaction', on_delete=models.CASCADE)
    monto_cargo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    monto_haber = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fecha = models.DateField()

    class Meta:
        db_table = 'gtransacciones_saldostransaccion'

    def __str__(self):
        return f'Saldo Transacción {self.idSaldoTransaccion}'





date = models.DateField()
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    debit_account = models.ForeignKey(Account, related_name='debit_transactions', on_delete=models.CASCADE)
    credit_account = models.ForeignKey(Account, related_name='credit_transactions', on_delete=models.CASCADE)

    def _str_(self):
        return f"{self.date} - {self.description} - {self.amount}"

class saldosTransaccion(models.Model):
    idSaldoTransaccion = models.AutoField(primary_key=True)
    idTransaccion = models.IntegerField()
    idCuenta = models.CharField(max_length=2)
    debeTransaccion = models.IntegerField()
    haberTransaccion = models.IntegerField()
    fechaTransaccion = models.DateField()

Logica de registro de transaccion 
tabla que contiene: idTransaccion 
                    numPartidad
                    idCuenta
                    monto_cargado
                    Monto_abonado
                    descripcion
                    fecha
"""

