import pytest 
from unittest.mock import *
from src.shopping_cart import *
def test_pago_exitoso():
    mock = Mock()
    mock.process_payment.return_value = True
    shop = ShoppingCart(payment_gateway  = mock)
    shop.add_item("x",1,0.05)
    resultado = shop.process_payment(5)
    assert resultado is True 
    mock.process_payment.assert_called_once_with(5)

def test_pago_timeout_sin_reintento_automatico():
    pgm = Mock()
    pgm.process_payment.side_effect = TimeoutError("timeout")
    shop = ShoppingCart(payment_gateway = pgm)
    shop.add_item("x",1,0.05)
    with pytest.raises(TimeoutError):
        shop.process_payment(0.05)
    assert pgm.process_payment.call_count == 1 

def test_pago_rechazo_definitivo():
    mock = Mock()
    mock.process_payment.return_value = False
    shop = ShoppingCart(payment_gateway = mock)
    shop.add_item("x",1,10.0)
    resultado = shop.process_payment(5)
    assert resultado is False
    mock.process_payment.assert_called_once()
    