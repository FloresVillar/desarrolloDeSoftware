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