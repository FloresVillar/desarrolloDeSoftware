# Construyendo un pipeline Devops con Make y Bash
En *CONSTRUIR*<br>
Se contruira un Makefile y probara unos scripts python<br>
Make decidira si rehacer un target a partir de sus dependencias *esta frase no se profundiza del todo aun* , esto con el uso de variables automaticas<br>
```bash
$@ nombre del target out/hello.txt 
$< primera dependencia
```
las configuraciones del script bash para el rastreo de errores ya nos son conocidas
``set - eu set -o pipefail`` 
y el internal field separator IFS tambien<br>
Pero TRAP si es una herramienta interesantisima, nos permite una finalizacion ordenada. Intercepta señales como SIGINT SIGTERM EXIT y permite ejecutar un comando del siguiente modo<br>
``trap comando_a_ejecutar SEÑAL1 SEÑAL2 ``<br>
``trap exit 1 INT`` donde INT =2  <br>
Cuando presionamos CTRL + C se ejecutara el comando exit 1<br>
<br>
En *LEER* ,los operadores de asignacion := ?= suenan familiares, la primera se asigna al momento de la declaracion y la segunda es una asignacion condicional.<br>
<br>
En *EXTENDER*,acerca de los LINTERS: Un linter es una herramienta que analiza el codigo y avisa posibles problemas , malas practicas  o inconsistencias de estilo,no ejecuta el codigo solo lee y revisa, este detecta : 
- Errores de sintaxis
- Variables sin usar
- Estilo inconsistente (espacios , identacion)
- Errores de seguridad(usar eval en bash o SQL sin sanitizar)
un ejemplo de eval: 
```bash 
cadena_comando = 'rm -rf '
eval $cadena_comando
```
esto es particularmente peligroso si  esa cadena tiene codigo malicioso,pues se interpretara como coomando de shell bash 

La guia de la actividad indica que el pipeline resultante compila , prueba y empaqueta scripts de pyhon demostrando practicas robustas de shell.

Es preciso exterdernos un poco en "practicas robustas de shell" como 
1. here-docs :
En bash son una forma muy util de redirigir un bloque de texto directamente a un comando o archivo , sin tener que usar muchos ``ècho`` ni archivos temporales
``comando << DELIMITADOR``<br>
los delimitadores pueden ser EOF , END , TEXT 
se prueba en el terminal
<br>
``cat << EOF > archivo.txt ``
permite ingresar texto hasta el EOF
y todo esto se redirecciona a un .txt

2. subshells:
un subshell es un proceso hijo que se crea cuando el shell necesita ejecutar un entorno separado, usa las variables del shell padre pero detro de su alcance
```bash
VAR = "hola"
(VAR="adios"; echo "dentro de subshell:" $VAR) 
echo "fuera de subshell: $VAR"  
```
como se ve () define el subshell
ademas una subshell se crea cuando se usa 
el comando de sustitucion ``$()``
cuando lanzamos un pipeline ``|``

la guia continua señalando,ademas, que el makefile esta endurecido : usa reglas claras, evita reglas implicitas y produce artefactos con empaquetado 100% reproducible(metadatos normalizados , orden estable)  

3. En este punto conviene precisar que son 'artefactos' 
Un artefacto es cualquier archivo o conjunto de archivos que resulta del proceso de construccion (build) o empaquetado de un software.
algunos ejemplos 
en C  .exe .out 
en java  .jar
en python .tar.gz (paquetes distribuidos)

'En pocas palabra es el achivo que se genera al ejecuta el codigo fuente'

Esto facilita CI/CD auditoria y bulids deterministas , como se espera en entornos profesionales

## Preparacion
- El entorno es WSl , bueno la guia señala que se deberia trabjar en ~/ en la raiz de mi usuario.
Sin embargo se trabaja directamente en actividad_5
- Dependencias: makee, bash, python3  son conocidos, pero los siguientes son nuevos, ``shellcheck shfmt ruff`` 
1. shellcheck : es un linter que analiza codigo y muestra errores comunes
```bash
for f in $FILES; do echo $f;done     
#al 'ejecutar' con     shellcheck script.sh
#indica que usemos comillas para evitar globbing 
for f in "$FILEs" ; do echo "$f";done
```
2. shfmt : es un formatter para scripts bash,ajusta la sangrias, espacios y llaves automaticamente 
```bash 
if [ $x -eq 1];then echo "uno";else echo "otro";fi
```
probando con shfmt -w script.sh
hara lo siguiente
```bash 
if [ $x -eq 1];then
    echo "uno"
else 
    echo "otro"
if
```
3. Ruff , es un linter y formatter para python , detecta posibles bugs , malas practicas
```python
import os,sys
def add(a,b): return a+b
```
ruff script.py
indica que hay multiples importaciones en una sola linea y que deberia haber un espacio luego de la coma
```python 
import os
import sys
def add(a, b):
    return a + b
```
un concepto más, un benchmark es una prueba de rendimiento util para medir tiempos de ejecucion , consum de memoria en general la eficiencia de un programa
```
La estructura inicial 
Laboratorio2/
├── Makefile
├── src/
│   ├── __init__.py
│   └── hello.py
├── scripts/
│   └── run_tests.sh
├── tests/
│   └── test_hello.py
├── out/
└── dist/
```
Se creara ``src/__init__.py`` para compatibilidad en entornos antiguos de python 

## Parte 1 : Construir - Makefile y Bash desde cero
Se crea un Makefile y un bash
src/hello.py

Algunos detalles acerca de la sintaxis de Makefile.

1. .VARIABLE importa las funcones de configuracion de bash,a saber, set -euo pipefail
entonces si queremos usar esas configuraciones se utiliza .SHELLFLAGS la asignacion al momento de declarar y las opciones de configuracion 
``.SHELLFLAGS := -eu -o pipefail -c``
y un detalle mas ``-c`` le dice a bash 'ejecuta el siguiente argumento como un comando/script
ejemplo :
```bash
bash -c "echo Hola; ls"
```
2. Lo siguiente es abarcar la sintaxis de ``MAKEFLAGS += --warn-undefined-variables --no-builtin-rules``
En este punto podria pensarse que cada linea de codigo aporta nueva sintaxis desconocida ,y es que realmente es asi , como sea. Veamos su interpretacion.
con ``MAKEFLAGS+=`` sumamos banderas a make en el sentido que indicamos como debe ejecutarse un comando ,asi, si se quiere que todos los comandos se ejecuten en modo estricto 
``MAKEFLAGS += --warn-undefined-variables ``.
Y desactivando las reglas implicitas (precisamente lo que se menciono) ``--no-builtin-rules`` 

3. Y una vez mas
.DELETE_ON_ERROR:
una bandera global para borrar el archivo target si su receta falla
ej :

```bash
.DELETE_ON_ERROR:

broken.txt:
    echo "mensjae" > broken.txt
    false
    echo "no ejecutado"

make broken.txt
echo "saludo" > broken.txt
false
make : *** [Makefile:4:broken.txt] error 1
rm broken.txt
```
make borra el archivo 

4. .DEFAULT_GOAL := help 
tal como indica su nombre sera el target que corre cuando no se indica a make cual ejecutar.
entonces para recalcar ``.VARIABLE`` son variables / directivas

5. Ahora bien la sintaxis export VARIABLE  := mezcla conceptos de variables de make con variables de entorno del sistema
```bash 
CC := gcc
```
es una variable dde make, visibles solo dentro de Makefile
Mientras que la palabra clave *clave* hace que la variable definida en Makefile se convierta en *variables de entorno * cuando make ejecuta los targets

una primera tentativa para entender que son las variables de entorno 
```bash
export VARIABLE_ENTORNO := saludos
VARIABLE_MAKE := hola

.PHONY:
demo_variable_entorno:
    echo $$VARIABLE_ENTORNO
.PHONY:
demo_variable_make:
    echo $$VARIABLE_MAKE
```
Al ejecutar con make y pasarle los valores de las variables, ambos tienen el mismo comportamiento , esto es que make les da prioridad
entonces investigando un poco mas se concluye que la utilidad de las variables de entorno(mucho verbo aparte) es que *las variables de entorno pueden ser referenciadas desde un script python (por ejemplo) actuan como puentes entre make y los programas o scripts que este ejecuta*<br>
Eso de momento

Las lineas de codigo que continuan en Makefile ya nos son familiares, ergo , obviamos su profundizacion 
sin embargo ; hay algo relativamente nuevo.<br>
```bash
build : $(OUT_DIR) /hello.txt
    $<  >  $@
```
build es un target con ``$(OUT_DIR)/hello.txt`` como prerrequisito  y este es a su vez un target con ``hello.py`` como prerrequisito<br>
``$(OUT_DIR)/hello.txt : $(SRC_DIR)/hello.py``<br>
Y luego la receta osea el cuerpo del target, que debe decodificarse con sumo cuidado y destreza<br>
```bash
    $@ es el target actual = out/hello.txt
    $(@D) es el directorio del target actual = out
    $< es el primer prerrequisito
```
se asegura que exista la carpeta out

```bash
    $(PYTHON) $< > $@
    es lo mismo que 
    $(PYTHON) hello.py > out/hello.txt 
```
Hermosas lineas de codigo

Clean es mas legible, aunque nunca esta de más interpretar su significado<br>
```'^ [caracteres digitos guiones]+'```<br>
```'inicio [a-zA-Z0-9_-] una o mas veces'```
<br>
osea por ejemplo se buscaria test-case
luego ``:``
luego ``.`` cualquier caracter
``*`` una o mas veces
``?`` minimo posible y ``##``<br>
ej: ``build: $()/hello.txt ## comentario`` 
 capturando toda la linea.

La salida se pasa a awk que separa el nombre del target y el comentario usando 
``':|##'`` como delimitadores, habrian 3 partes , el target, lo demas (dependencias) y el comentario, entonces nos quedamos con $1 y $3 , target y comentarios
``'{printf " %-12s %s\n",$1,$3}'``
```bash

help:  ## descripcion de los targets
	@grep -E '^[a-zA-Z0-9_-]+:.*##' $(MAKEFILE_LIST) | awk -F ':|##' '{printf "%-12s %s\n",$$1,$$3}'
#↑ aqui va bash -eu -o pipefail -c grep -E '^[a-zA-Z0-9_-]+:.*##' $(MAKEFILE_LIST) | awk -F ':|##' '{printf "%-12s %s\n",$$1,$$3}'
 
```
tal como indica el texto de la actividad <br>
``
help autodocumenta los objetivos escaneando el propio Makefile con grep y awk, y se fija como objetivo por defecto con .DEFAULT_GOAL := help
``<br>
okay ahora sabemos que hace makefile 


Y una vez editado todo el makefile, podemos señalar que este establece un entorno de construccion *estricto y determinista*.<br>
Esto define un flujo minimo para generar un artefacto desde un script.
Se fija el interprete de recetas a Bash ``SHELL := bash``<br>
Activamos el modos estricto con ``.SHELLFLAGS := -euo pipefail -c ``<br>
Se refuerza la deteccion de problemas con ``MAKEFLAGD +=--warn-undefined-variables --no-builtin-rules`` y desactiva reglas implícitas. 
```bash
mkdir test-make
cd test-make
echo "all: a.txt" > Makefile
make 
#make ejecuta el unico target 
touch b.o
make b.o
# como no hay un target b.o:  Make intenta usar reglas implicitas para compilar ej gcc
```
Exporta ``LC_ALL, LANG TZ a C/UTC`` para obtener salidas reproducibles(mensajes, ordenamientos y fechas estables). 
```bash
export SALUDO1 := "saludo1"
SALUDO2 := "saludo2"
all:
    @bash -c 'echo $$SALUDO1'
    @bash -c 'echo $$SALUDO2'
```
Se declara la variable dentro del Makefile y las exporta al entorno de procesos que make ejecute.Osea que cualquier comando que make ejecute en ese target verá a dicha variable con el valor asignado 
<br>
Efectivamente al ejcutar make all 
```bash
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/actividades/actividad_5$ make all
"saludo1"
```
Entonces al declarar las variables y exportarlas al entorno de ejecucion 
```bash
export LC_ALL := C  #variable de localizacion (controla el idioma)
export LANG   := C  #los mensajes usaran ASCII basico 
export TZ     := UTC  #zona horaria
#Exporta LC_ALL, LANG y TZ a C/UTC para obtener salidas reproducibles (mensajes, ordenamientos y fechas estables). 
```
La directiva .DELETE_ON_ERROR asegura que si una receta falla, no quede artefacto parcialmente generado. <br>
Finalmente help autodocumenta los objetivos escaneando el propio Makefile con ``grep  awk `` se fija el objetiivo por defecto con ``.DEFAULT_GOAL := help`` de modo que si invocamos make sin argumentos nos muestra la ayuda

### EJERCICIOS  
1. en el terminal :
```bash 
mkdir -p logs evidencia
make help | tee logs/make-help.txt
grep -E '^\.(DEFAULT_GOAL|PHONY):' -n Makefile | tee -a logs/make-help.txt
```
creamos las carpetas en cuestion, ignorando el comando si ya se han creado
se ejecuta el targets help , que como se describe en el DESENTRAÑAMIENTO de la sintaxis de este makefile<br>
Busca los nombres de los target y los comentarios (##)
con grep, luego esas lineas las pasamos a awk, quien se queda con esos nombres-comentarios fila a fila a modo de columnas, entonces ya unicamente usamos tee para copiar esa salida en make-help.txt.<br>
Nuevamente se usa grep para encontrar el patron .DEFAULT o PHONY , esto se ejecuta si usamos make sin argumentos, recordar que ``( | )`` es un grupo de ejecucion con varias opciones en este caso 2, el archivo donde buscar es Makefile , y otra vez se usa tee para guardar esa salida en make-help.
```bash
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/actividades/actividad_5$ cat logs/make-help.txt
all           ejecuta todas las tareas 
build         genera el archivo hello.txt 
clean         limpia los archivos generados
help          descripcion de los 1targets
```
2. 
```bash
rm -rf out dist
make build | tee logs/build-run1.txt
cat out/hello.txt | tee evidencias/out-hello-run1.txt
```
Se borra las carpetas out y dist
luego ejecutamos build , recordamos que este target tiene un prerrequisito OUT_DIR/hello.txt, se llama a ese prerrequisito  que tiene a su vez el prerrequisito saludo.py y el cuerpo del target crea out ``@D`` y guarda python saludo.py ``$<`` en out/hello.txt ``$@``
y esa salida es copiado en build-run1.txt via tee.<br>
Luego la salida de cat out/hello.txt (prerrequisto en make y a su vez target) se copia en evidencia/out-hello-run1.txt 
entonces hasta alli se sigue una ejecucion esperada, sin que haga falta contrastar el concepto de indempotencia usando timestamps.
```bash
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/actividades/actividad_5$ rm -rf out dist
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/actividades/actividad_5$ make build | tee logs/build-run1.txt
. out/hello.txt
python3 src/saludo.py > out/hello.txt
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/actividades/actividad_5$ cat out/hello.txt
Saludos,Todos
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/actividades/actividad_5$ cat out/hello.txt 
Saludos,Todos
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/actividades/actividad_5$ cat out/hello.txt | tee evidencias/out-hello-run1.txt
Saludos,Todos
```
Ahora bien al ejecutar 
```bash
make build | tee logs/build-run2.txt 
make: Nothing to be done for 'build'.
```
y que es eso? sencillo aunque no tanto, veamos 
build : out/hello.txt
su prerrequisito es out/hello.txt
entonces se analiza el target out/hello.txt : saludo.py
- si src/saludo.py  es mas nuevo osea HA CAMBIADO se ejecuta "rehace " our/hello "target"
- si out/hello.txt es mas nuevo esto es que src/saludo.py no ha cambiado no se hace nada<br>
Entonces build es el mismo ,no se hace nada.
Se deja todo como estaba, esto es indempotencia en acccion. INDEMPOTENCIA, que está en la comparacion automatica de timestamps entre targets y prerrequisitos
luego se ejecuta 

`` stat -c '%y %n' out/hello.txt | tee -a logs/build-run2.txt``

Otra vez algo nuevo, que tiene que analizarse, lo cual se hará<br>
stat = status, muestra atributos,  %y hora %n nombre del objetivo out/hello.txt  luego con tee en modo de append (no sobreescribiendo) guardamos la salida en logs/build-run2.txt
```bash
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/actividades/actividad_5$ cat logs/build-run2.txt
make: Nothing to be done for 'build'.
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/actividades/actividad_5$ stat -c '%y %n' out/hello.txt | tee -a logs/build-run2.txt
2025-09-30 09:57:45.173495647 -0500 out/hello.txt
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/actividades/actividad_5$ cat logs/build-run2.txt
make: Nothing to be done for 'build'.
2025-09-30 09:57:45.173495647 -0500 out/hello.txt
```

3. Forzando un fallo controlado para observar el modo estricto(-eu- o pipefail)  y .DELETE_ON_ERROR, este borrara cualquier artefacto (archivo generado al ejecutar el codigo fuente) en este caso los targets de Makefile
```bash 
rm -rf out/hello.txt
PYTHON = python4 make build ;echo "exit=$" | tee logs/fallo-python4.txt || echo "fallo(esperado)"
ls -ls out/hello | tee -a logs/fallo-python4.txt || echo "no existe python4"
```
Limpiamos el archivo  y pasamos el valor para la variable de make PYTHON que tendra preponderancia respecto al valor por defecto asignado mediante ``?=``<<br>
luego como sabemos build tiene out/hello.txt como prerequisito, va al target out/hello.txt , ejecuta el cuerpo<br> pero PYTHON = python4 no existe , entonces tendremos un error, se imprime mediante exit=$ ,codigo de salida del ultimo comando (make build), se pasa esa salida a fallo-python4.txt 
borrando cualquier artefacto corrupto generado
```bash
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/actividades/actividad_5$ rm -rf out/hello.txt
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/actividades/actividad_5$ PYTHON = python4 make build ;echo "exit=$" te | logs/fallo-python4.py || echo "fallo(esperado)"
PYTHON: command not found
bash: logs/fallo-python4.py: No such file or directory
fallo(esperado)
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/actividades/actividad_5$ ls -ls out/hello.txt | tee -a losg/fallo-python4.txt || echo "no existe ppython4"
tee: losg/fallo-python4.txt: No such file or directory
ls: cannot access 'out/hello.txt': No such file or directory
no existe ppython4
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/actividades/actividad_5$ cat logs/fallo-python4.txt
exit=2
```
4. 
```bash
make -n build | tee logs/dry-run-build.txt
make -d build | tee logs/make-d.txt 
grep -n "MENSAJE out/hello.txt objetivo" logs/make-d.txt
```


En make el flag -n activa el modo "dry-run" mostramos los comandos pero sin ejeecutarlos.
y acerca del flag -d (debug) , se imprime informacion detallada sobre como make decide rehacer targets, timestamps,dependencias ,reglas implicitas etc
grep -n es conocido 
```bash
    esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/actividades/actividad_5$ make -n build | tee logs/drry-run-build.txt
echo "." out/hello.txt
mkdir -p out
python3 src/saludo.py > out/hello.txt
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/actividades/actividad_5$ make -d build | tee logs/make-d.txt
GNU Make 4.3
Built for x86_64-pc-linux-gnu
Copyright (C) 1988-2020 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Reading makefiles...
```
5. 
```bash 
touch src/hello.py
make build | tee logs/rebuild-after-touch-src.txt

touch out/hello.txt
make build | tee logs/no-rebuild-after-touch-out.txt
```
porque como se vio en indempotencia, si saludo.py es modificado al tener timestamp mas reciente  y ser prerrequisito de out/hello.txt  y este ser prerequisito de build, se rehace el target.
Caso contrario si solo se modifica el target, el timestamp de saludo.py no cambio luego no se rehace el target<br>
Solo se reconstruye lo que necesita ser actualizado

6. Se comento al principio el uso de shellcheck y shfmt
```bash
command -v shellcheck >/dev/null && shellcheck scripts/run_tests.sh | tee logs/lint-shellcheck.txt || echo "shellcheck no instalado" | tee logs/lint-shellcheck.txt
command -v shfmt >/dev/null && shfmt -d scripts/run_tests.sh | tee logs/format-shfmt.txt || echo "shfmt no instalado" | tee logs/format-shfmt.txt
```
```bash
@@ -1,10 +1,10 @@
-#!/usr/bin/env bash 
+#!/usr/bin/env bash
 set -o errexit
 set -o nounset
 set -o pipefail
 
 IFS=$'\n\t'
-umask 027 
+umask 027
 set -o noclobber #>
 
 PY = "${PYTHON:-python3}"
@@ -13,30 +13,27 @@
 
 tmp="$(mktemp)"
 
-cleanup(){  #limpieza ordenada y rollback
-    error="$1"
-    rm -rf "$tmp"
-    if [ -f "${SRC_DIR}/saludo.py.bak" ];then
-        mv -- "${SRC_DIR}/saludo.py.bak" "${SRC_DIR}/saludo.py"
-    fi
-    exit "$error"
+cleanup() { #limpieza ordenada y rollback
+       error="$1"
+       rm -rf "$tmp"
+       if [ -f "${SRC_DIR}/saludo.py.bak" ]; then
+               mv -- "${SRC_DIR}/saludo.py.bak" "${SRC_DIR}/saludo.py"
+       fi
+       exit "$error"
 }
 
 trap 'cleanup $?' EXIT INT TERM
 
-check_deps(){ #checkea dependencias[]
-    local -a array_deps=("$PY" grep)
-    for dep in "${array_deps[@]}";do
-        if ! command -v "$dep" > /dev/null 2>&1;then
-            echo "error: $dep no instalado" >&2
-            exit 1
-        fi
-    done
+check_deps() { #checkea dependencias[]
+       local -a array_deps=("$PY" grep)
+       for dep in "${array_deps[@]}"; do
+               if ! command -v "$dep" >/dev/null 2>&1; then
+                       echo "error: $dep no instalado" >&2
+                       exit 1
+               fi
+       done
 }
 
-run_tests(){
-    
-}
+run_tests() {
 
-
-
+}
```
7. El siguiente bloque de codigo es muy interesante.
```bash
mkdir -p dist
tar --sort=name --mtime='@0' --owner=0 --group=0 --numeric-owner -cf dist/app.tar src/hello.py
gzip -n -9 -c dist/app.tar > dist/app.tar.gz
sha256sum dist/app.tar.gz | tee logs/sha256-1.txt
```
con tar estamos empaquetando el archivo src/hello.py
en dist/app.tar , con opciones "estandar" es que en si cada flags es un mundo

con gzip comprimimos el .tar dist/app.tar  a  dist/app.tar.gz

con sha256sum creamos el hash del comprimido guardando este en logs/sha256-1.txt

```bash
rm -f dist/app.tar.gz
tar --sort=name --mtime='@0' --owner=0 --group=0 --numeric-owner -cf dist/app.tar src/hello.py
gzip -n -9 -c dist/app.tar > dist/app.tar.gz
sha256sum dist/app.tar.gz | tee logs/sha256-2.txt

diff -u logs/sha256-1.txt logs/sha256-2.txt | tee logs/sha256-diff.txt || true
```
 las 3 lineas sigueintes hacen lo mismo,empaquetamos , comprimimos sin considerar metadatos y comprimimos, se hashea el comprimido y el hash resultante se espera , sea el mismo 
```bash
diff -u logs/sha256-1.txt logs/sha256-2.txt | tee logs/sha256-diff.txt || true
tar: src/hello.py: Cannot stat: No such file or directory
tar: Exiting with failure status due to previous errors
b1dd88cdd8bf09af2539d0b345e647129d8fd55c92b6d824b6ecc53efd531028  dist/app.tar.gz
tar: src/hello.py: Cannot stat: No such file or directory
tar: Exiting with failure status due to previous errors
b1dd88cdd8bf09af2539d0b345e647129d8fd55c92b6d824b6ecc53efd531028  dist/app.tar.gz
```
- --sort=name ordena los archivos dentro del tar alfabéticamente, eliminando variabilidad por orden de listado.

- --mtime='@0' fija la fecha de modificación de todos los archivos, evitando que el timestamp cambie el hash.

- --owner=0 --group=0 --numeric-owner normaliza propietario y grupo, evitando diferencias entre sistemas o usuarios.

- gzip -n suprime timestamps en el encabezado de compresión, y -9 solo afecta la compresión, no el contenido reproducible.

8. 
```bash
cp Makefile Makefile_bad
# (Edita Makefile_bad: en la línea de la receta de out/hello.txt, reemplaza el TAB inicial por espacios)
make --file Makefile_bad build 2>&1 | tee evidencia/missing-separator.txt || echo "error reproducido (correcto)"
```

Cuando Make ejecuta un Makefile, las recetas deben comenzar estrictamente con un TAB para diferenciar comandos de dependencias y targets. Si se usan espacios, Make no puede distinguir la receta y produce el error “missing separator”.

El flujo de la actividad reproduce esto: se copia el Makefile original, se reemplaza el TAB de la receta de out/hello.txt por espacios, y al ejecutar make -f Makefile_bad build se obtiene el error, confirmado en missing-separator.txt.

Este comportamiento garantiza que Make interprete correctamente la estructura de dependencias y comandos. Para diagnosticarlo rápido, se puede usar make -n o revisar la línea señalada en el mensaje de error, buscando líneas de receta que no comiencen con TAB.
*creaditos a gpt la explicacion anterior *
se puede decir que para codear la linea de comandos hacemos TAB,
TAB @cmd1
TAB @cmd2
asi mientras que para el prerrequisito
target:ESPACIO prerrequisito
eso es 

### creando un script bash
- cleanup

- deps
    ``local`` palabra clave para determinar un ambito local para una variable, luego declaramos un array via ``-a``  el array es ``deps`` asignandole dos elementos
    ``=("$PY" grep)``
    luego recorremos el array ``for dep in ${deps[@]};``
    y verificamos si python3 y grep estan instalados o no

- run_test 
    dos variables locales , a ``output `` se le asgina la salida del comando de sustitucion 
```bash 
    $(python3 argumento1_pasado_al_invocar_run_test)    
```
luego ``if !`` si no se encuentra "mensaje en saludo.py" entonces el test se asume como fallido
```bash
#!/usr/bin/env bash 
set -o errexit
set -o nounset
set -o pipefail

IFS=$'\n\t'
umask 027 
set -o noclobber #>

PY="${PYTHON:-python3}"

SRC_DIR="src"

tmp="$(mktemp)"

cleanup(){  #limpieza ordenada y rollback
    error="$1"
    rm -rf "$tmp"
    if [ -f "${SRC_DIR}/saludo.py.bak" ];then
        mv -- "${SRC_DIR}/saludo.py.bak" "${SRC_DIR}/saludo.py"
    fi
    exit "$error"
}

trap 'cleanup $?' EXIT INT TERM

check_deps(){ #checkea dependencias[]
    local -a dependencias=("$PY" grep)
    for dep in "${dependencias[@]}";do
        if ! command -v $dep  >/dev/null   2>&1;then
            echo " $dep no instalado" >&2
            exit 1                                                                                          
        fi
    done
}

run_tests(){
    local archivo="$1"
    local salida=$("$PY" "$archivo")
    if ! echo "$salida" | grep -F -i -q "Saludos,Todos";then 
        echo "Test fallido, salir!" >&2
        mv -- "$archivo" "${archivo}.bak" || true
    exit 2
    fi
    echo "Test pasó: $salida"
}

probando_pipefail(){
    echo "probando pipefail"
    set +o pipefail
    if false | true | false;then
        echo "pipefail sin deteccion de errores en pipeline status(0)"
    fi
    set -o pipefail 
    if false | false | true;then
        echo ".."
    else 
        echo "pipefail con deteccion de errores en pipeline status (1)"
    fi
}   
 probando_noclobber(){
    cat <<'EOF' >|"$tmp"
    linea1 
    linea2
    linea3
    linea4
EOF
}

check_deps
run_tests "${SRC_DIR}/saludo.py"
probando_pipefail

```
## ejercios
- Ejecutando en un entorno limpio
```bash
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/actividades/actividad_5$ make clean
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/actividades/actividad_5$ bash scripts/run_tests.sh
Test pasó: Saludos,Todos
probando pipefail
pipefail con deteccion de errores en pipeline status (1)
```
- Editando saludo.py
```bash
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/actividades/actividad_5$ bash scripts/run_tests.sh
  File "/home/esau/desarrolloDeSoftware/actividades/actividad_5/src/saludo.py", line 4
    #print(saludo("Todos"))
IndentationError: expected an indented block after 'if' statement on line 3
Test fallido, salir!
```
- Ejecutando bash -x scripts/run_test.sh
```bash
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/actividades/actividad_5$ bash -x scripts/run_tests.sh
+ set -o errexit
+ set -o nounset
+ set -o pipefail
+ IFS='
        '
+ umask 027
+ set -o noclobber
+ PY=python3
+ SRC_DIR=src
++ mktemp
+ tmp=/tmp/tmp.HNno31JGno
+ trap 'cleanup $?' EXIT INT TERM
+ check_deps
+ dependencias=('python3' 'grep')
+ local -a dependencias
+ for dep in "${dependencias[@]}"
+ command -v python3
+ for dep in "${dependencias[@]}"
+ command -v grep
+ run_tests src/saludo.py
+ local archivo=src/saludo.py
++ python3 src/saludo.py
  File "/home/esau/desarrolloDeSoftware/actividades/actividad_5/src/saludo.py", line 4
    #print(saludo("Todos"))
IndentationError: expected an indented block after 'if' statement on line 3
+ local salida=
+ echo ''
+ grep -F -i -q Saludos,Todos
+ echo 'Test fallido, salir!'
Test fallido, salir!
+ mv -- src/saludo.py src/saludo.py.bak
+ exit 2
+ cleanup 2
+ error=2
+ rm -rf /tmp/tmp.HNno31JGno
+ '[' -f src/saludo.py.bak ']'
+ mv -- src/saludo.py.bak src/saludo.py
+ exit 2
```
la expansion de PY ``python3``
de tmp ``tmp=/tmp/tmp.HNno31JGno``
del array dependencias ``dependencias=('python3' 'grep')``
de grep ``grep -F -i -q Saludos,Todos``

- Sustituyendo ``salida = $("$PY" "$archivo")`` en ``if ! $("$PY" "$archivo")`` en lugar de ``if ! "$salida"``
```bash
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/actividades/actividad_5$ bash scripts/run_tests.sh
scripts/run_tests.sh: line 45: salida: unbound variable
```
## Parte 2 Leer y analizar un repositorio completo
```bash
import unittest
from src.hello import greet

class TestGreet(unittest.TestCase):
    def test_greet(self):
        self.assertEqual(greet("Paulette"), "Hello, Paulette!")

if __name__ == "__main__":
    unittest.main() 
```
Nos enrumbamos nuevamente en descubrir la sintaxis , esta vez unittest<br>
Unittest es el framework de pruebas unitarias estandar de la biblioteca estandar de Python.<br>
Permite escribir clases de prueba con metodos que validan el comportamiento<br>
El pilar conceptual es que cada prueba que una unidad de codigo haga exactamente lo que se supone debe hacer<br>


