"""Pago serializers."""

# Django Rest Framework
from rest_framework import serializers


# Model
from .models import Pago

# Utilities
from datetime import datetime


# Custom Field Validations
def is_valid_date_to_make_payments(value):
    """
    Validates if the date corresponds to an odd day
    which are the days allowed to receive payments

    returns True if valid
    """

    payment_day = str(value).split('-')[2]
    if int(payment_day) % 2 == 0:
        raise serializers.ValidationError(
            "lo siento pero no se puede recibir el pago\
            por decreto de administración"
        )
    return value

def is_valid_paid_value_range(value):
    """
    Validates if (valorPagado) is between 1 and 1000_000
    not less, nor more
    1 represents (un peso)
    1_000_000 represents (1.000.000 - un millon de pesos)
    
    returns True if valid
    """

    min_valid_payment = 1
    max_valid_payment = 1_000_000

    if not min_valid_payment <= value <= max_valid_payment:
        raise serializers.ValidationError(
            'Valor no permitido, debe ser estar entre 1 y 1000000'
        )
    return value



class PagoModelSerializer(serializers.Serializer):
    """ Pago model serializer. """


    fechaPago = serializers.DateField(
        validators=[is_valid_date_to_make_payments],
        error_messages={'invalid': 'Formato de fecha incorrecto'}
    )
    
    documentoIdentificacionArrendatario = serializers.IntegerField(
        error_messages={'invalid': 'Solamente se permiten valores numéricos'}
    )
    
    codigoInmueble = serializers.CharField(max_length=100)
    
    valorPagado = serializers.DecimalField(
        validators=[is_valid_paid_value_range], 
        max_digits=10, decimal_places=0
    )

    
    def create(self, validated_data):
        """
        Create and return a new `Pago` instance, given the validated data.
        """
        return Pago.objects.create(**validated_data)

    # business logic
    def is_partial_payment(self, validated_data):
        """
        return True if valor pagado is less than 1000000
        """
        if self.is_valid():
            return int(validated_data['valorPagado']) < 1_000_000
                
    def get_previous_partial_payments(self, validated_data):
        """
        verify if a list of partial payments exists
        """
        payments = Pago.objects.all()
        property = payments.filter(codigoInmueble=validated_data['codigoInmueble'])
        partial_payments = property.filter(valorPagado__lt=1_000_000)
        return partial_payments
        
    def get_current_pending_charge(self, partial_payments, validated_data):    
        """
        Loop throw the list of partial payments and add the values together
        to know how much is pending to charge 
        """
        if partial_payments:
            previous_payments_sum = 0
            for partial_payment in partial_payments:
                previous_payments_sum += partial_payment.valorPagado
            pending_amount = previous_payments_sum % 1_000_000
            new_charge = 1_000_000 - (pending_amount + int(validated_data['valorPagado']))
            return new_charge
