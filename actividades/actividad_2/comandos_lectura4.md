## http contrato operativo del servicio
transicion: 
|-----CALMS y CI/CD---------------|
|---------------------------------|
|http → observabilidad y seguridad|
|---------------------------------|

http estructura la comunicacion entre cliente y servidor.
GET , PUT y DELETE son idempotentes.
POST no lo es, mientras PATCH depende lo sera a veces
ej : un endpoint /orders con POST debe asegurarse de reintentos automaticos que dupliquen pedidos
codigos de estado :
- 2xx exito 201 creado , 2022 aceptado<br>
- 3xx gestiona redirecciones<br>
- 4xx responsabiliza al cliente<br>
- 5xx señala fallas del servidor que activan alarmas<br>

cabeceras refuerzan el contrato:
- Cache-Controle
- Etag If-Match
- Strict-Transport-Security 
- X-Request-ID

la observabilidad mide latencias p50 p95 p99 
los endpoint de salud distinguen *liveness* de *readiness* evitando que balanceadores enruten a instacias no preparadas

un endpoint /health que retorna 200 para liveness y 503 para readiness
## inspeccion rapida del contrato (cabeceras y coodigos)
- con ``curl -I -k https://host:443`` enviamos en GET para recibir las cabeceras clave
sed -p permite imprimir lo deaseado especificando las lineas 1,20 

![cabeceras clave](imagenes/lectura4_1_1.png)
![](imagenes/lectura4_1_1b.png)
# validacion condicional con Etag 
ahora para ejecutar toda la segunda instruccion se requiere un endpoint que nos devuelva un recurso , en este caso se crea la clase recurso con dos atributos de clase(int) y en endpoint lo que hara se devolver esos valores

``class Recurso:
    def __init__(self,a,b):
        self.x = a;self.y = b
    def get_variables(self):
        return {"x":self.x,"y":self.y}``
 
 y el endpoint

 ``@app.route("/recurso")
    def recurso():
        r = Recurso(1,2)
        return jsonify(r.get_variables())
``
una peticion GET simple mediante curl devuelve: < HTTP/1.1 200 OK
< Server: nginx/1.24.0 (Ubuntu)
< Date: Sun, 07 Sep 2025 15:24:45 GMT
< Content-Type: application/json
< Content-Length: 14
< Connection: keep-alive
< 
{"x":1,"y":2}
* Connection #0 to host miapp2.local

Ahora lo que piden es ``curl -sI https://miapp2.local/recurso | awk -F': ' 'tolower($1)' ``

para ello definimos el eTag para nuestro recurso, como ni flask ni nginx tiene esa cabecera en sus respuestas, se necesita definirlo en nuestro app2.py 
dentro del endpoint @app.route(/recurso) def recurso():
    hasheamos el retorno de la funcion 
    obtenemos el hash (etag) anterior desde cliente
    los comparamos y enviamos la repsuesta
            si no cambio

            respuesta = make_response("",304)
            respuesta.headers["Etag"] = hash_recurso

            o si hubo modificacion

            respuesta = make_respuesta(cuerpo,"200")
            respuesta.headers["Content-type"] = "application/json"
            respuesta.headers["Etag"] = etag_recurso
y a consulta hecha devuelve el Etag de lo que devuelve el endpoint
![ETAG](imagenes/lectura4_1_2.png)

el  cliente curl pide solo las cabeceras| analiza la columna imprimiendo el segundo campo | evitando el salto de linea

y con el valor de ETAG obtenido se hace
el segundo comando , solicitando el recurso si el hash no coincide con el que se tiene

![etag ](imagenes/lectura4_1_2b.png)

# Forzar validacion de cache en cliente
ahora obviaremos la cache y consultaremos desde la fuente
curl -k -I -H "PETICION" htpps://..

![no cache](imagenes/lectura4_1_3.png)

# comprobar HSTS 
para forzar que la comunicacion sea solo por https agregamos la cabecera Strict-Transport-Security hsts  en el .conf que usara nginx, reiniciando este y finalmente se hace la consulta via cliente curl

![hsts](imagenes/lectura4_1_4.png)
# trazabilidad 
aunque request.headers.get() puede usarse en cualquier endpoint , esto es en cualquier cuerpo de os metodos definidos luego de app.route("/ip/ping")
lo ideal es determinar un punto de salud sin logica de negocio para verificar disponibilidad entonces se define en ping():
    devolver jsonify con cabeceras 

![trazabilidad](imagenes/lectura4_1_5.png)

## indempotencia y reintentos
ejecutaremos la misma operacion con el mismo resultado, ejemplo, si enviamos un get (ver) el resultado sera el mismo

para ``curl --retry 3 --retry-all-errors --fail https://HOST:PORT/items/123
``
![get/put/delete](imagenes/lectura4_2_0.png)
agregamos un endpoint con soporte para Indempotency-Key 
y se probara con la solicitud tipo POST que suele modificar entre llamadas

``  
    @app.route(ruta para el endpoint) 
    obtener el llava_idempotencia de la llamada (request)
    obtener el cuerpo de la llamada
    si no existe return 
    si llave_idempotencia esta en cache
        retorna respuesta para esa llave de cache
    crear una nueva orden con los campos id, sku,qty,status         
``
![mismas](imagenes/lectura4_2_1.png)

## observabilidad

ahora acerca de la observabilidad ,
las opciones 'nombre=%{nombre}s' tienen un sentido intuitivo. 
se va a medir latencias en cada fase de peticion https
*%{time_namelookup}* dns lookup tiempo desde que se inicio la peticion hasta la resolucion del nombre A/AAAA

*%{time_connect}* tcp connect tiempo desde el incio hasta que se completa la conexion tcp

*%{time_appconnect}* TSl handshake tiempo que tomo hacer el handshake tls (ssl/tls) 

*{time_pretranser}* tiempo para que libcurl de por hecho la negociacion preliminar(auth,proxy,tls) y listo para Enviar/ recibir 

*{tiime_starttransfer}* TTFB tiempo HASTA que llega el primer byte de respuesta del servidor
TTFB = DNS + TCP + TLS + tiempo_servidor_procesa

*{time_total}* total 

![](imagenes/lectura4_3_1.png)

### Liveness vs Readness (sin kubernetes)
*patron de monitoreo recomendado*
- /healthz 200 proceso vivo no revisa dependencias
- /readyz 200 solo cuando dependencias esten ok (db,cola) 503 mientras inicia

``curl -k -fsS https://miapp2.local:443/saludz >/dev/null && echo "VIVO" || echo "NO VIVO"
con esto se verifica que el proceso que da vida al servidor de la aplicacion (la misma applicacion) este corriendo, que sigue vivo en memoria y respondiendo 

y en una sola linea ``until curl -k -fsS http://miapp2.local:443/listoz >/dev/null; do echo "No ready aún..."; sleep 1; done; echo "READY"``
![healthz y readyz](imagenes/lectura4_4_1.png)

ver en tiempo real 

``watch -n1 'comando' ``
y la estadistica de sockets
``ss -tlnp``

## Liveness / Readiness en CI/CD  y systemd

## control de tasa (429)  y comportamiento de bajo carga

# ejemplos de actualizacion condicionesl Etag / If-match

## DNS identidad y disponibilidad en la red
# transicion : 
DNS pilar de la identidad del servicio, se alinea con la automatizacion  y medicion de CALMS para garantizar disponibilidad y consistencia

DNS resuelve nombres a direccion , la disponibilidad percibida , los registros principales son A/AAAA  etc 
el TTL controla la cache , un ttl de 300s permite cambios rapidos en canario , mientras quue uno de 86400 reduce consulta en servicios estables.

*segun lectura *

consulta dns stub--resolver(cliente)
                ↓ 
resolver recursivo (ISP)(que cachea respuestas y sigue la cadena raiz)  (1) en cache ? SI res
                ↓
TLD(.com.org clasifica) 
                ↓
         autoritativos

*segun chat gpt*
[Cliente]
   |
   v
[Stub resolver]
   |
   v
[Resolver recursivo del ISP(cachea respuestas y sigue la cadena raiz)]
   |  (1) ¿En caché?
   |       ├─ Sí → responde
   |       └─ No → sigue la cadena
   v
[Root servers]()
   |
   v
[TLD servers (.com, .org, .pe, ... clasifica) ]
pregunta a los Ns(name servers) de example.com
   |
   v
[Servidores autoritativos del dominio]
   |
   v
[Respuesta: IP o NXDOMAIN (usa cache negativa que amortigua consultas de nombres no existentes)]
   |
   v
[Resolver recursivo cachea respuesta]
   |
   v
[Stub resolver → Cliente]

la cache negativa para NXDOMAIN amortigua consultas a nombres inexistentes

en entornos corporativos , split-horizon DNS (respuestas distintas segun origen) entregan ip´s privadas a clientes internos y publicas a externos
ej : ``internal.example.com`` resuelve 10.0.0.1 internamente  y a una IP publica via CDN(red de  servidores distribuidores  que almacenan en cache contenido web)

        En devsecops 
            ↓
DNSSEC              CAA  

DNSSEC (DNS security extensions) valida integridad con firmas criptograficas
CAA  = (certificate Authority Authorization) restringe emisores de certificados
Verificaciones evitando discrepancias y revisa /etc/hosts
*ver servidores raiz . *
es la raiz de la jerarquia de nombres de dominio en internet, 13 nombres de servidores de raiz, aunque teoricamente solo hay una
# espacio de nommbres de y TLD (raiz→TLD→ dominio)
* viendo servidores raiz
``dig . NS +nocomments +noquestion +answer``
* viendo TLD´s server
``dig com. NS +nocomments +noquestion +answer``
``dig pe. NS +nocomments +noquestion +answer``
* viendo los servidores responsables de example.com
``dig example.com NS +nocomments +noquestion +answer``
![servidores responsables del dominio example.com](imagenes/dns_responsables.png)
* consulta directa a su NS 
``dig +nsearch example.com``
# flujo de resolucion DNS (trazado a paso )                                               
* camino completo raiz → TLD → autoritativo (sin cache del recursor)
tal como indica , no pasa por cache , va directo de la raiz al servidor autoritativo
``dig a_que_servidor los_NS_de_los_TLD desactiva_Recursion`` → ``dig @1.root-servers.net com. NS +norecurse``
![autoritativos de example](imagenes/autoritativos_example.png)

para hacerlo paso a paso
- a raiz``dig @a.root-servers.net com. NS +norecurse``
- a tld``dig @a.gtld-servers.net example.com NS +norecurse``
- `a autoritativo``dig @<ns_autoritativo_de_eample> www.example.com A +norecurse``

# resolver local y orden de resolucion (libc/ NSS)
*Stub resolver*, inicia la consulta DNS, envia la consulta al resolver recursivo 
resolver recursivo (configurado en /etc/resolv.conf)
↓ 
el *resolver recursivo* hace el trabajo pesado 
consulta a la raiz→TLD→autoritativo y devuelve la respusta al stub, puede ser remoto ISP, google 8.8.8.8 o uno local(systemd-resolver 127.0.0.53)

*glibc resolver + NSS (name service switch )*
"las funciones de libc getadd gethost no preguntan directamente dns, consultan al sistema de nombres configurado por NSS" ..chat gpt 
*que en plabaras simples seria que use el dominio disponible*
* nss esta en /etc/nsswitch.conf que define que fuentes de datos se usan para resolver diferentes cosas *

- devuelve ip de acuerdo a lo que diga nss
``getent hosts www.google.com``
``esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware$ getent hosts www.google.com
2800:3f0:4003:c0f::67 www.google.com
2800:3f0:4003:c0f::6a www.google.com
2800:3f0:4003:c0f::69 www.google.com
2800:3f0:4003:c0f::63 www.google.com``
- ipv4 e ipv6
``getent ahosts www.example.com``

y para ver como decide el sistema(nuestra pc) a que resolver recursivo va a preguntar

 ls -l /etc/resolv.conf
``lrwxrwxrwx 1 root root 20 Sep 10 19:06 /etc/resolv.conf -> /mnt/wsl/resolv.conf``
el etc/resolv.conf es un enlace simbolico

para cat /etc/resolv.conf 

``This file was automatically generated by WSL. To stop automatic generation of this file, add the following entry to /etc/wsl.conf:
# [network]
# generateResolvConf = false
nameserver 10.255.255.254``

resumiendo y uniendo los terminos:
el stub resolver (ping ,getent,.) lee /etc/resolv.conf que tiene la direccion del resolver recursivo(google 8.8.8.8 ) este "servidor dns"  hara la consulta a root → tld → autoritativos
``resolvectl status`` estado general de la resolucion
``resolvectl dns`` muestra los resolver recursivos
``resolvectl domain`` ......
``resolvectl query www.example.com `` consulta dns concreta , seria como dig

grep '^hosts:' /etc/nsswitch.conf
``hosts:          files dns``
esto significa que primero nuestro stub resolver al consultar /etc/nsswitch.conf buscara primero en /etc/hosts (local) y si no encuentra pasara a dns.



# Registros A/AAAA/CNAME/TXT/MX/SRV (+ CAA/ DNSSEC)
dig +short A www.example.com     A resgitro que mapea dominio a direccion ipv4        