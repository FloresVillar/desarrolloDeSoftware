# Laboratorio 10 
Ejecucion de las indicaciones del laboratorio 
Se ejecutan las recetas del Makefile 

1. Construir la imagen 
```bash
build:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .  
-----
docker build -t ejemplo-microservice:0.1.0 .
# algo de sintaxis , vamos , que nunca esta de más
# docker es el cliente CLI que que 'hablará´con el demonio docker (Docker engine)
#-t nombre:etiqueta
# y el punto que indica que el contexto de build (Dockerfile) es el directorio actual
```

2. Arrancar el contenedor
```bash
run:
	docker run -d \
		-p 80:80 \
		--name $(IMAGE_NAME) \
		$(IMAGE_NAME):$(IMAGE_TAG)

docker run -d \
  --name ejemplo-ms \
  -p 80:80 \
  ejemplo-microservice:0.1.0

bc54d6b3a574fcf2c379e5eb382743b170a74bce5ae7c3285d2692061b7cf290
```
3. Verificando que responde
```bash
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio10$

curl -i http://localhost/api/items
HTTP/1.1 307 Temporary Redirect
date: Sun, 14 Dec 2025 17:14:29 GMT
server: uvicorn
content-length: 0
location: http://localhost/api/items/
#la consulta fue echo hacia localhost quien accede al puerto 80(host)→80(contenedor) de modo que vamos al endpoint del servicio que corre dentro del container ya en estado run

```

4. Depurar 

```bash 
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio10$
 
docker logs -f ejemplo-microservice

INFO:     Started server process [1]
INFO:     Waiting for application startup.
2025-12-14 17:03:36,574 - INFO - microservice - Arrancando la aplicación
2025-12-14 17:03:36,574 - INFO - microservice - Inicializando base de datos en app.db
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
INFO:     172.17.0.1:36286 - "GET /api/items HTTP/1.1" 307 Temporary Redirect
# como se aprecia con la bandera de seguimiento se escucha constantemente

esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio10$ 

docker exec -it ejemplo-microservice /bin/bash
# i (modo iteractiva) y t (para obtener un terminal) y desde luego comando que ejecutamos /bin/bash (linea de comandos )
appuser@bc54d6b3a574:/app$ ls
Dockerfile  Instrucciones.md  Makefile  app.db  apuntes.txt  microservice  pytest.ini  requirements.txt  tests  venv_labo10
appuser@bc54d6b3a574:/app$ 
```

5 . Detener  y limpiar 
```bash
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio10$ 

docker stop ejemplo-microservice
ejemplo-microservice

esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio10$ 

docker rm -f ejemplo-microservice
ejemplo-microservice
# elimina el contenedor
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio10$ 

docker image prune -f
Total reclaimed space: 0B
#limpia imagenes
```
## Publicar 
La siguiente receta es muy interesante ,el uso de los comandos tag y push etiquetan  y publican nuestra imagen respectivamente.
```bash
IMAGE_NAME := ejemplo-microservice
REGISTRY=ghcr.io/tu-org 
IMAGE_TAG=0.1.0

docker tag $(IMAGE_NAME):$(IMAGE_TAG) $(REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG)

docker tag ejemplo-microservice:0.1.0 ghcr.io/tu-org/ejemplo-microservice:0.1.0

docker push $(REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG)

docker push ghcr.io/tu-org/ejemplo-microservice:0.1.0
# lo subimos (nuestra imagen creada ) al GitHub Container Registry  
```
## Conceptualizacion de microservicios
## monolito → SOA → Microservicios

Una aplicacion donde toda la logica vive en un solo proyecto (codigo, memoria)  → SOA divide el sistema en servicios, pero gobernados por una arquitectura comun usa ESB(enterprise service bus) un intermediario para enrutar mensaje. EBS se convierte en un cuello de botella →   Microservicios : Cada microservicio es una componente distinta , con una funcionalidad clara, incluso su propia base de datos. Esto permite desplegar cambios de manera aislada.

Un monolito se puede volver costoso de operar, por ejemplo un **e-commerce** con picos en temporadas como un **black-friday** el modulo de comprar(carrito) tendra un sobrcarga de uso en tanto que la modificacion de perfiles tanto. En un monolito , escalar  = duplicar toda la aplicacion , un error en un modulo colapsaria todo el sitio

Un ejemplo adicional es un SaaS multi tenant que permite que muchos clientes compartan la plataforma, si un cliente usa muchos recursos afecta a los otros. 

Como se ve el monolito e incluso el SOA presentan problemas de escalamiento , no son resilientes ni flexibles, cosa que los microservicios solventan muy bien.

## Criticas al monolito
Como se menciona, escalan mal. 
**Cadencia de despliegue reducida**(muy tecnico por cierto)  cualquier cambio requiere que todo el repo se actualice(redeploy) , tambien presenta un fuerte aacoplamiento que impide escalar de forma independiente las partes que solo se necesiten escalar.

## Popularidad de los microservicios
Empresas como neflix , Amazon  y Soptify, las ofertantes de streaming. Una de las caracteristicas es que los microservicios permiten aislar fallas y a escalar pequeños cambios(granularidad)

## Desventajas y retos 
Orquestacion

Consistencia de datos

Testing distribuidos

## Principios de diseño
DDD : Diseño guiado por el dominio, que introduce limites contextuales , delimitando las responsabilidades de cada servicio. Esto ayuda a evitar superposicion de funcionalidades. 

DRY (don´t repeat yourself) ,se acepta cierta duplicacion controlada para reducir acoplamiento y mantener la independencia de cada servicio

Respecto a la cantidad de responsabilidad , pues esta refleja la naturaleza de cada servicio. El sistema de pago por ejemplo sera mayor que el de login.

## Empaquetado y verificacion 

```bash
# construccion
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio10$ docker build --no-cache -t ejemplo-microservicio:0.1.0 .
[+] Building 27.2s (14/14) FINISHED                                                                       docker:default
 => [internal] load build definition from Dockerfile                                                                0.0s
 => => transferring dockerfile: 1.24kB                                                                              0.0s 
 => [internal] load metadata for docker.io/library/python:3.12-slim                                                 1.9s 
 => [internal] load .dockerignore                                                                                   0.0s
 => => transferring context: 257B                                                                                   0.0s 
 => CACHED [builder 1/4] FROM docker.io/library/python:3.12-slim@sha256:fa48eefe2146644c2308b909d6bb7651a768178f84  0.0s 
 => [internal] load build context                                                                                   0.1s 
 => => transferring context: 120.77kB                                                                               0.1s
 => CACHED [builder 2/4] WORKDIR /build                                   
 
 ....

 => => exporting layers                                                                                 0.3s 
 => => writing image sha256:a9d2c178286f820106facf8cd785178c7981078598a07b24bb766ee96b222a32                        0.0s 
 => => naming to docker.io/library/ejemplo-microservicio:0.1.0                                        
```

```bash
#mapear el puerto 80:80 host:contenedor
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio10$ docker run --rm -d --name ejemplo-ms -p 80:80 ejemplo-microservice:0.1.0
260bbbb0e51829afbadc2eb5018f9f333e5429cef4aa37cb7045d8df1ffaf372
```

```bash
# Verificacion http
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware$ curl -i http://localhost/api/items/
HTTP/1.1 200 OK
date: Sun, 14 Dec 2025 22:13:49 GMT
server: uvicorn
content-length: 68
content-type: application/json

[{"name":"test-item","description":"Descripción de prueba","id":1}]
```
En este punto un detalle que no se ve claramente , porque el dominio es localhost? , en que linea de codigo se define eso? , en el Dockefile quizas ? en la construccion de la imagen o en el levantamiento del contenedor?. Veamos, localhost es nuestra propia maquina, es un alias de nuestro sistema operativo. (127.0.0.1 definido /etc/hosts/). curl://localhost:80 indica a nuestro OS dirigirse a 127.0.0.1 en el puerto 80, luego el comando  **docker run -p 80:80 ejemplo-microservicio:0.1.0** dentro de este contenedor nuestra app escucha en 0.0.0.0:80  en todas las interfaces ( grupos de ip, simplificando el termino)del contenedor , docker crea una regla NAT que conecta el puerto 80 host con el 80 contenedor, como docker expone el puerto en 0.0.0.0 cualquier interfaz de nuestra maquina que reciba trafico en este puerto(80 del host) lo redirige al contenedor .
Si localhost (127.0.0.1) recibe una peticion en el puerto 80 , lo redirige al CONTENEDOR. 
```bash
[Tu navegador o curl]
       |
       v
[localhost:80 en Host]   <-- Docker NAT mapea puerto -->
       |
       v
[Contenedor Docker: 0.0.0.0:80]
       |
       v
[Tu aplicación → rutas como /api/items/]

```

```bash
#logs
e$ docker logs -n 200 ejemplo-ms
INFO:     Started server process [1]
INFO:     Waiting for aspplication startup.
2025-12-14 21:53:28,748 - INFO - microservice - Arrancando la aplicación
2025-12-14 21:53:28,748 - INFO - microservice - Inicializando base de datos en app.db
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
INFO:     172.17.0.1:44342 - "GET /api/items/ HTTP/1.1" 200 OK
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware$
```


```bash
#  limpieza
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware$ docker rm -f ejemplo-ms && docker image prune -f
ejemplo-ms
Total reclaimed space: 0B
# se detalló su sintaxis antes
```

## Base de datos : SQLite 


## Pruebas pytest -q
```bash
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio10$ pytest -q                                                                     [100%]
======================================================================== FAILURES =========================================================================
___________________________________________________________ test_create_item_and_verify_in_list ___________________________________________________________

client = <starlette.testclient.TestClient object at 0x7539605912b0>

    def test_create_item_and_verify_in_list(client):
        """
        1) Crea un ítem          -> 201 Created
        2) Devuelve los datos    -> nombre y descripción coinciden
        3) El ítem aparece luego en el listado general
        """
        payload = {"name": ITEM_NAME, "description": ITEM_DESCRIPTION}
        create_resp = client.post("/api/items", json=payload) #crea
>       assert create_resp.status_code == 201 # verifica
E       assert 400 == 201
E        +  where 400 = <Response [400 Bad Request]>.status_code

tests/test_api.py:36: AssertionError
------------------------------------------------------------------ Captured stdout call -------------------------------------------------------------------
2025-12-14 22:02:10,777 - ERROR - microservice - Error al crear ítem
Traceback (most recent call last):
  File "/home/esau/desarrolloDeSoftware/labs/Laboratorio10/microservice/api/routes.py", line 45, in create_item
    created = business_logic.create_item(item.name, item.description)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/esau/desarrolloDeSoftware/labs/Laboratorio10/microservice/services/business_logic.py", line 15, in create_item
    item_id = database.add_item(name, description)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/esau/desarrolloDeSoftware/labs/Laboratorio10/microservice/services/database.py", line 53, in add_item
    cursor.execute(
sqlite3.IntegrityError: UNIQUE constraint failed: items.name
---------------------------------------------------------------- Captured stdout teardown -----------------------------------------------------------------
2025-12-14 22:02:10,808 - INFO - microservice - Deteniendo la aplicación
==================================================================== warnings summary =====================================================================
../../../../../usr/lib/python3/dist-packages/_pytest/config/__init__.py:1373
  Warning: Unknown config option: python_paths

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================================================================= short test summary info =================================================================
FAILED tests/test_api.py::test_create_item_and_verify_in_list - assert 400 == 201
1 failed, 1 passed, 1 warning in 0.44
```
Como es de esperar **def test_healthcheck_items_endpoint(client)** quien solo lista (GET) los elementos de la tabla, pasa el test. Si embargo **def test_create_item_and_verify_in_list(client)** no pasa el test,  pues se solicita (POST) la creacion de una nueva fila en la tabla de datos , particularmente **payload = {"name": ITEM_NAME, "description": ITEM_DESCRIPTION}** , luego esta peticion llega a routes, quien para el prefijo /api/item posee un metodo post , que a su vez llama a logica de negocio, quien hace lo propio redirigiendo la peticion hacia la base de datos donde se tiene 
```bash
CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE, # no puede repetirse el nombre
                description TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
```
Algo mas de teoria (cortesia de GPT ) : La causa fundamental es que las pruebas de integración están compartiendo estado mutable. La base de datos SQLite utilizada por la aplicación es la misma para todos los tests y no se reinicia entre ellos. Esto viola una propiedad esencial de cualquier suite de pruebas: cada test debe poder ejecutarse de manera independiente, en cualquier orden, y producir siempre el mismo resultado

Qué demuestra esto sobre el tipo de prueba

Este comportamiento confirma que estás ejecutando una prueba de integración real. No hay mocks, no hay stubs y no hay aislamiento artificial. Están interactuando rutas HTTP reales, lógica de negocio real y una base de datos real. Precisamente por eso emergen este tipo de problemas, que no aparecerían en pruebas unitarias.

Qué suposición incorrecta hace el test

El test asume implícitamente que el sistema comienza en un estado vacío. Esa suposición no está garantizada por la infraestructura actual. La base de datos conserva datos de ejecuciones anteriores y, por tanto, el entorno no es limpio al inicio del test.

## Semver por sobre lastest
En palabras la misma variable (nombre lastest) puede ser la version A, version B ,no necesariamente será la imagen que queramos.

## Desarrollo y despliegue
Docker compose :declaratividad, gestión automática de redes, dependencias entre servicios, soporte para perfiles (profiles) y entornos reproducibles

Conceptos clave: services, volumes, networks, depends_on, variables de entorno, bind mounts (para recarga en vivo) vs named volumes (para datos persistentes)

1.
- Staging local : En un entorno real, un microservicio (aunque simple) depende de otros componentes, una base de datos, un sistema cache , un gateway. En produccion estos sistemas son independientes y conectados por la red.
Docker compose permite replicar esa topologia en una maquina local mediante un unico archivo declarativo.En docker-compose.yml se describen explicitamente los servicios , imagenes , variables. Y se ejecutan con una sola instruccion docker compose up . 
Eliminamos ,de esta forma, la divergencia entre entornos. 
- Pruebas de integracion , se busca validar el comportamiento de los componentes interactuando entre si. Para comprobar que una API escribe correctamente en Redis o que una transaccion persiste datos en una tabla SQL, lo que antes se hacia era instalar todo esto, pero con docker-compose podemos oequestar dependencias reales con contenedores efimeros. Cualquier servicio se declara y se conmfigura. De modo que las pruebas de integracion es un proceso determinista y repetible. 

- Recarga en vivo. Detener un contenedor  , reconstruir la imagen y volver a ejecutarla rompe el flujo de trabajo . Docker compose permite el uso de bind mounts, un montaje directo del codigo fuente del host dentro del contenedor.De modo que el contenedor ejecuta el servidor de desarrollo (uvicorn --reload) mientras el codigo reside fisicamente en el sistema de desarrollo. Ante cada cambio el interprete dentro del contenedor deetecta el cambio  y recarga automaticamente la aplicacion. Docker compose se convierte en un facilitador de desarrollo diario.

2. El uso de perfiles, nos permiten controlar que servicios y configuraciones se activan segun el contexto de ejecucion . 
Permiten la separacion explicita de entornos. (dev vs test). En desarrollo : el foco es la productividad, se recarga "en  caliente" (uvicorn --reload) bin mounts para editar el codigo sin reconstruir imagenes . En testing : reproducibilidad, aislamiento. <br>
Los perfiles permiten declarar esta diferencia de forma estructurada. Se activan via 
```bash
services:
  api:
    image: ejemplo-microservice
    ports:
    profiles:
      - dev
  api-test:
    image: ejemplo-microservice
    command: pytest -q
    profiles:
      - test
# y ejecutan 
docker compose --profile dev up
docker compose --profile test up
```
3. Fragmento conceptual de docker-compose.yml 
- Servicio Api ,se construye a partir de una imagen **imagen: ejemplo-microservice:0.1.0** , exposicion de puertos **ports: 8080:80** enturando el puerto 8080 del host al puerto 80 del contenedor. El bind mount para la edicion en vivo **volumes: - ./app:/app** , montamos en caliente nuestro directorio app dentro del directorio app del contenedor.Finalmente el campo command para **command: uvicorn main:app --reload --host 0.0.0.0 --port 80** , con modulo:objeto ASGI(fastapi).


- Redis (cache) se declara como un servicio dentro del campo services, con sus propios campos **image:redis:7 , expose: "6379"** imagen y puerto que expone respectivamente.


- Relacion entre servicios, api y cache se comunican dentro de la red de compose. **API → redis://cache:6379** , esta dependencia se declara con el campo depends_on en **services: api : depends_on: - redis** para **redis: image: redis:7**

**comandos clave**<br>
```bash
docker compose up --build
docker compose logs -f api
docker compose down --volume
```
**comunicacion entre microservicios**<br>
REST: (Representational State Transfer) se apoya en HTTP como protocolo de transporte, suele usar json . Cualquier lenguaje puede consumir una API REST sin dependencias especiales.

gPRC: framework que usa http2 y protocol Buffers(ProtoBuf) con contrato definido en .proto. El uso de binario reduce drastiamente el tamaño de los mensajes y, junto con hhtp/2 posibilita la multiplexacion y el streaming bidireccional.

RabbitMQ : message Broker tradicional basado en colas,e mensaje se envia a una cola, un consumidor los procesa y confirma que la ha consumido(ACK) , luego el mensaje se elimina. Modelo ideal para tareas asincronicas; el mensaje debe ser consumido una sola vez. "Entrega confiable, no historial de mensajeria"

Kafka : Es un log distribuido ,los mensajes se escriben en TOPICS particionados y se conservan durante un tiempo configurable .El orden esta garantizado por particion , no globalmente, multiples consumidores pueden leer el mismo mensaje. Kafka es adecuado para arquitecturas orientadas a eventos **event sourcing** , donde se require replay , retencion a largo plazo y alta escalabilidad horizontal

**ejercicios**

1. gRPC superior a REST, (cortesia de la IA)
**En un sistema de procesamiento de transacciones financieras en tiempo real, donde se manejan miles de operaciones por segundo, los mensajes tienen estructura bien definida y existe la necesidad de streaming continuo (por ejemplo, cotizaciones o confirmaciones), gRPC resulta claramente superior. La serialización binaria reduce el tamaño de los payloads, el contrato evita ambigüedades y el soporte de streaming bidireccional permite flujos eficientes que REST simplemente no puede ofrecer sin capas adicionales.**

2. Kafka > > RabbitMQ 
**En un sistema de auditoría de eventos de dominio, como OrderCreated o PaymentProcessed, Kafka es la opción natural. Estos eventos no solo deben ser consumidos en tiempo real, sino también reprocesados por nuevos servicios (fraude, analítica, notificaciones) meses después. Kafka permite retener los eventos, garantizar orden por entidad (mediante particiones) y soportar múltiples consumidores sin duplicar la lógica de publicación.**

3. Plan de pruebas con stubs
```bash
def test_creacion_item_dependencia_externa():
  mocked_reponse.post("http://ENDPOINT",json={DESCRIPCION})
  respuesta = client.post("/api/items",json={"name":"test"})
  assert respuesta.status_code == 201 
```
Antes se incluyen algunas librerias en **requirements.txt** tales como responses y httpx, luego redefinimos el test_ de la siguiente manera
```bash
from httpx import MockTransport
import responses
def test_mock_inventorio(client):
    responses.post("http://inventory/api/stock",json={"disponible":True},status = 200)
    payload = {"name":"test", "descripcion":"mocked"}
    respuesta = client.post("api/items",json=payload)
    assert respuesta.status_code == 201
```
Ahora bien, el contenedor ya esta creado via previa limpieza , merced a las recetas del makefile 
make stop  que detiene el contenedor
make clean que realiza la limpieza de las imagenes incluido, y via make run , que tiene build como prerrequisito.Entonces , con el contenedor ya construido  se ejecuta **docker exec ejemplo-microservice:0.1.0 pytest -q** , lo cual resulta en 2 test passed y 1 failed(de nuevo el que tiene que ver con el acceso a la base de datos para la creacion de una linea con el mismo nombre)
```bash
def test_mock_inventorio(client):
    responses.post("http://inventory/api/stock",json={"disponible":True},status = 200)
    payload = {"name":"test", "descripcion":"mocked"}
    respuesta = client.post("api/items",json=payload)
    assert respuesta.status_code == 201
```

```bash
docker exec ejemplo-microservice py
test -q
..F                                                                      [100%]
=================================== FAILURES ===================================
_____________________ test_create_item_and_verify_in_list ______________________

client = <starlette.testclient.TestClient object at 0x7b2bf2a63170>

    def test_create_item_and_verify_in_list(client):
        """
        1) Crea un ítem          -> 201 Created
        2) Devuelve los datos    -> nombre y descripción coinciden
        3) El ítem aparece luego en el listado general
        """
        payload = {"name": ITEM_NAME, "description": ITEM_DESCRIPTION}
        create_resp = client.post("/api/items", json=payload) #crea
>       assert create_resp.status_code == 201 # verifica
E       assert 400 == 201
E        +  where 400 = <Response [400 Bad Request]>.status_code

tests/test_api.py:43: AssertionError
----------------------------- Captured stdout call -----------------------------
2025-12-15 14:33:52,012 - ERROR - microservice - Error al crear ítem
Traceback (most recent call last):
  File "/app/microservice/api/routes.py", line 45, in create_item
    created = business_logic.create_item(item.name, item.description)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/microservice/services/business_logic.py", line 15, in create_item
    item_id = database.add_item(name, description)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/microservice/services/database.py", line 53, in add_item
    cursor.execute(
sqlite3.IntegrityError: UNIQUE constraint failed: items.name
------------------------------ Captured log call -------------------------------
ERROR    microservice:routes.py:48 Error al crear ítem
Traceback (most recent call last):
  File "/app/microservice/api/routes.py", line 45, in create_item
    created = business_logic.create_item(item.name, item.description)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/microservice/services/business_logic.py", line 15, in create_item
    item_id = database.add_item(name, description)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/microservice/services/database.py", line 53, in add_item
    cursor.execute(
sqlite3.IntegrityError: UNIQUE constraint failed: items.name
--------------------------- Captured stdout teardown ---------------------------
2025-12-15 14:33:52,036 - INFO - microservice - Deteniendo la aplicación
---------------------------- Captured log teardown -----------------------------
INFO     microservice:main.py:39 Deteniendo la aplicación
=============================== warnings summary ===============================
../home/appuser/.local/lib/python3.12/site-packages/_pytest/config/__init__.py:1448
  /home/appuser/.local/lib/python3.12/site-packages/_pytest/config/__init__.py:1448: PytestConfigWarning: Unknown config option: python_paths

    self._warn_or_fail_if_strict(f"Unknown config option: {key}\n")

../home/appuser/.local/lib/python3.12/site-packages/pydantic/fields.py:814
../home/appuser/.local/lib/python3.12/site-packages/pydantic/fields.py:814
  /home/appuser/.local/lib/python3.12/site-packages/pydantic/fields.py:814: PydanticDeprecatedSince20: Using extra keyword arguments on `Field` is deprecated and will be removed. Use `json_schema_extra` instead. (Extra keys: 'example'). Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.8/migration/
    warn(

microservice/main.py:24
  /app/microservice/main.py:24: DeprecationWarning:
          on_event is deprecated, use lifespan event handlers instead.

          Read more about it in the
          [FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).       

    @app.on_event("startup")

../home/appuser/.local/lib/python3.12/site-packages/fastapi/applications.py:4495
../home/appuser/.local/lib/python3.12/site-packages/fastapi/applications.py:4495
  /home/appuser/.local/lib/python3.12/site-packages/fastapi/applications.py:4495: DeprecationWarning:
          on_event is deprecated, use lifespan event handlers instead.

          Read more about it in the
          [FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).       

    return self.router.on_event(event_type)

microservice/main.py:33
  /app/microservice/main.py:33: DeprecationWarning:
          on_event is deprecated, use lifespan event handlers instead.

vv                                                           d          Read more about it in the
          [FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).       

    @app.on_event("shutdown")

tests/test_api.py::test_mock_inventorio
  /home/appuser/.local/lib/python3.12/site-packages/httpx/_client.py:690: DeprecationWarning: The 'app' shortcut is now deprecated. Use the explicit style 'transport=WSGITransport(app=...)' instead.
    warnings.warn(message, DeprecationWarning)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
FAILED tests/test_api.py::test_create_item_and_verify_in_list - assert 400 ==...
1 failed, 2 passed, 8 warnings in 0.99s
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio10$ c
```


**Despliegue kubernetes local**
Teniamos contenedores levantados via docker( o docker-compose) ahora introducimos Kubernetes
un breve esquema de como actua kubernetes(cortesia de GPT)
```bash
┌──────────────────────────────────────────┐
│            MANIFIESTO YAML               │
│                                          │
│ kind: Deployment                         │
│ spec:                                   │
│   replicas: 2                            │
│   template:                             │
│     spec:                               │
│       containers:                       │
│       - name: ejemplo-ms                │
│         image: ejemplo-ms:0.1.0  ─────┐ │
└────────────────────────────────────────┘ │
                                           │
                                           │ (1) Declaración, NO acción
                                           ▼
┌──────────────────────────────────────────┐
│        KUBERNETES (API SERVER)            │
│                                          │
│ "Ok, cuando cree un Pod..."               │
│ "usaré una imagen llamada:"               │
│                                          │
│     ejemplo-ms:0.1.0                      │
│                                          │
└──────────────────────────────────────────┘
                   │
                   │ (2) Kubernetes NO construye
                   │ (2) Kubernetes NO busca en tu PC
                   │ (2) Kubernetes NO ejecuta Docker
                   ▼
┌──────────────────────────────────────────┐
│        RUNTIME DEL NODO (containerd)      │
│                                          │
│ ¿Existe la imagen localmente?             │
│   ├─ SÍ → crear contenedor                │
│   └─ NO → intentar pull del registry      │
│                                          │
└──────────────────────────────────────────┘
                   │
                   │ (3) Si el pull falla
                   ▼
┌──────────────────────────────────────────┐
│             ERROR DEL POD                 │
│                                          │
│ ImagePullBackOff                          │
│ ErrImageNeverPull                         │
│                                          │
└──────────────────────────────────────────┘

```
De modo que los comandos 
```bash
  docker build     # construye la imagen 
  kind load docker-image   # hace la imagen visible al cluster
  kubeclt apply  # declara el estado deseado 

```
Ahora **minikube docker-env** , exporta las variables de entorno haciendo que variables como **export DOCKER_HOST=tcp://127.0.0.1:32770export DOCKER_TLS_VERIFY=1
export DOCKER_CERT_PATH=/home/user/.minikube/certs
export MINIKUBE_ACTIVE_DOCKERD=minikube
**  queden en el shell , luego del docker build , hacemos que Docker Cli se conecte con el daemon de kubernetes y no con el del docker(como se venia haciendo) , sucede algo muy similar a 
```bash
(1) Usuario ejecuta:
    eval $(minikube docker-env)
        |
        |  (exporta variables de entorno)
        v
┌────────────────────────────────────────────┐
│  TU SHELL (bash/zsh)                        │
│                                            │
│  DOCKER_HOST=tcp://127.0.0.1:32770          │
│  DOCKER_TLS_VERIFY=1                        │
│  DOCKER_CERT_PATH=~/.minikube/certs         │
│                                            │
└────────────────────────────────────────────┘
        |
        |  docker build
        v
Docker CLI
        |
        |  lee variables de entorno
        |  (NO sabe qué es minikube)
        v
SOCKET TCP en el HOST (127.0.0.1:32770)
        |
        |  NAT / tunnel / proxy (minikube)
        v
┌─────────────────────────────┐
│  MINIKUBE VM / CONTAINER    │
│                             │
│  dockerd  ← daemon real     │
│  containerd                 │
│  kubelet                    │
└─────────────────────────────┘

```

- manifiestos minimos
  - Deployment
  - livenessProbe
  - Service
Respecto a los manifiestos minimos esto declararlos es mucho mas amigable que entender lo  anterior que es casi transparente.
```bash
apiVersion: ..
kind: Deployment # tipo reconocido y admitido por kubernetes
spec: 
  replicas: 2 # aceptable 
  spec:
..
```
Antes entendamos que el Deployment (el archivo yml/ manifiesto) es una plantilla de pods <br>
Mientras que spec la especificacion (el estado deseado) , en tanto spec.template detalla el "como debe ser cad pod" <br>
spec.spec es la definicion del pod propiamente. 
````bash`
Deployment.spec            ← reglas del Deployment
Deployment.spec.template   ← definición del Pod
Deployment.spec.template.spec ← definición de CADA POD
``` 
Luego los campos que definen a cada contenedor estaran dentro de spec.template.spec
```bash
spec:                      # spec DEL DEPLOYMENT
  replicas: 2

  template:                # PLANTILLA DE POD
    metadata:
      labels:
        app: ejemplo-ms

    spec:                  # spec DEL POD
      containers:          # ← aquí empiezan los contenedores
        - name: ejemplo-ms
          image: ejemplo-ms:0.1.0
          imagePullPolicy: IfNotPresent

```
En tanto que los probes son propiedades de los contenedores, no del pod ni del deployment.
```bash
Deployment
│
├── spec
│   ├── replicas
│   └── selector
│
└── template
    ├── metadata
    │   └── labels
    │
    └── spec          ← POD
        └── containers
            └── ejemplo-ms
                ├── image
                ├── ports
                ├── readinessProbe
                └── livenessProbe

```
Finalmente el manifiesto 
```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ejemplo-ms
spec:
  replicas: 2                     # 2 pods (alta disponibilidad básica)
  selector:
    matchLabels:
      app: ejemplo-ms
  template:
    metadata:
      labels:
        app: ejemplo-ms
    spec:
      containers:
        - name: ejemplo-ms
          image: ejemplo-ms:0.1.0  # imagen local cargada en kind/minikube
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 80

          # --- Health checks ---
          readinessProbe:
            httpGet:
              path: /health
              port: 80
            periodSeconds: 10
            failureThreshold: 3

          livenessProbe:
            httpGet:
              path: /health
              port: 80
            periodSeconds: 10
            failureThreshold: 3
```
En tanto el manifiesto para el servicio, con ind: service
```bash
apiVersion: v1
kind: Service
metadata: 
  name : ejemplo-ms
spec:
  type: NodePort
  selector: 
    app: ejemplo-ms
  ports:
    - port : 80
      targetPort : 80
      nodePort: 

```
Entonces para poder usar kubernetes, instalammos primero el cliente de Kubernetes(kubectl) 
```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubctl /usr/local/bin
```
Luego instalamos minikube
```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
chmod +x minikube-linux-amd64
sudo mv minikube-linux-amd64 /usr/local/bin/minikube
```
Y arrancamos con especificaciones de memoria minima(wsl)
```bash
minikube start --drive=docker --memory=1800 --cpus=4
```

Ejercicios 
1 ,2, 3

OKAY retomando la solucion de esta actividad, no quedaban muy claros los pasos. Para el uso de minikube , los PASOS COMPLETOSjnnnnnnnnnmjkp´+1
```bash
minikube start #arrancar el cluster
kubectl get nodes # ver info
eval $(minikube docker-env) # usar docker del cluster
docker info | grep -i minikube # info
docker build -t ejemplo-ms:0.1.0 . #construir imagen
#creamos los manifiestos.
docker images | grep ejemplo-ms # info
kubtctl apply -f k8s/ # deploy  y service, corregir los manifiestos...
kubectl get pods #viendo los pods
kubectl get endpoints ejemplo-ms # info
minikube service ejemplo-ms --url #exponer servicio
curl http://127.0.0.1:46621/pi/items/  #probar
kubectl get pods
kubectl logs -l app=ejemplo-ms #logs
kubectl scale deployment ejemplo-ms --replicas=4 #escalado
kubectl delete pod .pod-name..
```
Las correcciones hechas en los manifiestos, en deployment  y en service
```bash
Pod
 └── labels (qué soy)

Deployment
 └── selector.matchLabels (qué Pods controlo)

Service
 └── selector (a qué Pods envío tráfico)

```
Y probando :
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio10$ curl http://127.0.0.1:42325/api/items/
[{"name":"test-item","description":"Descripción de prueba","id":1}]

