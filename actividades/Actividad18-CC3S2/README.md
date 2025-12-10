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

```