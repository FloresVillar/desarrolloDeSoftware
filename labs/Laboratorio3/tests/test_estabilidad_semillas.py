import random 
import pytest
from faker import Faker
from src.factories import *
from src.carrito import *
import factory.random
def test_estabilidad_semillas(capsys):
    random.seed(123)
    factory. random.reseed_random(123)
    faker = Faker()
    faker.seed_instance(123)
    #
    p1 = ProductoFactory()
    carro1 = Carrito()
    carro1.agregar_producto(p1,1)
    print(carro1.calcular_total())
    salida1 = capsys.readouterr().out
    #
    random.seed(123)
    factory.random.reseed_random(123)
    faker.seed_instance(123)
    #
    p2 = ProductoFactory()
    carro2 = Carrito()
    carro2.agregar_producto(p2,2)
    print(carro2.calcular_total())
    salida2 = capsys.readouterr().out
    #
    assert salida1 == salida2
    