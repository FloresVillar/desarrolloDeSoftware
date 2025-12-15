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


 => [production 3/6] WORKDIR /app                                                              0.1sg                        
 => [production 4/6] COPY --from=builder /root/.local /home/appuser/.local                     0.2s
 => [production 5/6] COPY . /app                                                               0.1s
 => [production 6/6] RUN chown -R appuser:appuser /app                                         2.0s
 => exporting to image                                                                         0.2s
 => => exporting layers                                                                        0.2s
 => => writing image sha256:0b33834d629f55081365923979e9dda198e38c9771cdb0f8839b798ce4f339e0   0.0s
 => => naming to docker.io/library/ejemplo-microservice:0.1.0           
 # imagen creada con un ID unico (SHA256)
 #  y tag asignado ejemplo             
```
## Etiquetado y verificacion 
**Contruccion**
```bash
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio10$ docker build --no-cache -t ejemplo-microservice:0.1.0 .
[+] Building 18.9s (14/14) FINISHED                                                                                                                                                                                                                                  docker:default
 => [internal] load build definition from Dockerfile                                                                                                                                                                                                                           0.0s
 => => transferring dockerfile: 1.21kB                                                                                                                                                                                                                                         0.0s
 => [internal] load metadata for docker.io/library/python:3.12-slim                                                                                                                                                                                                            1.4s
 => [internal] load .dockerignore                                                                                                                                                                                                                                              0.0s
 => => transferring context: 257B                                                                                                                                                                                                                                              0.0s
 => CACHED [builder 1/4] FROM docker.io/library/python:3.12-slim@sha256:b43ff04d5df04ad5cabb80890b7ef74e8410e3395b19af970dcd52d7a4bff921                                                                                                                                       0.0s
 => => resolve docker.io/library/python:3.12-slim@sha256:b43ff04d5df04ad5cabb80890b7ef74e8410e3395b19af970dcd52d7a4bff921                                                                                                                                                      0.0s
 => [internal] load build context                                                                                                                                                                                                                                              0.1s
 => => transferring context: 157.98kB                                                                                                                                                                                                                                          0.1s
 => CACHED [builder 2/4] WORKDIR /build                                                                                                                                                                                                                                        0.0s
 => [production 2/6] RUN groupadd -r appuser     && useradd -m -r -g appuser appuser                                                                                                                                                                                           0.4s
 => [builder 3/4] COPY requirements.txt .                                                                                                                                                                                                                                      0.0s
 => [builder 4/4] RUN pip install --user --no-cache-dir -r requirements.txt                                                                                                                                                                                                   13.9s
 => [production 3/6] WORKDIR /app                                                                                                                                                                                                                                              0.0s
 => [production 4/6] COPY --from=builder /root/.local /home/appuser/.local                                                                                                                                                                                                     0.3s
 => [production 5/6] COPY . /app                                                                                                                                                                                                                                               0.4s
 => [production 6/6] RUN chown -R appuser:appuser /app                                                                                                                                                                                                                         2.2s
 => exporting to image                                                                                                                                                                                                                                                         0.3s
 => => exporting layers                                                                                                                                                                                                                                                        0.2s
 => => writing image sha256:5990bccba33b6fe3accb6cfeae2d8283489944dc9825911b70df3d709366f77d                                                                                                                                                                                   0.0s
 => => naming to docker.io/library/ejemplo-microservice:0.1.0                                                                                                                                                                                                                  0.0s
```
**Ejecucion**
```bash
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio10$ docker run --rm -d --name ejemplo-ms -p 80:80 ejemplo-microservice:0.1.0
7cd2b0679eb53332dee75bba5b884aab2bbc29abd791db56aa3929ce9c01f9ac
```

**Verificacion**
```bash
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio10$ curl -i http://localhost/api/items/
HTTP/1.1 200 OK
date: Sun, 23 Nov 2025 15:40:42 GMT
server: uvicorn
content-length: 68
content-type: application/json

[{"name":"test-item","description":"Descripción de prueba","id":1}]
```
**Logs**
```bash
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio10$ docker logs -n 200 ejemplo-ms
INFO:     Started server process [1]
INFO:     Waiting for application startup.
2025-11-23 15:40:38,894 - INFO - microservice - Arrancando la aplicación
2025-11-23 15:40:38,894 - INFO - microservice - Inicializando base de datos en app.db
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
INFO:     172.17.0.1:36166 - "GET /api/items/ HTTP/1.1" 200 OK
```
**Limpieza**
```bash
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio10$ docker rm -f ejemplo-ms && docker image prune -f
ejemplo-ms
Deleted Images:
deleted: sha256:c30cd3ec36073ac8b957bbba8cf3aed2ee757daeb220ce9861c9f34cf6047bca

Total reclaimed space: 0B
```
**Pruebas**
```bash
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio10$ rm app.db
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio10$ pytest -q
..                                                                                                                                                                                                                                                                           [100%]
================================================================================================================================= warnings summary =================================================================================================================================
../../../../../usr/lib/python3/dist-packages/_pytest/config/__init__.py:1373
  Warning: Unknown config option: python_paths

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2 passed, 1 warning in 0.29s
```