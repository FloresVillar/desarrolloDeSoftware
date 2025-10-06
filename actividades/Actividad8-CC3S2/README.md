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
## Ejercicios
### Reglas generales
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