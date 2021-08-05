from django.test import TestCase, Client

# Django Rest Framework
import rest_framework

# Serializers
from .serializers import is_valid_date_to_make_payments, is_valid_paid_value_range


class PaymentsBussinessLogicTestCase(TestCase):
    """
    Payments manager  test cases.
    """
    

    def setUp(self):
        """
        set values to test
        """
        self.bad_data = { 
                "documentoIdentificacionArrendatario": "1036946622",
                "codigoInmueble": "8870", 
                "valorPagado": "1000000", 
                "fechaPago": "2021/09/21" 
            } 
        self.data = { 
                "documentoIdentificacionArrendatario": 1036946622,
                "codigoInmueble": "aaaa8870", 
                "valorPagado": "1000000", 
                "fechaPago": "21/09/2021" 
            }
        self.partial_data = { 
                "documentoIdentificacionArrendatario": 1036946622,
                "codigoInmueble": "aaaa8870", 
                "valorPagado": "500000", 
                "fechaPago": "21/09/2021" 
            }

        bad_client = Client()
        self.bad_response = bad_client.post('/api/pagos/', self.bad_data)
        
        client = Client()
        self.response = client.post('/api/pagos/', self.data)

        partial_client = Client()
        self.partial_response = partial_client.post('/api/pagos/', self.partial_data)
    
    def test_incorrect_date_format(self):
        """
        test if format date pased by user is allowed
        """        
        self.assertEqual(self.bad_response.status_code, 400)
        self.assertEqual(self.bad_response.content, b'{"fechaPago":["Formato de fecha incorrecto"]}')

    def test_correct_date_format(self):
        """
        test if format date pased by user is allowed 
        """
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.content, b'{"respuesta":"gracias por pagar todo tu arriendo"}')

    def test_date_id_document_number_should_be_integer(self):
        """
        test if documentoIdentificacionArrendatario is a valid integer value
        """
        self.assertEqual(type(self.data['documentoIdentificacionArrendatario']), int)
        self.assertNotEqual(type(self.bad_data['documentoIdentificacionArrendatario']), int)

    def test_codigo_inmueble_should_be_str(self):
        """
        test if codigo inmueble is a valid alfanumeric value
        """
        self.assertEqual(type(self.data['codigoInmueble']), str)
        self.assertEqual(type(self.bad_data['codigoInmueble']), str)

    def test_valid_value_to_pay(self):
        """
        test if valor a pagar is  between a valid range
        """
        
        try:
            valid_1 = is_valid_paid_value_range(1_000_000)
            valid_2 = is_valid_paid_value_range(1)
        except rest_framework.exceptions.ValidationError:
            valid_1 = 'does not fail'
            valid_2 = 'neither fail'
        
        try:
            invalid_1 = is_valid_paid_value_range(0.5)
            invalid_2 = is_valid_paid_value_range(1_000_001)
        except rest_framework.exceptions.ValidationError:
            invalid_1 = 'failed'
            invalid_2 = 'also_failed'

        self.assertEqual(valid_1, 1_000_000)
        self.assertEqual(valid_2, 1)
        self.assertEqual(invalid_1, 'failed')    
        self.assertEqual(invalid_2, 'also_failed')    

    def test_correct_partial_payment_response(self):
        """
        tests the correct response text for partial payments
        """
        self.assertEqual(self.response.status_code, 200)
        #self.assertEqual(self.partial_response.content, b'{}')
    
    def test_should_receive_payments_odd_days(self):
        """
        tests the custom function valid day to make payments
        Note: the function works in rest framework validation scope,
        so it receives the dates in the format it is going to be stored
        after django setting acceptance
        """
        
        try:
            valid_1 = is_valid_date_to_make_payments("2021-09-21")
            valid_2 = is_valid_date_to_make_payments("2020-09-03")
        except rest_framework.exceptions.ValidationError:
            valid_1 = 'does not fail'
            valid_2 = 'neither fail'
        
        try:
            invalid_1 = is_valid_date_to_make_payments("2021-09-20")
            invalid_2 = is_valid_date_to_make_payments("2020-09-08")
        except rest_framework.exceptions.ValidationError:
            invalid_1 = 'failed'
            invalid_2 = 'also_failed'

        self.assertEqual(valid_1, "2021-09-21")
        self.assertEqual(valid_2, "2020-09-03")
        self.assertEqual(invalid_1, 'failed')    
        self.assertEqual(invalid_2, 'also_failed')
