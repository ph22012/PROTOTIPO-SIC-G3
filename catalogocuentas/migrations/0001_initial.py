<<<<<<< HEAD
# Generated by Django 5.1.2 on 2024-11-05 22:24

=======
# Generated by Django 5.1.2 on 2024-11-05 20:41

import django.db.models.deletion
>>>>>>> 23bb880b30eca8400a09049d2f7b60f40e2979e5
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
<<<<<<< HEAD
=======
        ('EstadosFinancieros', '0001_initial'),
>>>>>>> 23bb880b30eca8400a09049d2f7b60f40e2979e5
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
<<<<<<< HEAD
=======
        migrations.CreateModel(
            name='SaldosCuentas',
            fields=[
                ('idSaldo', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('debe', models.DecimalField(decimal_places=2, max_digits=30)),
                ('haber', models.DecimalField(decimal_places=2, max_digits=30)),
                ('fechaSaldo', models.DateField()),
                ('esFinal', models.BooleanField()),
                ('idCuenta', models.ForeignKey(db_column='idCuenta', on_delete=django.db.models.deletion.CASCADE, to='catalogocuentas.cuenta')),
                ('idEstado', models.ForeignKey(db_column='idEstado', on_delete=django.db.models.deletion.CASCADE, to='EstadosFinancieros.estadosfinancieros')),
                ('idPeriodo', models.ForeignKey(db_column='idPeriodo', on_delete=django.db.models.deletion.CASCADE, to='EstadosFinancieros.periodos')),
            ],
        ),
>>>>>>> 23bb880b30eca8400a09049d2f7b60f40e2979e5
    ]
