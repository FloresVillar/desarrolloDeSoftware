from src.carrito import Carrito, Producto

def test_invariante_agregar_remover_y_actualizar():
    c = Carrito()
    p = Producto("x", 5.0)

    c.agregar_producto(p, 3)
    t1 = c.calcular_total()

    c.remover_producto(p, 3)
    c.agregar_producto(p, 3)
    c.actualizar_cantidad(p, 0)

    total_final = c.calcular_total()
    if total_final != 0.0:
        raise AssertionError("El total del carrito debería ser 0.0 después de remover o actualizar a 0")
    cantidad_total = 0
    for item in c.items:
        cantidad_total = cantidad_total + item.cantidad
    if cantidad_total != 0:
        raise AssertionError("La cantidad total de productos debería ser 0 después de remover o actualizar a 0")
    if t1 != 15.0:
        raise AssertionError("El total inicial debería ser 15.0 (3 unidades a 5.0 cada una)")
