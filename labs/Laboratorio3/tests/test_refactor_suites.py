import pytest 
from src.shopping_cart import *
from unittest.mock import Mock

class TestPrecisionMonetaria:
    def test_suma_pequenias_cantidades(self):
        shop = ShoppingCart()
        shop.add_item("x",1,0.05)
        shop.add_item("y",1,0.05)
        total = shop.calculate_total()
        assert round(total,2) == 0.1

class TestPasarelaDePagos:
    def test_pago_exitoso(self):
        pgm = Mock()
        pgm.process_payment.return_value = True
        shop = ShoppingCart(payment_gateway=pgm)
        shop.add_item("x",1,10.0)
        resultado_pago = shop.process_payment(10.0)        
        assert resultado_pago is True
        pgm.process_payment.assert_called_once() 

if __name__=='__main__':
    test1 = TestPrecisionMonetaria()
    test1.test_suma_pequenias_cantidades()
    test2 = TestPasarelaDePagos()
    test2.test_pago_exitoso()