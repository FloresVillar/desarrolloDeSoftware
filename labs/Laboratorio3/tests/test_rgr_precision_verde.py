import pytest 
from src.shopping_cart import *

@pytest.mark.skip(reason = "Contrato:precision binaria no se corrige")
def test_total_precision_decimal_skip():
    shopping = ShoppingCart()
    shopping.add_item("x",1,0.1)
    shopping.add_item("y",1,0.2)
    print(shopping.calculate_total())
    assert shopping.calculate_total() == 0.3