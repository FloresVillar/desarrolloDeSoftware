import pytest
from src.shopping_cart import *
from src.carrito import *

@pytest.mark.smoke
def test_smoke_agregar_y_total():
    carro = Carrito()
    p = Producto("x",0.05)
    carro.agregar_producto(p,1)
    assert carro.calcular_total() == 0.05

@pytest.mark.regression
def test_regression_descuento_redondeo():
    carro = Carrito()
    p = Producto("y",10.0)
    carro.agregar_producto(p,1)
    total = carro.aplicar_descuento(15)
    assert round(total,2) == 8.50