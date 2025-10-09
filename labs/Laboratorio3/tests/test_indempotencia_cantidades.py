from src.carrito import Carrito,ItemCarrito,Producto 

def test_indempotencia_cantidades():
 c = Carrito()
 p = Producto("x",3.25)
 c.agregar_producto(p,2)
 total1 = c.calcular_total()
 for _ in range(5):
  c.actualizar_cantidad(p,2)
 total2 = c.calcular_total()
 assert total1 == total2
 total = 0
 for item in c.items:
    total +=item.cantidad    #items.append(ItemCarrito(producto, cantidad))
 assert total == 2