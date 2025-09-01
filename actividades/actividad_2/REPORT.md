### Actividad2_CC3S2 
**FLORES VILLAR ESAU**
## 1 HTTP : Fundamentos y herramientas
 1. **Levantando la app** 
 - La app en cuestion se describe del siguiente modo. En las primeras lineas importamos las librerias de interes, entre ellos flask y os
en las siguientes se definen las variables de entorno como PUERTO y LANZAMIENTO
luego creamos una instancia de flask ``app=Flask(MODULO de recursos)``para procesar los request http.Seguidamente se usa un decorador 
``@app.route("/")`` para agregar comportamiento a ```def root()``` de modo que cada vez que  alguien haga un request hacia *http://localhost:PUERTO* o *("/")* se ejecutara root()
Cabe resaltar que se creó el entorno virtual ,`actividad-2` que es donde se corre la version de flask descargada.
- ![Levantando la app con variables de entorno 12-App](imagenes/1.png)

-  salida stdout ` mensaje=Hola CC3S2,lanzamiento=v1`

`python -m venv actividad_2`
` source actividad_2/bin/activate`
`sudo o apt install python3-flask`
`python3 app.py`

2. **Inpección con curl**
-  cabeceras `Host , user-Agent, Accept` cuerpos de estado:` 127.0.0.1:8080 ,curl/8.5.0 , */*`
    cuerpo json  
    ``HTTP/1.1 200 OK
    Server: Werkzeug/3.0.1 Python/3.12.3
    Date: Mon, 01 Sep 2025 16:52:38 GMT
    Content-Type: application/json
    Content-Length: 72
    Connection: close``

- ![Inpeccion Curl](imagenes/2.png)