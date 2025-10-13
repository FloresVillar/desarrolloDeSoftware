# SOLID y ppruebas
Los entornos actuales 
- Los ciclos de entrega se miden en minutos
- Las arquitecturas se despliegan en contenedores efimeros
El testing automatizado debe integrarse de manera organica con DevOps.<br>
Queremos que las pruebas mejoren con el codigo entonces usamos SOLID<br>

# SRP Principio de responsabilidad unica
Un test debe abarcar un comportamiento unico y especifico<br>
Esto se traduce en el uso de un solo assert
```bash
@pytest.mark.unit
def test_decuento_cliente_frecuente():
    total = 100
    cliente_frecuente = True
    esperado = 90
    resultado = calular_precio_final(total,cliente_frecuente)
    assert resultado == pytest.approx(esperado) 
```

- El mark.unit permite que pytest pueda filtrar ese y otros test con ese decorador y asi poderlos ejecutar en conjunto<br>
- pytest.approx() se usa para dar por valido un aproximado: 0.1 + 0.2 = 0.3.00000004 ,sera considerado 0.3

Entonces siguiendo el principio SRP tenemos: 
- Claridad
- Diagnostico rapido
- Mantenibilidad
- Reusabilidad
- Confianza
El siguiente script no cumple SRP:
```bash
def calcular_precio_final():
    #test cliente frecuente
    arrange
    act
    assert resultado == pytest.approx(90.0)
    #test cliente no frecuente
    ararange
    act 
    assert resultado == pytest.aprox(100.0)
    #test total con impuestos
    arrange
    act
    assert resultado == pytest.approx(110.0)
```
Auqnue haya claridad es dificil de diagnosticar, lo mejor es separlos en 3 test con responsabilidades definidas a comportamientos especificos<br>
```bash
@pytest.mark.unit
def test_descuento_cliente_frencuente():

@pytest.mark.unit
def test_precio_sin_descuento():

@pytest.mark.unit
def test_precio_con_impuestos():

```
## Como mantener SRP en las pruebas 
1. Normar los test de forma descriptiva
2. Usar un assert por tet
3. Evitar logica complejo como bucles, o usar parametrize cuando sea necesario

4. Usar fixtures minimalistas,los fixtures (digamos similar al arrange) incluye solo datos necesarios para el test.

5. Separar pruebas unitarias de pruebas de integracion
```bash
@pytest.mark.unit
def test_descuento_cliente_frecuente():
    arrange
    act
    assert resultado == pytest.approx(90.0)
@pytest.mark.integration
def test_proceso_compra_completo():
    arrange
    act
    asser total == pytest.approx(90.00)
    assert "mensaje" in mensaje
    assert leer_transaccion() == total
```
# OCP EL principio Abierto/cerrado OCP
El sistema debe estar abierto a la amplicacion pero no a la modificacion,ampliamos casos de prueba sin modificre el codigo test <br>
```bash
CASOS = [(),(),()]
@pytest.mark.parametrize("",CASOS)
def test_redondeo_05_centimos(cantidad,esperado):
    assert redondear(cantidad)==pytest.approx(esperado)
```
Se añade nuevos casos a modo de nuevas tuplas en CASOS<br>
Beneficios de aplicar OCP:
1. Escalabilidad
2. MAntenebilidad,al no modificar la logica , reduces el riesgo de introducir error
3. Legibilidad, la lista CASOS es una documentacion clara
4. Reusabilidad, se puede usar la misma estructura en otros tests
5. Automatizacion, añadir casos no implica reescribir codigo

## Extensiones del enfoque
### a. Externalizar los casos de prueba en lugar de mantener CASOS.
```bash
# tests/casos_redondeo.json
[{"cantidad":,"esperado"},{..},{..}]

# tests/test_redonde.py
import pytest
import json
from tienda.redondeo import redondear
with open("casos_redondeo.json") as f:
    CASOS = [ (caso[a],caso[b]) for caso in json.load(f)]
@pytest.mark.parametrize("a,b",CASOS):
    assert redondear(a) == pytest.approx(b)
```
Los equipos como QA pueden actualizar los casos de prueba sin tocar el codigo<br>
### b. Generacion dinamica de casos
si los casos de prueba siguen un patron, puedes generarlos dinamicamente<br>
```bash
CASOS = [(a,round(a,2)) for x in range(W,H,L)]
@pytest.mark.parametrize("a","b",CASOS)..
```

### c. Clasificacion de casos con etiquetas
Puedes usar marcadores de pytest para clasificar casos de prueba segun su proposito (casos limites)<br>
```bash
    CASOS =[
        pytest.param(c1,c2,marks = pytest.mark.casos_comunes),
        pytest.param(c1,c2,marks = pytest.mark.casos_comunes),
        pytest.param(c1,c2,marks = pytest.mark.casos_error)]

    @pytest.mark.parametrize()...
```
filtramos con pytest -m casos_limite

### d. Manejo de excepciones 
si la funcion redondear puede lanzar excepciones se extiende el enfoque para probar esos casos<br>
```bash
import pytest
from tienda.redondeo import redondear

CASOS = [(a,b),(a,b),invalido = pytest.raises(ValueError)]

@pytest.mark.parametrize("p1","p2",CASOS):
    if isinstance(e,) and issubclass(e,Exception):
    with e:
        redondear(p1)
    else:
        assert  redondear(p1)==pytest.approx(p2)
``` 
### Consideraciones adicionales
- limites de OCP, aunque la parametrizacion sirve, si la logica de "redondear" cambia podria se preciso modificar la funcion de prueba<br>
- Cobertura de pruebas, asegurarse que CASOS cubra casos limites, casos comunes, casos de error<br>
pytest-cov ayudan
- Mantenimiento de datos, si CASOS creciera demasiado considerar organizar en modulos separados o usar una base de datos mas completa
# LSP principio de sustitución de Liskov
Los objetos de una clase derivada deben poder sustituir a los objetos de su bas clase, sin alterar el comportamiento del programa<br>
Los doubles de prueba (mocks,stubs,fake) se comportan como la interfaz de la clase real<br>

```bash
# app/repositorio.py
class RepoBD:
    def obtener(self,id_:int)-> dict ..
    def guardar(self,registro:dict) -> int..
# test/test_servicio.py
import ...
from app.repositorio import RepoBD

@pytest.fixture
def repo_mock():
    return creato_autospec(RepoBD,instance = True) #el mock hereda la firma de RepoB    D
def test_obtener_invoca_repo():
    svc = ServicioNegocio(repo = repo_mock)
    repo_mock.obtener.return_value = {id:1,valor:numero}
    resultado = svc.obtener_transformado(1)
    repo_mock.obtener.assert_called_once_with(1)
    assert resultado == doble_numero
```
## por que es importante respetar LSP en las pruebas?
Permite que los fakes, stub, mock  sean representaciones fieles de los objetos reales.
- Consistencia con el comportamiento real
- Deteccion temprana de errores
- Mantenimiento del contrato

## ejemplo de violacion del LSP y consecuencia
Se modifica la interfaz de RepositorioDB sin actualizar el mock o test
```bash
class RepoBD:
    def obtener(self,id:str)->dict
    def guardar(self,registro:dict)->int
```
Si no se usara create_autospec un mock manual  no podria detectar el cambio
```bash
from unittest.mock import Mock
@pytest.fixture
def repo_mock():
    repo = Mock()
    repo.obtener() = Mock(return_value={id:1,valor:42})
    return repo
```
## Ventajas de usar create_autospec
- Validacion estricta de la interfaz create_autospec asegura que el mock solo exponga los metodos definidos en la clase original y que las firmas de esos metodos tambien
- Reduccion de errores manuales, los mocks manuales so propensos a errores
- Mantenimiento simplificado, cuando la interfaz cambia, los tets fallan automaticamente, eso facilita refactorizacion.
## casos practicos adicionales 
### Agregar un nuevo metodo a RepoBD
```bash
class RepoBD:
    def obtener()
    def guardar()
    def eliminar()
```
Con create_autospec el mock incluye automaticamente el metodo eliminar<br>

### cambiar el tipo de retorno 
```bash
class RepositorioBD:
    def obtener()->list
    def guardar()->int
```
def base_mock():
    return create_autospec(RpeoBD)
Asegura que se actualice
### Mejores practicas para LSP
- usar create_autospec
- validar assert_called_once_with()
- si cambias interfaz actualiza los tests
- considera el uso de interfaces explicitass, 
```bash
class Repositorio(ABC):
    @abstractmethod
    def obtener(self, id_: int) -> dict:
        pass

    @abstractmethod
    def guardar(self, registro: dict) -> int:
        pass

class RepositorioDB(Repositorio):
    def obtener(self, id_: int) -> dict:
        # Implementación real
        pass

    def guardar(self, registro: dict) -> int:
        # Implementación real
        pass
```
# ISP principio de segregacion de interfaces
El ISP implica que cada fixture debe tener una responsabilidad unica y proporcionar solo que un test especifico necesita<br>
Se debe evitar un mega-fixture que cree BD+ usuario + Cliente<br>
```bash
@pytest.fixture def conexion_bd(): ...
@pytest.fixture def usuario_autenticado(conexion_bd):...
@pytest.fixture def cliente_http(app):...
```

# DIP dependency inversion Principle
El servicio depende de abstracciones , no de implementaciones concretas<br>
```bash
class IRepositorioMensajes(Protocol):
    def guardar():

    def obtener_todos():

```
# Metricas y disciplinas DevOps
- Cobertura usar pytest-cov con umbral --fail-under=80
- Flakiness aislar entorno, usar pytest-rerunfailures ó pytest-flakefinder
- Benchmark pytest-benchmark para controlar performance y detectar degradaciones
- Pipelines CI/CD gates automaticos 
  - falla cobertura <80%
  - alerta si prueba es flaky
  - si benchmark empeora >10% falla

# Refactor progresivo(Boy -Scout rule)
- Refactoriza poco a poco
1. Divide tests monoliticas(SRP)
2. Parametriza(OCP)
3. Usa autospec(LSP)
4. Extrae fixtures pequeñas(ISP)
5. Inyecta dependencias(DIP)

# DevSecOps + DIP
fixtures pueden inyectar componentes seguros
- DB solo de lectura 
- Scanner de seguridad (OWASP ZAP, Trivy)
- Proxies para detectar vulneerabilidades