# Generated by Django 5.1.2 on 2024-11-06 03:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cuenta',
            fields=[
                ('idCuenta', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('codClase', models.IntegerField()),
                ('rubro', models.IntegerField()),
                ('codMayor', models.IntegerField()),
                ('codCuenta', models.TextField()),
                ('nameCuenta', models.TextField()),
                ('codDetalle', models.TextField(unique=True)),
            ],
            options={
                'db_table': 'cuentas',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('idTransaccion', models.AutoField(primary_key=True, serialize=False)),
                ('numPartida', models.CharField(max_length=50)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('descripcion', models.CharField(max_length=200)),
                ('fecha', models.DateField()),
                ('idCuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gtransacciones.cuenta')),
            ],
            options={
                'db_table': 'gtransacciones_transaction',
                'ordering': ['fecha'],
            },
        ),
        migrations.CreateModel(
            name='SaldosTransaccion',
            fields=[
                ('idSaldoTransaccion', models.AutoField(primary_key=True, serialize=False)),
                ('monto_cargo', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('monto_haber', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('fecha', models.DateField()),
                ('idCuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gtransacciones.cuenta')),
                ('idTransaccion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gtransacciones.transaction')),
            ],
            options={
                'db_table': 'gtransacciones_saldostransaccion',
            },
        ),
    ]
