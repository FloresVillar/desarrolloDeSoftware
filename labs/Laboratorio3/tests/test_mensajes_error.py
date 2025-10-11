import pytest
from src.carrito import Carrito
@pytest.mark.xfail(reason="Esperamos mensaje con pista accionable (nombre de producto o cantidad inválida)")
def test_mensaje_error_contiene_contexto():
    c = Carrito()
    try:
        c.actualizar_cantidad("inexistente", 1)
    except ValueError as error:
        mensaje = str(error)
    else:
        raise AssertionError("Se esperaba una excepción ValueError, pero no fue lanzada")
    contiene_nombre = False
    if "inexistente" in mensaje:
        contiene_nombre = True
    if contiene_nombre is False:
        raise AssertionError("El mensaje de error debería incluir el nombre del producto ('inexistente')")
