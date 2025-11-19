## Resumen de lectura 18
IaC cambia la forma como se diseña , revisan y operan la infraestructura. El codigo es la unica fuente de verdad, en base a este se discute la logica de la infraestructura. Pero cuando el proyecto crece los estados , entornos, modulos aumentan y surgen problemas de escalabilidad(por ejemplo).

Las causas que generarian conflictos son la estructura de los respositorios, estrategias de versionamiento , mecanismos de liberacion  y el marco cultural.

Escalar con el equipo , la definicion de la insfraestructura suele vivir en un unico repo junto a un backend remoto que almacena (S3 , terraform ,DynamoDB o Gitops con pull-based-deploys). Pero surge el problema cuando el proyecto crece,  los planes se vuelven lentos, los merge requests acumulan  etc, los cambios en modulos(entornos?) aislados provocan locks , el conocimiento se concentra en unas pocas personas, se necesita entonces estrechar la comunicacion entre dueños  y consumidores de esta infraestructura

Monorepositorio : toda la configuracion vive en un solo repo. Terraform define una sola fuente , un solo registro de commits refleja la evolucion , es facil de trazar.
Una debilidad es por ejemplo,que para corregir una simple linea de codigo debemos compilar(apply) TODO el proyecto de nuevo. Un monorepo escala mal cuando hay muchos merge request 
de forma continua

Multirepo: la logica se distribuye en multiples repos por dominio,de modo que un equipo de **data** mantiene sus propios modulos y uno de **plataform** revisa la provision. Cada repo tiene su propio pipeline.

De modo que se fortalece la seguridad, el tiempo de aplicacion plan/apply se acorta y las variables de entorno dejan de mezclarse. Pero se complica la busqueda de recursos .

Flujo para migrar de mono a multi repo :
```bash
Identificar y aislar el directorio (modules/network)→ extraer el historial(git filter-repo --banderas) → verificar la integridad e historial (git log, init,apply) → configurar el nuevo repo (terraform validate , plan, terraform {backend "s3" {}}) → publicar la primera version semantica (git tag v1.0.0 git push origin main --tags) 
```
Versionado y semantica:
Un esquema explicito  informa acerca de las versiones : 
EL SemVer por ejemplo, MAJOR.MINOR.PATCH 
MAjor aumenta si hay cambios incompatibles **1.0.0 → 2.0.0**
Minor aumenta si hay funcionalidades nuevas pero compatibles **1.2.0 → 1.5.0**
Patch aumenta cuando hay correciones menoress **1.5.2 → 1.5.9**
El terraform.lock.hcl ancla las versiones, el plan arrojara un diff edentico. Para modulos internos hace falta ademas usar un artifact repository ,asi no se dependemos de la fuente en si ,con un token accedemos a los artefactos ya creados

Liberaciones y notas de lanzamiento:
Liberar implica, compilar CHANGELOGS, firmar artefactos, describir pasos de upgrade en un lenguaje comprensible.El release notes incluira: contexto funcional(explicacion de los cambios) , impacto operativo(explica como modificcar lo necesario para que lo nuevo funcione), compatilidad(versiones minimas que para correr), acciones manuales(pasos extras)

Comparticion segura y gobernanza colaborativa de modulos: un modulo de base de datos requiere "secure by design" para que no se desactive el modo de cifrado(?) para ello: 
- Se expone solo las variables absolutamente necesarias
- Se documenta con ejemplos practicos
- Se establecen  pull request publicos donde cualquier equipo proponga cambios
- Se etiqueta cambios disruptivos.

En paralelo , se integran OPA/ Conftest , terraform-compliance, tfsec .

De modo que obtenemos que la seguridad y resiliencia sean parte de la evolucion del proyecto, gracias a una buena estructura de repositorios, versionado comprensible, liberaciones auditables y un ecosistema de modulos compartidos

Metricas e indicadores KPI's , para evaluar la efectividad del gobierno y la escalabilidad , se mide:
```bash
tiempo medio de plan --duracion del init----<60s 
frecuencia de locks concurrentes---numero de bloqueos ---- <5% de ejecuciones
tasa de rechazo por politicas---%de pipelines detenidos por OPA.---<2% evitar falsos positivos
Tiempo de revision MR---duracion media PR→merge----<4horas
versiones estables de modulos----%de consumos apuntando a tag ---->95%

```
Se registra esto en un dashboard tipo grafana,permite detectar cuellos de botella.

Cuando los pipelines comienzan a ralentizarse, de debe a una combinacion de : procesar todo el monorepo para cambio; bloqueos simultaneo de estado terraform y sobrecarga de notificaciones.
- Particionar el repo
- Implementar caches inteligentes
- Paralelizar
- Optimizar la duracion de los locks
- Autoescling 

Agrupar estas inciativass en un unico bloque
## Resumen de lectura 19
La seguridad de IaC dentro de DevSecOps es un flujo continuo donde la cadena de suministros , la proteccion de secretos , el control de permisos , el crifrado, la integridad del backend y la gestion de desviaciones como partes de un sistema.

La base de la seguridad empieza protegiendo la cadena de sumistros del software(creacion,distribucion y uso de la infraestructura) , esto se consigue firmando cualquier modulo, proveedor o artefacto.

Con este objetivo, generamos elementos como el SBOM (lista de componentes del software) , ademas los attestations y metadatos al estilo SLSA , estos permiten rastrear el origen de los artefactos.

Todo requiere estar firmado y tener controles como checksum de proveedores o lockfiles que congelan versiones no confiables.
La idea es que el pipeline produzca artefactos verificables

En tanto que la gestion de secretos, se intenta que el codigo no exponga secretos, entonces el almacenamiento se da en AWS Secrets Manager (por ejemplo). Se prohibe claves estaticas, en su lugar se utilizan tokens temporales generados via IODC hacie cloud. El codigo usa escanares para detectar secretos antes de cualquier commit. Se evita tambien que los outputs de terraform tengan valores sensibles.

La definicion de permisos minimo es otro pilar importante. Los modulos de terraform deben exponer lo minimo posible, y tambien analizan si hay permisos excesivos.El cifrado es neceario para datos de transito , gestiona clave en infraestructuras confiables como KMS(guarda llaves) . La auditoria se logra via logs centralizados segun NIST(norma estandares)

configuramos terraform se configura como un control de integridad. El estado debe estar cifrado , versionado , bloqueado y tener politicas de impiden borrado accidental. Solo algunos roles pueden aplicar cambios.Toda accion queda registrada y el historial es una evidencia operativa. Las brechas de seguridad son fallas por ausencia de controles en cadena de suministros, como por ejemplo manejo incorrecto de IAM. 

La observabilidad total del pipeline se consigue mediante registros de plan y apply, traza de auditoria  y metricas operativas, que miden la calidad del proceso. La deteccion de drift se convierte en un mecanismo diario : los modulos se comparan con sus estados anteriores, se evalua segun su impacto y se decide si hay remediacion. La resiliencia por estrategias de respaldo, restauracion y diseños multi-zona, que garantizen continuidad, con pruebas continuas que validen estos mecanismos.

Finalmente , la postura en tiempo de ejecucion se gestiona via CSPM  o CNAPP que vigilan configuraciones y exposiciones. Se crea un ciclo cerrado donde la infraestructura aplicada e infraestructura observada siempre coinciden, caso contrario se corrige. En este ecosistema se automatiza recursos, tambien es gobernable, auditable y resiliente. Tambien obtnemos trazabilidad, integramos controles de seguridad y operaciones disciplinadas.

# Actividad16-CC3S2

## Parte A. Preguntas teorico-conceptuales 
A1. Monorepositorio vs multi-repositorio
1. Comenzar con un monorepositorio acelera el poder construir y levantar la insfraetructura inicial y los modulos básicos, porque (por ejemplo) es muy fácil encontrar un recurso especáfico buscado, pues tenemos una sola fuente; trazar los cambios es muy fácil, se puede ver  TODOS los cambios correspondientes al proyecto mediante **git log**, el cual  muestra el historial completo con todo lo que ello implica, se sabra exactamente quien , cuándo y por qué realizó el cambio.

2. De la experiencia , en un proyecto con colaboradores , si se depende de un solo repositorio las solicitudes de merge se ralentizan, tenemos que esperar que el colaborador envie su pull-requests para poder implementar nuestros issues, pese a que ya se modulariza* mediante las columnas del kanban.
Esto es evidente en el control de concurrencia(locks),ya que luego de un plan - apply se bloquea el estado remoto para asegurar que solo una persona este modificando estado en un momento dado. Esto obviamente obliga a los demas colaboradores a esperar para usar un recurso especifico.
En correlacion con lo anterior, quienes estan asignados para la resvision de los pull-requests sufriran sobrecarga de trabajo, podiendo revisar cambios en areas totalmente separadas pero que son necesarios revisar.
En cuanto a la Ci lenta, sabemos que en un repositorio todo el codigo forma el cojunto del proyecto , de modo que las configuraciones que necesita un modulo en concreto, se aplican  a todo el repositorio.
Permisos demasiado amplios, git otorga permisos a todo el repo, que se de permisos sobre un modulo particular es un tanto complicado.Esto aumenta, desde luego , el radio de impacto de una error, pues un solo commit afectaria a toda la infra.
3. Cuando el proyecto crece es preciso extraer modulos y trabajar con un enfoque multi-repo. 
Tal como se explica en la lectura 18: 
- (1) se identifica el directorio, en este caso **modules/network** ,
- (2) se extrae el historial (**git filter-repo**) con esto creamos un repo con los commits correspondientes a esa carpeta , 
- (3) se verifica la integridad del historial mediante **git log**, **terraform init , plan** apuntando al estado existente(?),
- (4) configuramos el nuevo repositorio ( creamos el pipeline especifico **lint ,terraform init, terraform plan**) ,  
- (5) se publica la primera versión semántica (**git tag v1.0.0 ,git psuh origin main --tags**)
- (6) se actualiza consumos en el repositorio original(cambiamos los **source** de los modulos , se ubican los URL de los nuevos repos , eliminamos la carpeta en un commit posterior, una vez que los clientes hayan migrado)

A2.Versionado semántico y notas de versión 

El versionado semántico detalla mediante numeros si las nuevas funciones (cambios son incompatibles, compatibles, se realizaron cambios menores)
VMAJOR.MINOR.PATCH. Si MAJOR crece **v1.0.0 → v3.0.0** significa que hay cambios incompatibles entre versiones

MINOR crece si hay funcionalidades nuevas pero compatibles.

PATCH crece cuando hay correciones menores que desde luego no rompen la logica entre versiones.

No es aceptable que un equipo apunte a la rama main de un modulo sin una etiqueta de version firmada, pues main es no representa el producto final, main es volatil, en main podria eliminarse una funcion que se esta usando en por un equipo en particular.Por otro lado una ausencia de contrato, podria provocar que luego de un terraform plan se rompa la compatibilidad sin que se haya versionado.

Acerca de la nota de version debe ser una guia de upgrade que el equipo consumidor podra adoptar,el cual deberá incluir 
- Contexto y justificacion funcional:   se detalla el por que se introdujo el cambio. Ejemplo **se introduce este modulo para cumplir con el nuevo estandar de cifrado (AES -256) requerido por el area de seguridad** 
- Impacto operativo y variables : Detalla con precision como la actualizacion afecta al codigo de consumo, variables : variables nuevas , variables eliminadas, valores por defecto modificados ejemplo (el tipo e instancia cambia de **t3.medium a t4g.medium**) 
Migraciones de estado:si el cambio requiere que se modifique un recurso existente ejemplo (**el nombre logico del recurso de base de datos ha cambiado, se requerira un state move manual antes de apply para evitar recreacion**)     

A3. Seguridad en cadena de suministros
- SBOM + verificacion de proveedores: 
La lista de componentes de software 
y el SLSA permite revisar metadatos,




