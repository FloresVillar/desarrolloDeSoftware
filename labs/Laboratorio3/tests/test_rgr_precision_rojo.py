import pytest 
from src.shopping_cart import *

@pytest.mark.xfail(reason="Float puede introducir error en dinero")
def test_total_precision_decimal():
    shopping = ShoppingCart()
    shopping.add_item("x",1,0.1)  
    shopping.add_item("y",1,0.2)
    print(shopping.calculate_total())
    assert shopping.calculate_total() == 0.
    
    