Toda la informacion de los servicios que se despliegan , estos dentro sus correspondientes contenedores se encuentran en el **docker-compose.yml**  , son 5 servicios dentro del bloque del atributo **services**. Se tiene una red define por (en?) el atributo **networks** : backend. Todos los servicios se comunican dentro de esta red. La comunicacion se hace con el nombre del servicio como DNS 
```bash
etl-app:
    environment:
        POSTGRES_HOST: postgres
    networks:
        - backend
```
Ni base de datos postgres ni etl-app exponen puertos, lo cual agrega seguridad , no pueden ser accedidos desde afuera.
Ademas la guia sugiere añadir un atributo driver quien aislará la red interna de la externa(en nuestro HOST) 