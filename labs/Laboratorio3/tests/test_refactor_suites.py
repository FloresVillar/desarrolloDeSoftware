import pytest 
from src.shopping_cart import *
from unittest.mock import Mock

class TestPrecisionMonetaria:
    def test_suma_pequenias_cantidades():
        shop = ShoppingCart()
        shop.add_item("x",1,0.05)
        shop.add_item("y",1,0.05)
        total = shop.calculate_total()
        assert round(total,2) == 0.1

class TestPasarelaDePagos:
    def test_pago_exitoso():
