# ReSUMEN DE CLASE 06 octubre
Los apuntes se hicieron "en caliente" por lo que podrian haber inconsistencias entre en algunas siglas
- SOLID:
- DRY:
- IaC:
- Shift lefft security : movemos la seguridad al inicio del ciclo del desarrollo<br>
De ese modo se evita auditoria tardia, detectar errores tempranamente.

- Infraestructura inmutable : los reportes no se modifican una vez creados, se reemplazan por nuevas versiones, para evitar drift , eso mejora reproducibilidad. Esta infraestructura inmutable se junta con IaC 
- Zero Trust infraestruc: nada es confiable por defecto, se verifica todo, se minimiza superficie de ataque
- Ingenieria de caos:en sistemas distribuidos
- Politicas como codigo: las politicas de seguridad y operacion se definen como codigo
- monitoreo continuo y feedback : 
Pytest valida la implementacion, que sea consistente<br>

que hace mocks/stubs → DI  /DIP → SOLID → gates devsecops<br>
IaC local, no es proveedor con nube<br>
 
## un stubs 
Regresa una respuesta fija y predecible, sirve para aislar una unidad de codigo de factores externos, ej 
- LATENCIA DE RED
- Dependencias no disponibles
- fluctuaciones de API  
No comprueba que se llamó correctamente,solo entrega datos controlados.
Stub provienen de ...<br>
Evitan estos problemas, data leadge, ej registro de token por error, o golpes a API con cierto coste<br>
Eso es basicamente un stub

## Que es un mock
Verifica interacciones, cuantas veces se llamo, mock si sirve para seguridad, pues se puede forzar contratos "toda peticion debe usar https" , "no debe incluir autorizacion en logs", ...<br>

stub comportamiento determinista<br>
mock comportamiento de seguridad<br>

## DI y DIP 
-DIP lo que se hace es que "los modulos de alto nivel dependan de abstracciones"<br>
Permite testear fallos , este dip permite testear fallos, hablamos de codigo 5xx, politicas de reintento<br>
politica de reintento  :{ackoff, Itter}<br>
DI en service.py 
## Modalidades de DI 
- Inyeccion de constructor ,recomendado para negocios SVC  =MovieService(http = SecureRequest()) va a prodccion <br>
DIP modulos de alto nivel (sevice) deben depender de abstracciones interfaces/puertos  service → depende de→ abstraccion  : httpPort → adapter real

El punto de arranque en donde tu implementas para ...(NO APUNTADO)

El patron permite que en local se use hhtp con fixtures determinista
en real 
SOLID , revisar

SRP , 

- OCP , nucleo se agregan como decoradores y adapter, reduce cambios , <br>
- LSP   Fake  debe comportarse en terminos de contrato observable<br>
Si el real lanza valueError ante dominio no permitido, el Fake tambien lo hace<br>
- ISP segregacion de interfaces , uno minimo reduce metodos peligrosos, si se tiene httpPort con un getj_son es mas facil de auditar, SCAPE HATCH<br>
- DIP hablamos flujo de dependencias con abstracciones, se cablean en composition en main<br>
- GATES reglas automatizadas y reproducibles, bloquean etapas del ciclo si no se cumplen con estandares<br>


