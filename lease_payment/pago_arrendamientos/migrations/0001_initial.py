# Generated by Django 3.2.5 on 2021-07-29 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaPago', models.DateField()),
                ('documentoIdentificacionArrendatario', models.BigIntegerField(unique=True)),
                ('codigoInmueble', models.CharField(max_length=100, unique=True)),
                ('valorPagado', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
