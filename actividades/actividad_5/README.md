# Construyendo un pipeline Devops con Make y Bash
En *CONSTRUIR* en Se contruira un Makefile y probara unos scripts python
Make decidira si rehacer un target a partir de sus dependencias *esta frase no se profundiza del todo aun* , esto con el uso de variables automaticas
$@ nombre del target out/hello.txt 
$< primera dependencia
las configuraciones del script bash para el rastreo de errores ya nos son conocidas
set - eu set -o pipefail 
y el internal field separator IFS tambien
pero TRAP si es una herramienta interesantisima, nos permite una finalizacion ordenada, intercepta señales como SIGINT SIGTERM EXIT y permite ejecutar un comando del siguiente modo :
``trap comando_a_ejecutar`` SEÑAL1 SEÑAL2 ...
ej:
``trap exit 1 INT`` INT =2  cuando presionamos CTRL + C se ejecutara el comando exit 1
En *LEER*
en tanto que los operadores de asignacion := ?= suenan familiares, la primera se asigna al momento de la declaracion y la segunda es una asignacion condicional 
En *EXTENDER*
Acerca de los LINTERS: Un linter es una herramienta que analiza el codigo y avisa posibles problemas , malas practicas  o inconsistencias de estilo
No ejecuta el codigo solo lee y revisa, este detecta : 
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
```comando << DELIMITADOR``
los delimitadores pueden ser EOF , END , TEXT 
se prueba en el terminal
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
- El entorno es WSl , bueno la guia señala que se deberia trabjar en ~/ en la raiz de mi usuario, se hace eso y luego se copia dicha carpeta a actividad_5
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

Se creara ```src/__init__.py para compatibilidad en entornos antiguos de python 