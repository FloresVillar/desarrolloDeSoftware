### lunes 8 setiembre
se tiene que dominar shell linux xd
entender procesos y controlar el terminal, 
- tail -f inspecciion incremental
- find 
- top 
- umask
rwx permisos  , chmod 
entradas pipes


git init
git clone
git commit  *unidad de comunicacion* se prepara cambios con github y se confrima con git -m "..."
git switch -c *aisla*
git merge *integra resultados*
entonces, un buen mensaje de commit resume un buen contexto, es una referencia a issues, es una voz activa, granular  granularidad adecuada de cambios.

esto de loss commit es importantisimo

como se ha trabjado con make, el makefile codifica informacion reproducible 
Se dijo : el makefile codifica lineas reproducibles, un target declara prerequisitos y comandos(receta) la palabra .PHONY evita choues con archivos homonimos deja en claro que el objetivo es logico
 - *.PHONY* (test , clean)
 - *las variables* := ?= parametricas rutas y flag

 y las automaticas como $< >  dan contexto al comando 

 - *reglas de patron*
escalan ----

*order * ....
un esqquelto sano tiende a trabajar con lint? (ShellCheck)  es de bash 

para un codigo sano incluir test, build , pack y clean 
asegura la calidad continua,

# que tiene que ver makefile con git , que tiene que ver git con make?

cuando hablamos de make hablamos de casi un lenguaje de programacion, cuando se trabja con make, make orquesta tareas repetibles, pero git GOBIERNA la historia y la colaboracion 
en make tenenos target y encademos en una arbol para lograr idempotencia? 

validamos make -j paraleliza
make -n 
make verify *checksum*
make 

git-describe.
git aporta ramas y flujos verificables, se puede usar estategias de ramificacion? para reducir eel tiempo de espera,,, los status check,,,den devops todo se junta, el pipeline ejecuta make como contrato unico , *pipeline como codigo* git es una fuente de verdad

cuando se hace make realese deploy usa variables de entorn para separa..que?

y los ..sirven de forensi
primerproyecto aegurar ciclos cortos , observabiidad, git que se cambia, make como se ejecuta???

estrategias de merge limpieza de historial .....
tecnicas : 
- fast forward (-ff) esto muevee el puntero cunado no hubo commit en la... o tras un rebase
- No-fast forward , commmit con 2 padres, registra el hito de modificacion

suash (--squash) multiples commit de ramas en make, en ramas compartir requiere disciplina , para no romper el historial publicado

cuando se tiene commit con multiples padres , eso ilustra como git modela una fusion no ff. 

el famosos trunk based development , promueeve ramas cortas, hacer feature hash , para que? TBD , el main debe ser siempre desplegable, cuando se trabaja con git/flow, main ,hotfixes,,, aporta......

cuando se trabaje con github flow se tiene que ajustar convenciones, nombre como hostfix? +

lo que se necesita es ......
los mensajes de commit son peizas de comunicaicon entre personas.. favorece lectura historica

no --ff fija → 
linealidad y granularidad →
ciclos confiables...

3-way merge ....

preservar la idea de momento de integracion : usamos para forzar commit de merge, squah para traer conteindo sin el grafo intermedio, 
cuando tienes merge de caracteristicas que pasan por ....
se habla de recursivo pero ahora de ord. 

git ghaph
git show



# clase miercoles 10 setiembre

git merge -no-off
usar three way mersh

pasos del non - fast - forward     punta:tip se refiere al ultimo commit
de una rama. ej : main o add-feature, cuando se refiere a un ancestro
X es ancestro de Y si llegas de Y a X .
que hace git un merge bash  un ¿commit comun? ,combina lo que cambio en main desde la base
con lo que cambio en add-feature desde la base.
git crea un commit de fusion  y mueve la referencia para que apunte a M 
imagen de MERGE
la instantanea de M tiene ambos,


# diferentes formas de merge en GIT
imagen FAST FORWARD

main no avanzo, que hace git, al integrar , solo mueve la refernecia 
el puntero de main al commit que ya tiene a add-feature, y lo demas 
ambos nombres de rama apuntan al mismo commit 

pero si main tuviera cambios ff no podria darse


imagen pasos de fast - forward merging
quedando lineal 

# git merge --squash
 main 
feature

main aun no tiene los cambios, on elcomando solo pasan los resultados de ambos commit(feature) a main
ej: 
git switch main
git main --squash feature
git commit -m "incorpa X (squahs de feature)" , solo vera el commit A + B

cuales el problema , si muestra un unico commit , es limpio es reversible, es util si A B son commit pequeños o ruidosos
se pierde el detalle A B en main?
se pierde granularidad para git biset  y   blame... busqueda binaria
cuando no hay regsistro de un merge habra... 
git toma el cambio aumlado de l aotra rama y lo aplica al directorio principal, no crea commit de mersh, cambios sin confirmar....

en luggar de mezclar la historia , toma todos los cambios de la rama fuente y ...en la rama destino
