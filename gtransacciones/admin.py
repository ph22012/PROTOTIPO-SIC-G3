from django.contrib import admin
from .models import saldosTransaccion, Transaction

# Register your models here.

admin.site.register(saldosTransaccion)
admin.site.register(Transaction)
