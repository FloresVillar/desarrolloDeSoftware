from unittest.mock import Mock
import pytest
from src.shopping_cart import ShoppingCart
#elcarrito no toca la pasarela de pago, solo conoce el contrato minimo, el metodo process payment
#el as preibsa inyecto un mock 
def test_add_item():
    cart = ShoppingCart()
    cart.add_item("apple", 2, 0.5)  # nombre, cantidad, precio unitario
    assert cart.items == {"apple": {"quantity": 2, "unit_price": 0.5}}

def test_remove_item():
    cart = ShoppingCart()
    cart.add_item("apple", 2, 0.5)
    cart.remove_item("apple")
    assert not cart.items

def test_calculate_total():
    cart = ShoppingCart()
    cart.add_item("apple", 2, 0.5)
    cart.add_item("banana", 3, 0.75)#arrange preparacion
    total = cart.calculate_total()#act ejecucion
    assert total == 2*0.5 + 3*0.75  # 2*0.5 + 3*0.75 = 1 + 2.25 = 3.25

def test_apply_discount():
    cart = ShoppingCart()
    cart.add_item("apple", 2, 0.5)
    cart.add_item("banana", 3, 0.75)
    cart.apply_discount(10)  # Descuento del 10%
    total = cart.calculate_total() #act
    expected_total = (2*0.5 + 3*0.75) * 0.9  # Aplicando 10% de descuento asserr
    assert total == round(expected_total, 2)  # Redondear a 2 decimales aseer

def test_process_payment():
    payment_gateway = Mock()#sin importar si en produccion es un sericio interno, vamos reducireno acoplamineto , evitamos ...que?
    payment_gateway.process_payment.return_value = True

    cart = ShoppingCart(payment_gateway=payment_gateway)
    cart.add_item("apple", 2, 0.5)
    cart.add_item("banana", 3, 0.75) #hasta aqui es arrange
    cart.apply_discount(10)

    total = cart.calculate_total() #act
    result = cart.process_payment(total) #act

    payment_gateway.process_payment.assert_called_once_with(total) #assert
    assert result is True #assert

def test_process_payment_failure():
    payment_gateway = Mock() #arranege
    payment_gateway.process_payment.side_effect = Exception("Pago fallado")
#fallo con sideeffect
    cart = ShoppingCart(payment_gateway=payment_gateway)
    cart.add_item("apple", 2, 0.5)
    cart.apply_discount(10) #hasta aqui arrange , carritos con gateways inyectados

    total = cart.calculate_total() #act
#como usar AAA con el famoso Four.phase-test
#hamos lo mismo pero aparece tear down
#comentario , el tear down es impicito lo hace pytest, pero cuando se habla de four phase test
#setup -exercise   pytest aisla el estado entre pasos? los mocks que se han creado en cada prueba no rquerren una limpieza , se desconoectana al sali, no hay tear down manual, las pruebas no dejan estado sucio
#hay que saber cuadno añadir , 
    with pytest.raises(Exception) as exc_info:
        cart.process_payment(total) #py lanza excepcons

    assert str(exc_info.value) == "Pago fallado"
#podemos combinar act y asser
#han habido casos en que el act y assert se han combinado