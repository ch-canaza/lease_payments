""" Pago Model."""

# Django
from django.db import models

# Utilities
import datetime


class Pago(models.Model):
    """ Pago Model.
    A Pago is is executed when a user makes a partial or total payment of
    the cost of his lease on the previously established dates
    """
    
    fechaPago = models.DateField()
    documentoIdentificacionArrendatario = models.BigIntegerField()
    codigoInmueble = models.CharField(max_length=100)
    valorPagado = models.DecimalField(max_digits=10, decimal_places=0)

    class Meta:
        db_table='pagos'


    def __str__(self):
        """ Return codigoInmueble and fechaPago"""
        
        return str(self.valorPagado)
