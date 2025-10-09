# Actividad 8 : El patrón AAA-Red-Green-Refactor
En esta actividad se usa el proceso RGR(red, gree,refactor) y pruebas unitarias con pytest<br>
## El patron AAA
Arrange: Prepara el escenario<br> 
Act: Ejecuta el comportamiento<br>
Assert: Verifica el resultado <br>
Las pruebas son el primer uso real de código: lo invocan como lo haría la aplicacion<br>
Los nombres de las clases y métodos de prueba cuentan la "historia" del comportamiento esperado ("TestUsername")

Aplicar los principios FIRST: <br>
- Fast: ejecucion rápida
- Isolated: independientes entre sí
- Repeteable: sin factores externos , apoyandose en stubs/mocks cuando haga falta
- Self-verifying:repotan aprobado/fallo sin inspeccion manual
- Timely : se escriben antes del codigo productivo

## Introducción a Red-Green-Refactor
1. Red (Fallo): Escribir una prueba que falle porque la funcionalidad no está implementada aún
2. Green (Verde): Implementar la funcionalidad mínima necesaria que pase la preba
3. Refactor (Refactorizar): Mejorar el código existente sin cambiar su comportamiento, manteniendo todas las pruebas pasando

Este ciclo se repite iterativamente

Creamos las carpetas
```bash
loDeSoftware/labs/Laboratorio4$ mkdir -p out evidencias
(venv_labo4)

```
### Observaciones y configuración 
- Markers de pytest(si se usa @pytest.mark.smoke y @pytest.mark.regression¡) se declara en pytest.ini
```bash
[pytest]
pythonpath = -ra
testpaths = tests[pytest]
filterwarnings =
    ignore::DeprecationWarning
markers =     
    smoke: fast smoke tests
    regression: extended regression suite


``` 
- Mocks
```bash
pytest==8.3.3
pytest-cov==5.0.0
coverage==7.6.1
factory-boy==3.3.0
pylint==3.2.7
pytest-mock
```

- Quality gate de cobertura(falla si no alcanza el mínimo)

```bash
loDeSoftware/labs/Laboratorio3$ pytest -q --maxfail=1 --disable-warnings --cov=src --cov-report=term-missing --cov-fail-under=90 --junitxml=out/junit.xml
pytest --cov=src --cov-report=term-missing > out/coverage.txt
...............                      [100%]
- generated xml file: /home/esau/desarrolloDeSoftware/labs/Laboratorio3/out/junit.xml -

---------- coverage: platform linux, python 3.12.3-final-0 -----------
Name                   Stmts   Miss  Cover   Missing
----------------------------------------------------
src/__init__.py            0      0   100%
src/carrito.py            55      7    87%   9, 21, 50, 52, 60, 68, 91
src/factories.py           7      0   100%
src/shopping_cart.py      29      3    90%   9, 27, 31
----------------------------------------------------
TOTAL                     91     10    89%

FAIL Required test coverage of 90% not reached. Total coverage: 89.01%
15 passed, 1 warning in 0.33s
```

Se entiende que pytest con opciones mediante flags 

```bash
loDeSoftware/labs/Laboratorio3$ pytest -q --maxfail=1 --disable-warnings --cov=src --cov-report=term-missing --cov-fail-under=90 --junitxml=out/junit.xml
...............                      [100%]
- generated xml file: /home/esau/desarrolloDeSoftware/labs/Laboratorio3/out/junit.xml -

---------- coverage: platform linux, python 3.12.3-final-0 -----------
Name                   Stmts   Miss  Cover   Missing
----------------------------------------------------
src/__init__.py            0      0   100%
src/carrito.py            55      7    87%   9, 21, 50, 52, 60, 68, 91
src/factories.py           7      0   100%
src/shopping_cart.py      29      3    90%   9, 27, 31
----------------------------------------------------
TOTAL                     91     10    89%

FAIL Required test coverage of 90% not reached. Total coverage: 89.01%
15 passed, 1 warning in 0.14s
(venv_labo3) 
```
```bash
loDeSoftware/labs/Laboratorio3$ pytest --cov=src --cov-report=term-missing > out/coverage.txt
(venv_labo3) 
```

- Semillas Globales opcionales

```bash
import random
from faker import Faker 
import pytest

@pytest.fixture(autouse = True)
def _semillas_estables():
    random.seed(123)
    try:
        Faker().seed_instance(123)
    except Exception:
        pass

```
### instalacion rapida
```bash
(venv_labo3) esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio3$ pip install -r requirements.txt
Requirement already satisfied: pytest==8.3.3 in ./venv_labo3/lib/python3.12/site-packages (from -r requirements.txt (line 1)) (8.3.3)
Requirement already satisfied: pytest-cov==5.0.0 in ./venv_labo3/lib/python3.12/site-packages (from -r requirements.txt (line 2)) (5.0.0)
Requirement already satisfied: coverage==7.6.1 in ./venv_labo3/lib/python3.12/site-packages (from -r requirements.txt (line 3)) (7.6.1)
Requirement already satisfied: factory-boy==3.3.0 in ./venv_labo3/lib/python3.12/site-packages (from -r requirements.txt (line 4)) (3.3.0)
Requirement already satisfied: pylint==3.2.7 in ./venv_labo3/lib/python3.12/site-packages (from -r requirements.txt (line 5)) (3.2.7)
Collecting pytest-mock (from -r requirements.txt (line 6))
  Using cached pytest_mock-3.15.1-py3-none-any.whl.metadata (3.9 kB)
Requirement already satisfied: iniconfig in ./venv_labo3/lib/python3.12/site-packages (from pytest==8.3.3->-r requirements.txt (line 1)) (2.1.0)
Requirement already satisfied: packaging in ./venv_labo3/lib/python3.12/site-packages (from pytest==8.3.3->-r requirements.txt (line 1)) (25.0)
Requirement already satisfied: pluggy<2,>=1.5 in ./venv_labo3/lib/python3.12/site-packages (from pytest==8.3.3->-r requirements.txt (line 1)) (1.6.0)
Requirement already satisfied: Faker>=0.7.0 in ./venv_labo3/lib/python3.12/site-packages (from factory-boy==3.3.0->-r requirements.txt (line 4)) (37.8.0)
Requirement already satisfied: platformdirs>=2.2.0 in ./venv_labo3/lib/python3.12/site-packages (from pylint==3.2.7->-r requirements.txt (line 5)) (4.4.0)
Requirement already satisfied: astroid<=3.3.0-dev0,>=3.2.4 in ./venv_labo3/lib/python3.12/site-packages (from pylint==3.2.7->-r requirements.txt (line 5)) (3.2.4)
Requirement already satisfied: isort!=5.13.0,<6,>=4.2.5 in ./venv_labo3/lib/python3.12/site-packages (from pylint==3.2.7->-r requirements.txt (line 5)) (5.13.2)
Requirement already satisfied: mccabe<0.8,>=0.6 in ./venv_labo3/lib/python3.12/site-packages (from pylint==3.2.7->-r requirements.txt (line 5)) (0.7.0)
Requirement already satisfied: tomlkit>=0.10.1 in ./venv_labo3/lib/python3.12/site-packages (from pylint==3.2.7->-r requirements.txt (line 5)) (0.13.3)
Requirement already satisfied: dill>=0.3.6 in ./venv_labo3/lib/python3.12/site-packages (from pylint==3.2.7->-r requirements.txt (line 5)) (0.4.0)
Requirement already satisfied: tzdata in ./venv_labo3/lib/python3.12/site-packages (from Faker>=0.7.0->factory-boy==3.3.0->-r requirements.txt (line 4)) (2025.2)
Using cached pytest_mock-3.15.1-py3-none-any.whl (10 kB)
Installing collected packages: pytest-mock
Successfully installed pytest-mock-3.15.1
(venv_labo3) esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio3$
```
## Ejecución con Makefile (AAA + RGR )
Se tiene Makefile con atajos para el ciclo Red-Green-Refactor<br>
- make test
- make cov
- make lint 
- make rgr
- make red
- make green
- make refactor
### Flujo recomendado (ciclo RGR)
make red || true → make green → make refactor → make rgr 

### Cobertura y estilo 
make cov  ,  male lint 

### Ejecutando las pruebas
make test<br>
Todas las pruebas deberían pasar confirmando que la funcionalidad *ShopingCart* funciona correctamente despues de las cinco iteraciones del proceso RGR

## Uso de mocks y stubs
Hemos incorporado el uso de mocks para simular el comportamiento de un servicio externo de procesamiento de pagos(payment_gateway)<br>
```bash
 def process_payment(self, amount):
        if not self.payment_gateway:
            raise ValueError("No se proporciona pasarela de pago.")
        try:
            success = self.payment_gateway.process_payment(amount)  
            return success
        except Exception as e: 
            raise e
```
Esto se logra mediante la inyección de dependencias, donde payment_gateway se pasa como parametro 
```bash
payment_gateway = Mock()
payment_gateway.process_payment.return_value = True
cart = ShoppingCart(payment_gateway=payment_gateway)
```
Esto permite que durante las pruebas, podamos sustituir el gateway real por un mock , evitando llamadas reales a servicios externos y permitiendo controlar sus comportamientos(como simular pagos exitosos o fallidos)

- Mock : un objeto que simula el comportamiento de objetos reales  de manera controlada. En este caso , *payment_gateway* es un mock que simula el metodo *process_payment*
- Stub : Un objeto que proporciona respuestas predefinidas a llamadas realizadas durante las pruebas, sin lógica adicional, en este caso <br>
*payment_gateway.process_payment.return_value = True*

### Inyección de dependencia
clase   ←  dependencias desde el exterior
```bash
cart = ShoppingCart(payment_gateway=payment_gateway)
```
Esto es una inyección por metodo, asi se puede pasar mocks/stubs en pruebas. Esto facilita el uso de mocks durante las pruebas y mejorar la modularidad y flexibilidad

### Manejo de excepciones
En el método process_payment se agrega manejo de excepciones
```bash
except Exception as e:
            # Maneja excepciones según sea necesario
            raise e
```
### Refactorización
Cada iteración del proceso RGR  se basa en la anterior, permitiendo construir la clase ShoppingCart robusta y funcional <br>
Al integrar caracteristicas avanzadas como la inyección de dependencias y el uso de mocks, asegurando que el código sea testeable y mantenible

### Pruebas prácticas en pruebas
- Pruebas unitarias  : cada prueba se ocupa de una funcionalidad especifica de ShoppingCart
- Aislamiento : Al usar mocks para  el payment_gateway aislamos las pruebas de la clase ShoppingCart de dependencias externas
- Cobertura de casos de uso : se cubren escenarios exitosos   
```bash
def test_process_payment():
    payment_gateway = Mock()#sin importar si en produccion es un sericio interno, vamos reducireno acoplamineto , evitamos ...que?
    payment_gateway.process_payment.return_value = True
    cart = ShoppingCart(payment_gateway=payment_gateway)
    cart.add_item("apple", 2, 0.5)
    cart.add_item("banana", 3, 0.75) #hasta aqui es arrange
    cart.apply_discount(10)
    total = cart.calculate_total() #act
    result = cart.process_payment(total) #act
    payment_gateway.process_payment.assert_called_once_with(total) #assert
    assert result is True #assert
```
Y el escenario de fallos
```bash
def test_process_payment_failure():
    payment_gateway = Mock()  
    payment_gateway.process_payment.side_effect = Exception("Pago fallado")
    cart = ShoppingCart(payment_gateway=payment_gateway)
    cart.add_item("apple", 2, 0.5)
    cart.apply_discount(10) 
```
### Ejercicios
#### Reglas generales
- No cambiamos *src/carrito.py* .. ni *Makefile*
```bash
class Producto :
    def constructor():
        nombre,precio
    def info():
        return info
class ItemCarrito:
    def constructor():
        producto;cantidad
    def total(): 
        producto.precio*cantidad
    def info():
        return info

class Carrito:
    def constructor():
        item = []
    def agregar_producto(producto,cantidad):
        for item in items
            item.cantidad+=cantidad
        items.append(ItemCarrito(producto,cantidad))
    def remover_producto():
        ...

    def actualizar_cantidad():
        ..
    def calcular_total():
        ..
    ...  
```
#### Ejecucion base
```bash
pytest -q --maxfail=1 --disable-warnings --cov=src --cov-report=term-missing --cov-fail-under=90 --junitxml=out/junit.xml
```

```bash
(venv_labo3) esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio3$ pytest -q --maxfail=1 --disable-warnings --cov=src --cov-report=term-missing --cov-fail-under=90 --junitxml=out/junit.xml
...............                                                             [100%]
- generated xml file: /home/esau/desarrolloDeSoftware/labs/Laboratorio3/out/junit.xml -

---------- coverage: platform linux, python 3.12.3-final-0 -----------
Name                   Stmts   Miss  Cover   Missing
----------------------------------------------------
src/__init__.py            0      0   100%
src/carrito.py            55      7    87%   9, 21, 50, 52, 60, 68, 91
src/factories.py           7      0   100%
src/shopping_cart.py      29      3    90%   9, 27, 31
----------------------------------------------------
TOTAL                     91     10    89%

FAIL Required test coverage of 90% not reached. Total coverage: 89.01%
15 passed, 1 warning in 0.32s
```
```bash
(venv_labo3) esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio3$ pytest --cov=src --cov-report=term-missing > out/coverage.txt
(venv_labo3)
```

### El patrón AAA
#### A1 Descuestos parametrizados
En el bloque de parametrizacion se modifica este bloque para que los descuentos sean porcentajes y no numeros decimales<br>
```bash
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
```
mientras que en la funci+on de prueba unitaria<br>
```bash

def test_descuento_total(precio,cantidad,descuento,esperado):
    carro = Carrito()
    producto = Producto("x",precio)
    item = ItemCarrito(producto,cantidad)    
    carro.agregar_producto(producto,cantidad)
    total_final = carro.aplicar_descuento(descuento)
    assert round(total_final,2) == pytest.approx(esperado,abs=0.01)
    
```
#### A2 Idempotencia de actualización de cantidades
Verifica que establecer varias veces la misma cantidad no cambia el total ni el numero de items<br>

```bash
 for item in self.items:
            if item.producto.nombre == producto.nombre:
                if nueva_cantidad == 0:
                    self.items.remove(item)
                else:
                    item.cantidad = nueva_cantidad
                return
        raise ValueError
```
Se asegura que siempre se actualiza la nueva cantidad para un mismo producto
```bash
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
```
#### A3 Fronteras de precio y valores inválidos
Cubre precios fronteraa 0.01 0.005 ..<br>
y precios no validos 0, negativos. Si el comportamiento no esta definido en SUT(componente que se esta probando Carrito) usa *xfail* con razon.<br>

En ItemCarrito 
```bash
def precio_total(self):
        return self.producto.precio * self.cantidad
```
Y en Carrito
```bash
def calcular_total(self):
        """ Calcula el total del carrito sin descuento."""
        total = 0
        for item in self.items:
            total += item.precio_total()
        return total
```

y al ejecutar la prueba
```bash
tware/labs/Laboratorio3$ pytest tests/test_precios_fronteras.py
=============== test session starts ===============
platform linux -- Python 3.12.3, pytest-8.3.3, pluggy-1.6.0
rootdir: /home/esau/desarrolloDeSoftware/labs/Laboratorio3
configfile: pytest.ini
plugins: Faker-37.8.0, cov-5.0.0, mock-3.15.1
collected 6 items                                 

tests/test_precios_fronteras.py ....xX      [100%]

===== 4 passed, 1 xfailed, 1 xpassed in 0.08s =====
(venv_labo3) esau@DESKTOP-A3RPEKP
```
#### A4 Redondeos acumulados vs final
Crea casos donde redondear por item difiere de redondear al final.<br>
```bash
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
```
y la ejecucion de la prueba
```bash
(venv_labo3) esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio3$ pytest tests/test_redondeo_acumulado.py
================= test session starts ==================
platform linux -- Python 3.12.3, pytest-8.3.3, pluggy-1.6.0
rootdir: /home/esau/desarrolloDeSoftware/labs/Laboratorio3
configfile: pytest.ini
plugins: Faker-37.8.0, cov-5.0.0, mock-3.15.1
collected 2 items                                      

tests/test_redondeo_acumulado.py ..              [100%]

================== 2 passed in 0.06s ===================
(venv_labo3)
```

### RGR sin tocar el SUT

#### B1 Rojo  (falla esperada) - precisión financiera
Escribimos un test que xfail con precision binaria float.
En el metodo calculate_total() de ShoppingCart
```bash

    def calculate_total(self):
        total = sum(item["quantity"] * item["unit_price"] for item in self.items.values())
        if self.discount > 0:
            total *= (1 - self.discount / 100)
        return total  # Redondea a 2 decimales
```
Ejecutando test etapa R siguiendo el ciclo TDD rgr 
```bash

@pytest.mark.xfail(reason="Float puede introducir error en dinero")
def test_total_precision_decimal():
    shopping = ShoppingCart()
    shopping.add_item("x",1,0.1)  
    shopping.add_item("y",1,0.2)
    print(shopping.calculate_total())
    assert shopping.calculate_total() == 0.3
```

se tiene que la salida es
```bash
================== test session starts ==================
platform linux -- Python 3.12.3, pytest-8.3.3, pluggy-1.6.0
rootdir: /home/esau/desarrolloDeSoftware/labs/Laboratorio3
configfile: pytest.ini
plugins: Faker-37.8.0, cov-5.0.0, mock-3.15.1
collected 1 item                                        

tests/test_rgr_precision_rojo.py 0.30000000000000004
x

================== 1 xfailed in 0.07s =
```

tal como se aprecia el total es 0.30000...4 y no exactamente 0.3<br>

#### B2 Verde (exclusión docuementada)
Convierte el test anterior a *skip* con una razon explicita(no se corrige..). <br>
De la lectura 14 
```bash
9. Marcas de pytest: xfail y skip
En pipelines orientados a gates, xfail documenta deudas técnicas conocidas o comportamientos no soportados en determinados entornos, mientras que skip evita ruido cuando una precondición externa no se cumple.
```
Bueno, skip evita ruido , osea omitir el test por una razon externa

```bash
@pytest.mark.skip(reason = "Contrato:precision binaria no se corrige")
def test_total_precision_decimal_skip():
    shopping = ShoppingCart()
    shopping.add_item("x",1,0.1)
    shopping.add_item("y",1,0.2)
    print(shopping.calculate_total())
    assert shopping.calculate_total() == 0.3
```
Ejecutando
```bash
collected 1 item                           

tests/test_rgr_precision_verde.py s

============ 1 skipped in 0.01s ============
(venv_labo3)
```
A ver , la salida indica las version de linux, python ,pytest. la ruta donde pytest busca para ejecutar, luego el resultado esperado del test, que se omite en este caso<br> 
#### B3 Refactor de suites
Reorganizamos casos en 2 clases para legibilidad sin duplicar logica<br>
Para entender el codigo *Pista* se requiere chequear la lectura11.md
```bash
Stubs devuelven respuestas prefabricadas sin verificar interacciones.
Mocks permiten inspeccionar llamadas, argumentos y orden. Mocks ayuda a afirmar que el codigo cumple contrato de uso(headers)
Stub basta si solo importa el payload(informacion que se transmite)
Mock es necesario si se necesita asegurar el como se invoca una dependencia
```
Para la clase TestPrecisionMonetaria y su funcion test_suma_pequenias_cantidades los conceptos no son nuevos <br>
De modo que se implementa sin contratiempos
```bash
def test_suma_pequenias_cantidades():
        shop = ShoppingCart()
        shop.add_item("x",1,0.05)
        shop.add_item("y",1,0.05)
        total = shop.calculate_total()
        assert round(total,2) == 0.1

```
Mientras que para TestPasarelaDePagos, revisamos en que consiste la inyeccion de dependencias  y como esto es mas favorable que le acoplamiento fuerte<br>
```bash
sin inyeccion
def __init__(self):
    self.gateway = Gateway() #
    
def process_payment(self,monto):
    self.gateway.process_payment(monto)

```
Se ve que gateway depende de una funcion interna entonces se necesitaria modificar la clase , en contraposición con la inyeccion de dependencia
```bash
def __init__(self,payment_gateway):
    self.payment_gateway = payment_gateway
def process_payment(self,monto):
    payment_gateway.process_payment(monto)
```
Más flexible, y luego en el script del test,se puede trabajar con Mock

```bash
import pytest 
from src.shopping_cart import *
from unittest.mock import Mock

class TestPrecisionMonetaria:
    def test_suma_pequenias_cantidades(self):
        shop = ShoppingCart()
        shop.add_item("x",1,0.05)
        shop.add_item("y",1,0.05)
        total = shop.calculate_total()
        assert round(total,2) == 0.1

class TestPasarelaDePagos:
    def test_pago_exitoso(self):
        pgm = Mock()
        pgm.process_payment.return_value = True
        shop = ShoppingCart(payment_gateway=pgm)
        shop.add_item("x",1,10.0)
        resultado_pago = shop.process_payment(10.0)        
        assert resultado_pago is True
        pgm.process_payment.assert_called_once() 

if __name__=='__main__':
    test1 = TestPrecisionMonetaria()
    test1.test_suma_pequenias_cantidades()
    test2 = TestPasarelaDePagos()
    test2.test_pago_exitoso()
```
ejecutando 
```bash
 pytest tests/test_refactor_suites.py
============== test session starts ==============
platform linux -- Python 3.12.3, pytest-8.3.3, pluggy-1.6.0
rootdir: /home/esau/desarrolloDeSoftware/labs/Laboratorio3
configfile: pytest.ini
plugins: Faker-37.8.0, cov-5.0.0, mock-3.15.1
collected 2 items                               

tests/test_refactor_suites.py ..          [100%]

=============== 2 passed in 0.05s ===============
(venv_labo3) esau@DESKTOP-A3RPEKP:
```