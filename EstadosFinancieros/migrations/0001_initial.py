import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='periodos',
            fields=[
                ('idPeriodo', models.AutoField(primary_key=True, serialize=False)),
                ('fechaInicio', models.DateField()),
                ('fechaFin', models.DateField()),
            ],
            options={
                'db_table': 'periodos',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='tiposEstados',
            fields=[
                ('idTipoEstado', models.AutoField(primary_key=True, serialize=False)),
                ('nombreEstado', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'tiposEstados',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='estadosFinancieros',
            fields=[
                ('idEstado', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('idPeriodo', models.ForeignKey(db_column='idPeriodo', on_delete=django.db.models.deletion.CASCADE, to='EstadosFinancieros.periodos')),
                ('idTipoEstado', models.ForeignKey(db_column='idTipoEstado', on_delete=django.db.models.deletion.CASCADE, to='EstadosFinancieros.tiposestados')),
            ],
        ),
    ]
