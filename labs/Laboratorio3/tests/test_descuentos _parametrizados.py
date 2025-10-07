from src.carrito import Carrito , ItemCarrito, Producto
import pytest
@pytest.mark.parametrize(
    "precio,cantidad,descuento,esperado",
    [
        (10.00, 1, 0, 10.00),
        (10.00, 1, 1, 9.9),
        (10.01, 1, 33, 6.71),  # ajusta 'esperado' si el contrato indica otro redondeo
        (100.00, 1, 50, 50.00),
        (1.00, 1, 100, 0.00),
        (50.00, 1, 100, 0.00),
    ],
)

def test_descuento_total(precio,cantidad,descuento,esperado):
    carro = Carrito()
    producto = Producto("x",precio)
    #item = ItemCarrito(producto,cantidad)    
    carro.agregar_producto(producto,cantidad)
    total_final = carro.aplicar_descuento(descuento)
    assert round(total_final,2) == pytest.approx(esperado,abs=0.01)
    

    
