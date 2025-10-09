import pytest 
from src.carrito import *

def test_redondeo_acumulado_vs_final():
    carro = Carrito()
    p1 = Producto("a",.333)
    p2 = Producto("b",.6667)
    carro.agregar_producto(p1,3)
    carro.agregar_producto(p2,3)
    total = carro.calcular_total()
    suma_por_item = 0
    for item in carro.items:
        c = item.producto.precio*item.cantidad
        suma_por_item +=c
    assert round(total,2) == round(suma_por_item,2)

def test_redondeo_acumulado_diferente():
    carro = Carrito()
    p1 = Producto("a",0.335)
    p2 = Producto("b",0.335)
    carro.agregar_producto(p1,3)
    carro.agregar_producto(p2,3)
    total = carro.calcular_total()
    suma_por_item = 0
    for item in carro.items:
        suma_por_item +=round(item.producto.precio * item.cantidad,2)
    print(f"total={round(total,2)} , total-item = {suma_por_item}")
    assert round(total,2) != suma_por_item