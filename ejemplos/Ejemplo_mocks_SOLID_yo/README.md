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
@pytest.fixture def conexion_bd(): 
    db = SessionLocal()
    yield db
    db.close()

@pytest.fixture def usuario_autenticado(conexion_bd):
    #crea usuario
    user = Usuario()
    conexion_bd.add(usser) , commit
    return user 
@pytest.fixture def cliente_http(app):
    #monta flask FastAPI TestCL
    from fastapi.testclient import TestClient 
    return TestClient(app)
```

1. conexion_db , proporciona solo sesion de bd, interfaz minima
2. usuario_auntenticado, depende del anterior y crea usuario autenticado
3. cliente_http, proporciona cliente http para interactuar con FastApi,sin base de datos o usuarios

## beneficios de aplicar ISP en fixtures 
1. Modularidad
2. Reduccion de acoplamientos
3. MAntenibilidad
4. Eficiencia
5. Claridad

## ejemplo 
```bash
    def test_leer_datos():
        resultado = conexion_db.query(Usuario).all()
        assert len(resultado) == 0

    def test_endpoint_con_autenticacion():
        headers = 
        respuesta = 
        assert respuesta.status_code == 200 
```

Antipatron a evitar
1. 
```bash
    @pytest.fixture
    def entorno_completo():
        db = SessionLocal()
        user = 
        db.add(user)
        db.commit()
        client = TestClient(app)
        client.headers.update({})
        yield db,usr,client
        db.close()
```
Esto obliga a los test a desempaquetar  incluso si solo necesitan uno de los elementos,aunmentando acoplamiento
2. 
Dependencias implicitas
si un fixture asume que otra estara presente sin declararla explicitamente , puede generar errores dificiles de depurar

3. Nombres genericos setup o test_env en lugar de conexion_db  usuario_autenticado reduce claridad

# DIP dependency inversion Principle
El servicio depende de abstracciones , no de implementaciones concretas<br>
Las abstracciones no deben depender de detalles,los detalles deben depender de abstracciones<br>

```bash
#dominio/puertos.py
class IRepo(Protocol):
    @abstractmethod
    def guardar():
    @abstractmethod
    def obtener_todos():


#infra/repos_sqlite.py
from dominio.puertos import IRepo
class RepoSQL(IRepo)

#servicio.py
from dominio.puertos import IRepo
class Servicio:
    def __init__(repo = IRepo):
    def publicar(msg):
        guardar(msg.)

# test/test_servicio..
from servicio
from dominio.puerto

class RepoEnMemoria(IRepo):
    def __init__
    def guardar
    def obtener_todos
def test_publicar_mayusculas():
    repo = RepoEnMemoria
    svc = ServicioMensajeria(repo)
    svc.publicar()
    assert repo.obtener_todos()
```
En el contexto de pruebas unitarias DIP facilita el aislamiento de dependencias.<br>
Recapitulando
```bash
# dominio/puertos.py
from abc import ABC, abstractmethod
from typing import Protocol

class IRepositorioMensajes(Protocol):
    @abstractmethod
    def guardar(self, mensaje: str) -> None: ...
    @abstractmethod
    def obtener_todos(self) -> list[str]: ...

# infraestructura/repos_sqlite.py
import sqlite3
from dominio.puertos import IRepositorioMensajes

class RepoSQLite(IRepositorioMensajes):
    ...

# servicio.py
from dominio.puertos import IRepositorioMensajes

class ServicioMensajeria:
    def __init__(self, repo: IRepositorioMensajes):
        self._repo = repo

    def publicar(self, msg: str) -> None:
        self._repo.guardar(msg.upper())

# tests/test_servicio_mensajeria.py
from dominio.puertos import IRepositorioMensajes
from servicio import ServicioMensajeria

class RepoEnMemoria(IRepositorioMensajes):
    def __init__(self):
        self._datos: list[str] = []
    def guardar(self, mensaje: str) -> None:
        self._datos.append(mensaje)
    def obtener_todos(self):
        return self._datos

def test_publicar_mayusculas():
    repo = RepoEnMemoria()
    svc  = ServicioMensajeria(repo)

    svc.publicar("hola devops")
    assert repo.obtener_todos() == ["HOLA DEVOPS"]
```         
![DIP](imagenes/dip_yo.png)
no pude subir mi imagen asi que gpt hizo lo que pudo
```bash
                 ┌──────────────────────────┐
                 │         IREPO            │
                 │  (funciones abstractas)  │
                 └───┬─────────┬────────┬───┘
                     │         │        │
    ┌────────────────▼┐   ┌────▼────┐  ┌▼─────────────────┐
    │     REPOSQL     │   │ Servicio│  │ RepoEnMemoria(IREPO) │
    │ (implementación)│   │ Mensajería ││  (fake para tests)  │
    └─────────────────┘   │ def __init__(repo: IREPO) │  └─────────────────┘
                          └───────┬────────────┘
                                  │
                                  ▼
                           ┌──────────────┐
                           │    Test      │
                           │ repo = RepoEnMemoria()  │
                           │ ServicioMensajeria(repo)│
                           └──────────────┘

```
en el test , se inyecta repo , el servicioMensajeria publica el mensaje, luego el assert verifica que el fake RepoEnMemoria tenga [MENSAJE] confirmndo que el servicio transforma el mensaje sin escribir en disco.
## beneficios de dip en pruebas
- Aislamiento de dependencias externas; sin dip se necesita Sql real, una conexion a bd o archivos en disco, lo que hace la prueba lenta;con ip se inyecta fake,RepoEnMemoria simula el comportamiento sin side-effects

- velocidad y eficiencia
- Control total sobre el comportamiento , simular escenarios edge-case facilmente, facilita mocks y stubs
-mejora cobertura y mantenibilidad

## Alternativas  y extensiones
- sin dip, self._repo = RepoSQLite()
- dependency_injector
- pruebas de integracion, dip no elimina las pruebas de integracion , dip se usa para pruebas rapidas, valida implementacion concreta
- en otros lenguajes, en java se usan interfaces y spring para di


# Metricas y disciplinas DevOps
En un entorno DevOps , las metricas son esenciales para garantizar la calidad del software y la estabilidad del pipeline<br>


Herramientas como pytets-cov, pytest-benchmark permiten establecer umbrales que actuan como gates<br>

## cobertura de codigo 
la cobertura mide el porcentaje de codigo ejecutado durante las pruebas , pero ha de evitarse los falsos positivos
- cobertura por ramas, --cov-branch se prueba todo , bucles etc

- Exclusion selectiva, 
```bash
[tool.coverage.run]
omit =[ "*/config/*","",""]
```
- integracion CI/CD , githubs o gitactions ci, 

## flakiness (pruebas inestables)
las pruebas inestables son un problema comun que afecta la confianza en el pipeline<br>
Una prueba es flaky si pasa o falla de forma no esperada(determinista)<br>

formas de mitigarlo:
- Aislamiento de pruebas, 
- Reintentos controlados,
- Deteccion de flakiness,
- Trazabilidad, 

## benchmarks de rendimiento
Los benchmark miden el redimiento de funciones criticas.
- umbrales de rendimiento
```bash
def test(benchmark):
    resultado = benchmark.pedantic()
    assert resultado > 0
    assert benchmark < 0.5
```
- comparacion historica, 
```bash
pytest --benchmark-save= --benchmark-compare=
```

## automatizacion en pipeline
el pipeline debe ser el guardian de la calidad , configura gates automaticos:
- cobertura
- flakiness
- rendimiento 

- Cobertura usar pytest-cov con umbral --fail-under=80
- Flakiness aislar entorno, usar pytest-rerunfailures ó pytest-flakefinder
- Benchmark pytest-benchmark para controlar performance y detectar degradaciones
- Pipelines CI/CD gates automaticos 
  - falla cobertura <80%
  - alerta si prueba es flaky
  - si benchmark empeora >10% falla

## Refactor progresivo(Boy -Scout rule)
Refactorizar un suites de pruebas es un desafio, en la estrategia BOY-SCOUT(dejar el codigo mejor de lo que se encontro)<br>
Permite modernizarla incrementalmente sin interrumpir el desarrollo

1. Identificar y mapear pruebas
v   
2. dividir en funciones independientes(SRP)
3. Parametrizar pruebas(OCP)
4. Sustituir dobles con Autospec (LSP)
5. Extraer fixtures granulados
6. Ineyectar dependencias con protocolos(DIP)

# DevSecOps + DIP
fixtures pueden inyectar componentes seguros
- DB solo de lectura 
- Scanner de seguridad (OWASP ZAP, Trivy)
- Proxies para detectar vulnerabilidades