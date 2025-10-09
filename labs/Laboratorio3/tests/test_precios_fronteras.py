import pytest
from src.carrito import *

@pytest.mark.parametrize("precio",[0.01,0.005,0.0049,9999999.99],)
def test_precios_fronteras(precio):
    carro = Carrito()
    p = Producto("p",precio)
    carro.agregar_producto(p,1)
    assert carro.calcular_total() >0
#xfail documenta deuda s tecnicas conocidas o comportamientos  no soportados en determinados entornos
@pytest.mark.xfail(reason="contrato no definido precio=0  o negativo")
@pytest.mark.parametrize("precio_invalido",[0.0, -1.0],)
def test_precios_invalidos(precio_invalido):
    carro = Carrito()
    p = Producto("p",precio_invalido)
    carro.agregar_producto(p,1)
    assert carro.calcular_total() < 0