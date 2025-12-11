# Actividad18 - CC3S2
Este laboratorio usa el Laboratorio 9, por lo que ejecutamos sus instrucciones en primer lugar
Antes de empezar
```bash
#.env.example →→ .env 
--------------------------------------------------------------
POSTGRES_USER=etl_user
POSTGRES_PASSWORD=etl_password_local
POSTGRES_DB=etl_db
AIRFLOW_UID=50000

SQLALCHEMY_CONN=postgresql+psycopg2://etl_user:etl_password_local@postgres:5432/etl_db
# Ruta de entrada del CSV para el ETL
ETL_INPUT=/app/data/input.csv
---------------------------------------------------------------

#de modo que en docker-compose 
---------------------------------------------------------------
  postgres:
    image: postgres:13
    restart: unless-stopped
    env_file: .env ←← nuestras variables de entorno
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
# estas son las variables de entorno para acceder a la base de datos
# de modo que en healthcheck por ejemplo via conexion psycop2.connect usamos estas variables  (como credenciales?)
---------------------------------------------------------------------
conn = psycopg2.connect(
            dbname=os.environ["POSTGRES_DB"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            host=os.environ.get("POSTGRES_HOST", "postgres"),
            port=os.environ.get("POSTGRES_PORT", "5432"),
            connect_timeout=3,
        )
```
Luego continua el arranque en 3 pasos, con las recetas build , reset-init  y up.Cada una de ellas es muy interesante
```bash
build:
    docker --no-cache(RECONSTRUYE) -t $(IMAGEN) ./app(RUTA DEL CONTEXT) 
# en este caso se define la ruta del contexto del build
    docker --no-cache -t $(AIRFLOW_IMG) -f airflow/Dockerfile .
# usamos un Dockerfile especifico y el contexto 
#Analizando un poco las banderas de los comandos , ambos se dirigen al contexto docker de sus respectivos Dockerfile, en esencia hacen (salvo las capas en especifico) lo mismo.

```
```bash
reset-init:
    ./scripts/airflow_reset_init.sh 
# ejecutamos un script de bash
# los comentarios son muy claros, 
```
Sin embargo hay muchisimo que decir acerca de airflow, comenzando por lo que es, una plataforma que organiza flujos de trabajo(workflows). Con el podemos crear workflows complejos , programar tareas, monitorear pipelines, automatizar ETL´s 
En el caso particular del laboratorio9 , lo que se hace es, para la construccion de la imagen dentro del contenedor donde correrá nuestro servicio airflow 
```bash
COPY airflow/dags /opt/airflow/dags
COPY app          /opt/airflow/app
# de modo que el contenido de airflos/dags/etl_dag.py estara en esa ruta dentro de la mv airflow dentro del contenedor, ese script contiene a defincion de nuestro DAG precisamente
--------------------------
Dockerfile(FROM apache/airflow:2.9.1-python3.11)  /opt/airflow/dags   ←←←←←←← airflow/dags  ( DAG ) 

---------------------------
with DAG( #metadata airflow
    dag_id="etl_pipeline_demo",
    start_date=datetime(2025, 1, 1),
    schedule="@daily", # ejecutado diariamente
    catchup=False,
    default_args={"owner": "devsecops"},
    tags=["devsecops", "etl"],
):
    run_etl_task = PythonOperator(
        task_id="run_etl",  # esta es la tarea
        python_callable=run_etl,
    )
# la tarea esta definida en /app/pipeline.py que tambien fue copiado a la imagen via Dockerfile.run_etl ejecuta secuencialemte 3 tareas(funciones) 
def run_etl():
    df_raw = extract()
    df_clean = transform(df_raw)
    load(df_clean)

        EN EL CONTENEDOR AIRFLOW
 -------------------------------------------
| /opt/airflow/dags     "/opt/airflow/app"  |
|task_id="run_etl" ←←←← run_et()            |
 -------------------------------------------

```
Entonces cuando el contenedor es levantado(junto a otros) via docker compose up -d , Airflow levantarpa sus servicios : webserver scheduler workers
```bash
docker compose build
↓ 
Dockerfile(FROM imagen airflow)  /opt/airflow/dags   ←←←←←←← airflow/dags  ( DAG )
↓
Airflow scheduler, webserver, workers
```
Desde luego hay mucho mas que detallar , incluyendo los principios tecnicos subyacentes, con todo y muy  a mi pesar, el tiempo es el peor enemigo.Sin embargo se entiende el porque y como encaja airflow en el proeyecto y de momento eso es ligeramente suficiente.
En ese sentido **make reset-init** levanta un contenedor temporal 
```bash
# levanta un contenedor temporal
docker compose run --rm -e AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=$DB_URL airflow-webserver bash -lc

# ejecuta dos comandos , borrando la metadata y  recrea las datas airflow

airflow db reset -y &&
    airflow db init &&

# para luego crear un usuario con todos atributos (opciones)
airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \
  --password admin || true

```
La siguientes recetas son mucho mas directas
```bash
.PHONY: up
up:                 
	docker compose up(SERVICIOS ) --build(RECONSTRUYE IMAGENES) -d (SEGUNDO PLANO)    
PHONY: logs
logs:
	docker compose logs -f airflow-webserver
```
Y el resto de las instrucciones son explicativas y claras..
```bash
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio9$ make build
docker build --no-cache -t etl-app:1.0.0 ./app
[+] Building 181.0s (15/15) FINISHED                                                                                                                        docker:default
 => [internal] load build definition from Dockerfile                                                                                                                  0.0s
 => => transferring dockerfile: 1.06kB                                                                                                                                0.0s
 => [internal] load metadata for docker.io/library/python:3.12-slim                                                                                                   1.7s
 => [internal] load .dockerignore                                
...
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio9$ make reset-init
./scripts/airflow_reset_init.sh
[+] Running 1/1
 ✔ Container laboratorio9-postgres-1  Started                                                                                                                         0.7s 
[+] Creating 1/1
 ✔ Container laboratorio9-postgres-1  Running   
 ...
```
Para make reset-init se realiza lo siguiente
```bash
Tú corres:
    make reset-init
         |
         v
Script intenta:
    airflow db reset
         |
         v
Airflow intenta crear:
    /opt/airflow/logs/...
         |
         v
ERROR: Permission denied
(no coincide el UID del contenedor con permisos del host)
         |
         v
Necesitamos saber el UID interno → probamos:
    docker run airflow-secure:1.0.0 id -u
         |
         v
ENTRYPOINT fuerza:
    airflow id -u    ← ERROR
         |
         v
Solución:
    docker run --entrypoint "" airflow-secure:1.0.0 id -u
         |
         v
Resultado:
    50000   ← UID real del contenedor
         |
         v
Ahora puedes corregir permisos:
    chown -R 50000:50000 ./airflow
         |
         v
Finalmente:
    make reset-init
✔ Funciona
```
y
```bash
               ┌────────────────────────────────────────┐
               │      TU MÁQUINA (HOST - Ubuntu)        │
               └────────────────────────────────────────┘
                             │
                             │  Montas esta carpeta al contenedor
                             ▼
                 ./airflow/ (dueño = esau:esau)
                 ├── dags/
                 ├── logs/              ← PROBLEMA
                 └── plugins/

   El contenedor Airflow necesita escribir en:
   /opt/airflow/logs/scheduler/...

   PERO el usuario interno del contenedor es:
                     UID = 50000
                     GID = 50000

   Y el host tenía:
                     dueño = esau (UID 1000)
                     permisos = 755

   Resultado:
   ┌────────────────────────────────────────────────────┐
   │  ERROR: PermissionError: [Errno 13] Permission denied│
   │  Airflow no puede crear carpetas en logs/           │
   └────────────────────────────────────────────────────┘


───────────────────────────
      🔧 SOLUCIÓN FINAL
───────────────────────────

PASO 1 — Cambiar dueño del directorio montado  
(para que coincida con el usuario del contenedor)

    sudo chown -R 50000:50000 airflow
           │      │      │       └── carpeta local que se monta
           │      │      └───────── grupo interno del contenedor
           │      └──────────────── usuario interno del contenedor
           └──────────────────────── recursivo (subcarpetas)

PASO 2 — Limpiar logs corruptos
    sudo rm -rf airflow/logs/*

PASO 3 — Reintentar inicialización
    make reset-init


───────────────────────────
        ✔️ RESULTADO
───────────────────────────

Ahora el contenedor:

   /opt/airflow/logs  ↔  ./airflow/logs  
   (50000:50000)          (50000:50000)

   → Puede crear carpetas  
   → Puede escribir logs  
   → Puede correr `airflow db init`  
   → No hay más PermissionError
...
[2025-12-11T00:36:29.092+0000] {override.py:1880} INFO - Added Permission can read on Permission Views to role Admin
[2025-12-11T00:36:29.117+0000] {override.py:1829} INFO - Created Permission View: menu access on Permission Pairs
[2025-12-11T00:36:29.124+0000] {override.py:1880} INFO - Added Permission menu access on Permission Pairs to role Admin
[2025-12-11T00:36:29.894+0000] {override.py:1516} INFO - Added user admin
User "admin" created with role "Admin"
```
make up
```bash
 ✔ airflow-secure:1.0.0                        Built                                                                                                                  0.0s 
 ✔ etl-app:1.0.0                               Built                                                                                                                  0.0s 
 ✔ Container laboratorio9-postgres-1           Healthy                                                                                                                0.9s 
 ✔ Container laboratorio9-airflow-scheduler-1  Started                                                                                                                1.2s 
 ✔ Container laboratorio9-etl-app-1            Started                                                                                                                1.2s 
 ✔ Container laboratorio9-airflow-webserver-1  Started                                                                                                                1.2s 
 ✔ Container laboratorio9-airflow-init-1       Started               
```
make logs
```bash
.PHONY: logs
logs:
	docker compose logs -f airflow-webserver(SERVICIO)

```
<p aling = center>
    <img src=airflow.png 
    width = 80%>
</p>

Como bien indica las instrucciones del laboratorio **csv_path = os.environ.get("ETL_INPUT", "data/input.csv")**
calcula la columna **df["value_squared"] = df["value"] ** 2**  e insertamos el resultado en una tabla **INSERT INTO processed_data (name, value, value_squared)
VALUES (%(name)s, %(value)s, %(value_squared)s)**

```bash
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio9$ docker compose run --rm etl-app python pipeline.py
[+] Creating 1/1
 ✔ Container laboratorio9-postgres-1  Running                                                                                                                         0.0s 
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio9$ 
```
Para el siguiente comando 
```bash
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio9$ docker compose exec -T postgres  psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT * FROM processed_data
 LIMIT 5;"
psql: error: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: FATAL:  role "root" does not exist
```
veamos lo que sucede
```bash
              Tu .env
    ┌─────────────────────────┐
    │ POSTGRES_USER=airflow   │
    │ POSTGRES_DB=lab9        │
    └─────────────┬───────────┘
                  │
     Docker Compose (sí lo lee)
                  │
         Contenedores OK ✔
                  │
────────────── LOCAL SHELL ────────────────
                  │
    (POSTGRES_USER no existe aquí)   ✘
                  │
docker compose exec postgres \
  psql -U "$POSTGRES_USER" ...
                  │
"$POSTGRES_USER" → "" (vacío)
                  │
psql usa usuario local → root
                  │
Postgres: "role root no existe" → ERROR
    set -a
    . .env
    set +a    ← modo auto export ,cada variable definada despues se exporta

```
Resultado deseado
```bash
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio9$ set -a
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio9$ . .env
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio9$ set +a
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio9$ docker compose exec -T postgres  psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT * FROM processed_data LIMIT 5;"
 name  | value | value_squared 
-------+-------+---------------
 alpha |     2 |             4
 beta  |     5 |            25
 gamma |    -3 |             9
 alpha |     2 |             4
 beta  |     5 |            25
(5 rows)
```
make test 
```bash
test:
	docker compose -f docker-compose.test.yml up --build --exit-code-from sut
	docker compose -f docker-compose.test.yml down -v
# en el docker compose se levantan construyen(las imagenes) dos servicios en sus repectivos contenedores, sut y postgres ,con los atributos usuales tanto para la definicion de las imagenes como para los contextos docker,
...
postgres-1  | 2025-12-11 02:17:58.401 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"                                                           
postgres-1  | 2025-12-11 02:17:58.413 UTC [27] LOG:  database system was shut down at 2025-12-11 02:17:56 UTC                                                              
postgres-1  | 2025-12-11 02:17:58.430 UTC [1] LOG:  database system is ready to accept connections
[+] Running 3/3
 ✔ Container laboratorio9-sut-1       Removed                                                                                                                         0.0s 
 ✔ Container laboratorio9-postgres-1  Removed                                                                                                                         0.0s 
 ! Network laboratorio9_backend       Resource is still in use     1

```
make sbom
```bash
#una nueva receta prerrequisito de sbom para instalar syft 
.PHONY: sbom
sbom: dep
	./scripts/sbom.sh $(APP_IMG)  ./dist/sbom-app.spdx.json
	./scripts/sbom.sh $(AIRFLOW_IMG) ./dist/sbom-airflow.spdx.json
	@echo "SBOMs en ./dist"
.PHONY: dep
dep: 
	@curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sudo sh
	./bin/syft version
#make sbom
#ejecuta el .sh 
SYFT_BIN="./bin/syft"

"$SYFT_BIN" "$IMG" -o spdx-json > "$OUT"
...
 ✔ Loaded image                                                                                                                                            etl-app:1.0.0   
 ✔ Parsed image                                                                                  sha256:e679f317d5a7e07d9f8366a017a9792accec157f754907ca68243bd271bd4636   
 ✔ Cataloged contents                                                                                   6257ef686c0f68dee0395d0b0634be08751902068fa1652184f832e8a81efe22   
   ├── ✔ Packages                        [113 packages]
   ├── ✔ Executables                     [838 executables]
   ├── ✔ File metadata                   [2,690 locations]
   └── ✔ File digests                    [2,690 files]
./scripts/sbom.sh airflow-secure:1.0.0 ./dist/sbom-airflow.spdx.json
[SBOM] Generando SBOM para airflow-secure:1.0.0 en ./dist/sbom-airflow.spdx.json
 ✔ Loaded image                                                                                                                                     airflow-secure:1.0.0   
 ⠙ Parsing image                   ━━━━━━━━━━━━━━━━━━━━                                          sha256:27c89e1cb1ceb9cccac5a66a0c0cff0acd502ae93ac858fe4b68c4932d56778b   
..
 ✔ Parsed image                                                                                  sha256:27c89e1cb1ceb9cccac5a66a0c0cff0acd502ae93ac858fe4b68c4932d56778b   
 ✔ Cataloged contents                                                                                   288565d245a60d678545605e9890de773d54e79241b1879f8ce0ba580425de4c   
   ├── ✔ Packages                        [603 packages]
   ├── ✔ Executables                     [1,367 executables]
   ├── ✔ File metadata                   [7,939 locations]
   └── ✔ File digests                    [7,939 files]
SBOMs en ./dist
```
make scan
```bash
#se agrega la receta dep-trivy

.PHONY: scan
scan: dep-trivy
	./scripts/scan_vulns.sh $(APP_IMG)
	./scripts/scan_vulns.sh $(AIRFLOW_IMG)

.PHONY: dep-trivy
dep-trivy:
	@mkdir -p ./bin
	@curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b ./bin
	@./bin/trivy version
	trivy --version
```
ejecutando el .sh scan_vulns
**./bin/trivy image --exit-code 1 --severity HIGH,CRITICAL "$IMG"**
```bash
 sudo chmod +x scripts/scan_vulns.sh
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio9$ make scan
aquasecurity/trivy info checking GitHub for latest tag
aquasecurity/trivy info found version: 0.68.1 for v0.68.1/Linux/64bit
...
```
Para lo anterior fue necesario 
```bash
[./bin existe y es de root]
           │
           ▼
ls -ld ./bin
           │
           ▼
make dep-trivy
  # Falla: install: Permission denied
           │
           ▼
sudo chown -R $(whoami):$(whoami) ./bin
           │
           ▼
make dep-trivy
  # Vuelve a intentar, puede tardar por conexión lenta
           │
           ▼
rm -rf ./bin && mkdir ./bin
           │
           ▼
make dep-trivy
  # Descarga e instala Trivy en ./bin 

```
Ahora la actividad propiamente
## Parte 1 - Operar, observar y documentar
### 1.1 Levantamiento y verificacion
imagenes → verifica estado 
Los artefactos se guardadn en evidencias/

### 1.2 Topologia y superficie expuesta
servicios → redes → resolucion de nombres en red Docker ..

Detecta la red , inspeccion de la red, tabla de puertos, prueba DNS 

### 1.3 Observabilidad minima
logs de webserver , del scheduler, morker  y comprobacion de salud

Se tuvo problemas al ejecutar la obtencion de los logs **docker compose logs --tail=200 airflow-scheduler | sed -E 's/(password|token|secret)=\S+/REDACTED/g' | tee -a Actividad18-CC3S2/evidencia/03_logs_airflow.txt** , por lo que se se resetringe pandas < 2.2 para que trabaje bien con airflow 2.9.1 , ademas se solventa el hecho de que **depends_on: postgres: condition: service_healthy** espera que inicie el servicio postgres pero no a que este listo , entonces definimos esa dependencia explicitamente en el make 
```bash
.PHONY: build
build:
	docker build --no-cache -t $(APP_IMG) ./app
	docker build --no-cache -t $(AIRFLOW_IMG) -f airflow/Dockerfile .

.PHONY: up
up: build
	docker compose up --build -d

```
Al hacer make up , se construyen y levantan los servicios.
Y la consulta resulta.
```bash
(.venv_labo9) esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio9$ make up
docker build --no-cache -t etl-app:1.0.0 ./app
[+] Building 124.9s (9/14)                                 docker:default
[+] Building 644.1s (15/15) FINISHED                       docker:default
 => [internal] load build definition from Dockerfile                 0.0s 
 => => transferring dockerfile: 1.06kB 
...
(.venv_labo9) esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio9$ docker compose logs --tail=200 airflow-scheduler | sed -E 's/(password|token|secret)=\S+/REDACTED/g' | tee ~/desarrolloDeSoftware/actividades/Actividad18-CC3S2/evidencias/03_logs_airflow_scheduler.txt
airflow-scheduler-1  | 
airflow-scheduler-1  |   ____________       _____________
airflow-scheduler-1  |  ____    |__( )_________  __/__  /________      __ 
airflow-scheduler-1  | ____  /| |_  /__  ___/_  /_ __  /_  __ \_ | /| / / 
airflow-scheduler-1  | ___  ___ |  / _  /   _  __/ _  / / /_/ /_ |/ |/ /  
airflow-scheduler-1  |  _/_/  |_/_/  /_/    /_/    /_/  \____/____/|__/   
airflow-scheduler-1  | [2025-12-11T15:01:36.498+0000] {task_context_logger.py:63} INFO - Task context logging is enabled
airflow-scheduler-1  | [2025-12-11T15:01:36.498+0000] {executor_loader.py:235} INFO - Loaded executor: SequentialExecutor
airflow-scheduler-1  | [2025-12-11T15:01:36.672+0000] {scheduler_job_runner.py:796} INFO - Starting the scheduler
airflow-scheduler-1  | [2025-12-11T15:01:36.673+0000] {scheduler_job_runner.py:803} INFO - Processing each file at most -1 times
airflow-scheduler-1  | [2025-12-11 15:01:36 +0000] [21] [INFO] Starting gunicorn 22.0.0

```
El pipeline* seguido, Cortesia de GPT 
```bash
# Construcción y setup del pipeline Airflow + ETL

Dockerfile airflow modificado:
  ├─ COPY dags /opt/airflow/dags
  ├─ COPY app /opt/airflow/app
  ├─ USER airflow (runtime seguro, no root)
  └─ pip install pandas<2.2 psycopg2-binary
      # Restricción pandas <2.2 evita incompatibilidades con Airflow 2.9.1

           │
           ▼
make build
  ├─ docker build -t etl-app:1.0.0 ./app
  ├─ docker build -t airflow-secure:1.0.0 -f airflow/Dockerfile .
  └─ Prepara imágenes listas para levantar stack
           │
           ▼
make up
  ├─ up: build → ya ejecuta make build antes
  ├─ docker compose up --build -d
  ├─ Levanta contenedores: postgres, etl-app, airflow-webserver, airflow-scheduler
  ├─ Dependencias:
      postgres -> etl-app / airflow-* via service_healthy
  ├─ Inicialización implícita:
      airflow-init:
        ├─ Inicializa DB
        └─ Crea usuario admin
  └─ ETL y Airflow Scheduler ya pueden acceder a Postgres por DNS interno
           │
           ▼
Pipeline/flujo en ejecución
  ├─ ETL lee datos de input.csv
  ├─ ETL procesa datos y los escribe en Postgres
  ├─ Airflow Scheduler detecta DAGs en /opt/airflow/dags
  ├─ Airflow Webserver expone UI en localhost:8080
  └─ Todos los logs se guardan en /opt/airflow/logs

# Notas de seguridad y diseño:
  - Solo airflow-webserver expone puerto 8080 al host
  - Postgres y etl-app solo se comunican internamente por la red 'backend'
  - build como prerequisito de up garantiza que los contenedores siempre tengan la versión correcta
  - Restricción pandas<2.2 asegura compatibilidad de librerías, evitando fallos en los DAGs/ETL

```

Este comando 
```bash
docker run --rm --network "$NET" byrnedo/alpine-curl \
  curl -s -o /dev/null -w "webserver /health: %{http_code}\n" http://airflow-webserver:8080/health \
  | tee -a Actividad18-CC3S2/evidencia/03_logs_airflow.txt
```
Ahorrajaba **webserver /health: 000 webserver /health: 000** , pues nuestro brige no es **echo "${NET}" observabilidad-mcp_default** sino  **8a96f1faa8f8   laboratorio9_backend         bridge    local**
