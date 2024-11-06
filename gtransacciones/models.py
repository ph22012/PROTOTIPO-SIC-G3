from django.db import models
"""class saldosTransaccion(models.Model):
    idSaldoTransaccion = models.AutoField(unique=True,primary_key=True)
    idTransaccion = models.ForeignKey('Transaction', on_delete=models.CASCADE, db_column='idTransaccion', to_field='idTransaccion')
    idCuenta = models.ForeignKey('catalogocuentas.Cuenta', on_delete=models.CASCADE, db_column='idCuenta', to_field='idCuenta') 
    debeTransaccion = models.DecimalField(max_digits=30, decimal_places=2)
    haberTransaccion = models.DecimalField(max_digits=30, decimal_places=2)
    fechaSaldoTransaccion = models.DateField(); 

    def save(self, *args, **kwargs):
        # Si fechaSaldo no está ya asignada, tomar la fecha de la transacción relacionada
        if not self.fechaSaldoTransaccion and self.idTransaccion:
            self.fechaSaldo = self.idTransaccion.fecha
        super().save(*args, **kwargs)


class periodos(models.Model):
    idPeriodo = models.AutoField(primary_key=True)
    fechaInicio = models.DateField()
    fechaFin = models.DateField()

    class Meta: 
        db_table = 'periodos'
        managed = False
        
    def __str__(self):
        return str(self.idPeriodo)
"""
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
    idTransaccion = models.ForeignKey('Transaction', on_delete=models.CASCADE)
    monto_cargo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    monto_haber = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fecha = models.DateField()

    class Meta:
        db_table = 'gtransacciones_saldostransaccion'

    def __str__(self):
        return f'Saldo {self.idSaldoTransaccion} - Cuenta: {self.idCuenta}'


