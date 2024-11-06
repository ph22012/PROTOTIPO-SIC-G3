from django.contrib import admin
from .models import Cuenta, Transaction, SaldosTransaccion

class SaldosTransaccionInline(admin.TabularInline):
    model = SaldosTransaccion
    extra = 1  # Número de formularios vacíos a mostrar en el admin

class TransactionAdmin(admin.ModelAdmin):
    inlines = [SaldosTransaccionInline]

admin.site.register(Cuenta)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(SaldosTransaccion)



"""from django.contrib import admin
from .models import Cuenta, Transaction, SaldosTransaccion

# Registra el modelo Cuenta
admin.site.register(Cuenta)

# Registra otros modelos si es necesario
admin.site.register(Transaction)
admin.site.register(SaldosTransaccion)"""



"""from django.contrib import admin

# Register your models here.

from .models import Account

admin.site.register(Account)"""
