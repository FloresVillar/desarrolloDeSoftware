# Laboratio 10 
Ejecucion de las indicaciones del laboratorio 

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