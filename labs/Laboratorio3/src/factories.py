# pylint: disable=too-few-public-methods
# src/factories.py
import factory
from src.carrito import Producto

class ProductoFactory(factory.Factory):  # pylint: disable=too-few-public-methods
    class Meta:
        model = Producto
    nombre = factory.Faker("word")
    precio = factory.Faker("pyfloat", left_digits=2, right_digits=2, positive=True)
#basaso en faker creamos ojetos produto con nombres y precios, hacemos legibles las pruebas
#podmeos variar escenarios, tenemos control sobre como cubrir limites
#definmos plantilla con valores razonables.
#en cada prueba reeferenciamos instancias creadas
#fixtures archivos temporales.....
#factorias codigo listo para usar en pruebas, dentro de ese contexto 
#mocks sustituyen dependencias externas
