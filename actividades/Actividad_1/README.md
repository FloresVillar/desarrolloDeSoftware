# Actividad 1-CC3S2                                     
**Nombre:** Flores Villar Esau
**Fecha:** 31/08/2025
**Tiempo:** Dias
**Entorno usado :** Wsl, ejecutamos de forma nativa un entorno linux en windows

## 4.1 Comparacion Cascado vs Devops
- ![Cascada vs Devops](imagenes/devops-vs-cascada.png)
* imagen 1. Constraste en entre en enfoque cascada y Devops. Fuente en [FUENTES.md](FUENTES.md).*

- Como se menciona en la Lectura 1 ,en el desarrollo tradicional se espera que la etapa anterior termine , esto provoca que los errores se acumulen y sea dificil detectar en que parte se genero tal o cual error.Ahora bien, esto es un lastre si pretendemos usar computacion en la nube, pues  una de las caracteristicas de esta ultima,es que permite gestionar el ciclo de vida de las aplicaciones; entonces se debera optar por devops, quee tiene como una de sus bondades la  retroalimentacion continua lo que permitira  por ejemplo la creacion de dashboard para la medicion de metricas de interes.

- En un entorno de programacion de hardware medica-por ejemplo un marcapasos- se exige una trazabilidad documentaria, osea que cada etapa debe quedar delimitada claramente,caracteristica que encaja maravillosamente con el enfoque cascada,con lo cual queda abarcado el primer criterio "la documentacion exhaustiva" que ayudara a demostrar el cumplimiento de las normas ante cualquier entidad reguladora.Respecto al seugundo criterio es precisamente la validad de la seguridad, cada etapa debe "testear" por separado , generando que ese estadío abarque y satifaga todas los requerimientos.
Con todo esto el trade-offs es indiscutiblemente el hecho de sacrificar "agilidad" y ganar en cambio, conformidad y seguridad, lo cual es imprescindible en un escenario donde un fallo equilvadria a poner en riesgo la vida del paciente.


## 4.2 Ciclo tradicional de dos pasos y silos
- ![Ciclo tradiccional construccion-lanzamiento](imagenes/silos-equipos.png)
* imagen 2. Ciclo tradicional (limitaciones y anti-patrones). Fuente en [FUENTES.md](FUENTES.md). *

- A saber,CI añade cambios pequeños probados, si esto no se considera como parte del ciclo de desarrollo resultara en una "falta de visibilizacion temprana de errores" lo que naturalmente propicia una gran entrega en produccion.
La "compatibilidad entre entornos" si no se realiza la integracion continua la aplicacion puede correr bien en desarrollo, pero; por temas de configuracion de librerias-por ejemplo- falle en produccion.

- "Throw over the wall": es la principal caracteristica del modo tradicional, los equipos estan serparados , terminan su trabajo(bien, en el sentido de validar sus metas) pero luego simplemente lo lanzan(handoff) al siguiente equipo,en este sentido Devops es -como se menciona en las lecturas- es tambien un cambio de la cultura organizativa.

"Seguridad como auditoria tardia": como se viene mencionando, este antipatron origina que luego de un gran lanzamiento  no pueda identificar facilmente(MTTR) donde realmente estan los errores.

## 4.3 Principios y beneficios de Devops(CI/CD, automatizacion, colaboracion,Agile como precursor)

- **CI:** Integramos pequeños cambios continuos y correctos  al repo principal,estas pruebas se automatizan y pueden ser -por ejemplo- unitarias.
**CD:** Entregamos cambios a produccion de modo que cada version sea reproducible,finiquitando con el clasico "en mi maquina corre".La automatizacion ademas nos ayudara a acortar los ciclos de entrega y a responder rapidamente ante errores.
- **Practica Agil:**
Las practicas agiles tienen entre sus maximas la colaboracion con el cliente, de modo que mecanismos como  stand-up meetings permitiran una mejora continua del software en este aspecto.

- **Indicador que mide la mejora de la colaboracion Devops**
Numero de despliegues exitosos por dia, utilizando curl, redirigiendo la salida a un archivo luego de hacer un request al endpoint en nuestro localhost , estas tendrian posibles valores : 200,500,404 se contaria las veces que se obtiene 200.

## 4.4 Evolucion a Devsecops(SAST/ DAST)
- **SAST** esta tecnica analiza codigo fuente sin ejecutarla, de modo que podamos detectar vulnerabilidades en la logica de programacion como sql inyection. En tanto que **DAST** se aplica en ejecucion,mas precisamente en un entorno de preproduccion(staging) , donde simulamos el entorno real de produccion.

![Cascada vs Devops](imagenes/SAST_DAST.png)
* imagen 4. SAST y DAST. Fuente en [FUENTES.md](FUENTES.md).*

- **Gate:Dependencias externas sin vulnerabilidades CVE** Todas las librerias externas no deben presentar vulnerabilidades registrados en CVE
un ejemplo concreto es que librerias como numpy pasen esta condicion de seguridad.Los Acerca de los umbrales: 
Umbral estricto (0 vulnerabilidades)
umbral permisivo( <=2 vulnerabilidades ) 
Dependiendo de estos se permitira que promocione o no  hacia la siguiente del ciclo del software.Sin embargo, en caso de no poder resolver este gate(por falta de una actualizacion), ha de aplicarse la siguiente politica de "captura de excepcion" la cual considera para la *caducidad* un maximo de 30 dias,*responsable* el lider tecnico del proyecto , *plan de correcion* esta incluiría colocar la actualizacion de la dependencia mientras tanto se puede usar un reemplazo.
## 4.5 CI/CD y estrategias de despliegue(sandbox, canary azul/verde)

![Cascada vs Devops](imagenes/pipeline_canary.png)
* imagen 5. Ciclo tradicional Estrategias de despligue. Fuente en [FUENTES.md](FUENTES.md).*

## 4.6 Fundamentos practicos sin comandos 

### 1.HTTP - contrato observable
![Cascada vs Devops](imagenes/http-evidencia.png)
* imagen 6.1. HTTP . Fuente en [FUENTES.md](FUENTES.md).*

### 2.DNS - nombres y TTL
![Cascada vs Devops](imagenes/dns-ttl.png)
* imagen 6.2. DNS . Fuente en [FUENTES.md](FUENTES.md).*

### 3.TLS - seguridad en transito
![Cascada vs Devops](imagenes/tls-cert.png)
* imagen 6.3. TLS . Fuente en [FUENTES.md](FUENTES.md).*

### 3.Puertos- estado de runtime
![Cascada vs Devops](imagenes/puertos.png)
* imagen 6.3. TLS . Fuente en [FUENTES.md](FUENTES.md).*

### 5 12-Factor -port binding , configuración, logs

### 6 Checklist de diagnostico (incidencia simulado)

## 4.7 Desafios de Devops y mitigaciones
![Desafios Devops](imagenes/desafios_devops.png)
* imagen 7. Desafios Devops . Fuente en [FUENTES.md](FUENTES.md).*

## 4.8 Arquitectura minima para DevsecOps (HTTP/ DNS/ TLS + 12-factor)
![Desafios Devops](imagenes/arquitectura_minima.png)
* imagen 8. DevsecOps . Fuente en [FUENTES.md](FUENTES.md).*



