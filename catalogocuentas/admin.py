from django.contrib import admin
from .models import Cuenta, SaldosCuentas
# Register your models here.
admin.site.register(Cuenta)
admin.site.register(SaldosCuentas)