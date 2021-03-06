# Generated by Django 3.2.5 on 2021-07-30 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pago_arrendamientos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='codigoInmueble',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='pago',
            name='documentoIdentificacionArrendatario',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='pago',
            name='valorPagado',
            field=models.DecimalField(decimal_places=0, max_digits=10),
        ),
        migrations.AlterModelTable(
            name='pago',
            table='pagos',
        ),
    ]
