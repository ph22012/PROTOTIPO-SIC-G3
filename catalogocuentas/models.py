from django.db import models

# Create your models here.
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

    def __str__(self):
        return self.nameCuenta
