# Rest Framework

#from rest_framework import viewsets
from rest_framework import status, request
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Serializer
from .serializers import PagoModelSerializer

# Models
from .models import Pago


@api_view(['GET', 'POST'])
def payments(request):
    """
    API endpoint that allows pagos to be excecuted
    """
    if request.method == 'GET':
        payments = Pago.objects.all()
        serializer = PagoModelSerializer(payments, many=True)

        return Response(serializer.data,)

    elif request.method == 'POST':

        serializer = PagoModelSerializer(data=request.data)
        
        if serializer.is_valid():
        
            if serializer.is_partial_payment(request.data):
                partial_payments = serializer.get_previous_partial_payments(
                    request.data
                )
                if partial_payments:
                    current_charge = serializer.get_current_pending_charge(
                        partial_payments,
                        request.data
                    )
                    if current_charge == 0:
                        serializer.save()
                        return Response(
                            { "respuesta": "gracias por pagar todo tu arriendo" }
                        )
                    else:
                        serializer.save()
                        return Response(
                            { "Respuesta":
                            "gracias por tu abono, sin embargo recuerda que"
                            f"te hace falta pagar ${current_charge}"
                        }
                    )         
            else:
                serializer.save()
                return Response({ "respuesta": "gracias por pagar todo tu arriendo" })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
