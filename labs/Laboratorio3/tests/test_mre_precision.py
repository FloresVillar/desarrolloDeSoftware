import pytest
from src.shopping_cart import *

def test_mre_precision():
    shop = ShoppingCart()
    shop.add_item("x",1,0.5)
    shop.add_item("y",1,0.8)
    assert round(shop.calculate_total(),2) ==1.3
