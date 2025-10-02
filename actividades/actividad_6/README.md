# Actividad 6: Introduccion a Git conceptos básicos y operaciones esenciales

## Conceptos basicos de Git : Comenzando con una experiencia basica

### git config: Nos presentamos a Git

Antes de hacer nada nos presentamos a Git via el comando ``git config``
```bash
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git config --global user.name "FloresVillar"

esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git config --global user.email "efloresv@uni.pe"
```
Este comando es usado para configurar Git a nivel de sistema
1. El nivel de system aplica a todos los usuarios y a todos los repositorios
2. El nivel global aplica a todos los repositorios de un usuario específico
3. El nivel local aplica a solo un repositorio

verificamos la presentacion hecha con el comando ``config --list``
```bash
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$
git config --list
user.email=efloresv@uni.pe
user.name=FloresVillar
```
### git init:  Donde comienza el viaje de nuestro codigo
Al igual que un gran viajee tiene su origen , en Git el viaje de nuestro codigo comienza con el comando ``git init`` <br>
Se usa para inicializar un nuevo repositorio de Git y comienza a rastrear directorios existentes.<br>
Al ejecutar este comando creamos un directorio .git 

Ahora estamos listo para sumergirnos en la gama de comandos de Git y comenzar a rastrear y actualizar el proyecto 
```bash
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git init
Reinitialized existing Git repository in /home/esau/Actividad6-CC3S2/.git/
```
Otra sería pasar un nombre como argumento de ``git init carpeta`` sin necesidad de usar ``mkdir``<br>
Una vez creado el directorio .git/ se usará ```git add```, que selecciona conscientemente los archivos a guardar entre los que se han editado, agregado o eliminado  y el comando ``git commit ``

### git add : Preparando nuestro código 
El comando ``git add`` es el puente entre hacer cambios en nuestro directorio de trabajo y prepararlos para almacenarlo permanentemente en el repositorio Git
```bash
    cambios en el directorio ------git add------>repositorio Git
```
Cuando modificamos nuestros archivos Git los detecta, pero no están listos automaticamente para convertirse en parte del historial<br>
Aqui es donde entra ``git add``
```bash
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ echo "aaa" > README.md
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ ls
README.md
```
El comando ``git status`` muestra el estado actual del repositorio , muestra que archivos tienen cambios que están siendo rastreados y cuales no.<br>
``Untracked files`` =  aun hay archivos de los cuales no estoy pendiente
```bash
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git status
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   README.md

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   README.md
```
README.md es un archivo nuevo para Git, no esta registrado , por lo tanto , está etiquetado como no rastreado, para moverlos a un estado rastreado usamos ``git add``
```bash
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git add README.md
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git status
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   README.md
```
Ahora Git reconoce a README.md como nuevo archivo y esta siendo rastreado<br>
Archivo modificado---- ``git add``--------->Staged<br>     
Espacio de trabajo------``git add``--------->preparado<br> 
``git add`` tienes otras opciones 
- git add .
- git add file1.md file2.md file3.md
- git *.md
### git commit: Registro de cambios
El comando ``git commit`` registra los cambios que has preparado con ``git add`` en el historial del repositorio. Esto nos permite rastrear los cambios

Una muy buena analogia *Imagina que estás jugando un videojuego desafiante. A medida que avanzas, a menudo guardarás tu juego para bloquear tus logros. Del mismo modo, cuando desarrollas software, guardarás tu trabajo usando git commit*

Cada commits es un punto de guardado al que se puede regresar mas tarde si se necesita.

Para cometer los cambios 
```bash
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git commit -m "commit inicial con README.md"
[main (root-commit) f0a0096] commit inicial con README.md
 1 file changed, 1 insertion(+)
 create mode 100644 README.md
```
La bandera -m es seguida de un mensaje CORTO Y DESCRIPTIVO que captura la esencia de lo que se ha hecho.Escribir buenos mensajes de *commits* , ayuda a entender el historial  y la intencion de los cambios

Con ``git status `` vemos si todos los cambios en el directorio de trabajo han sido guardados<br>
```bash
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git status
On branch main
nothing to commit, working tree clean 
```
El flujo de edicion, preparacion y commit sigue siendo el mismo sin importar cuan complejo sea nuestro proyecto
```bash
(1)Editar cambios-->(2)Preparar cambios--->(3)commits de cambios
                    staged
```
Cada commit genera una ID de commit unica.

### git log: Recorrer el arbol de commits
Una que se hemos realizado algunos commits para ver el historial de cambios<br>
El comando ``git log`` muestra una lista de commits realizados en un repositorio en orden cronologico inverso
El ultimo se muestra primero
```bash
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git log
commit f0a00966a0156667c7184f2e0d1638bf1f9a41a6 (HEAD -> main)
Author: FloresVillar <efloresv@uni.pe>
Date:   Wed Oct 1 21:18:47 2025 -0500

    commit inicial con README.md 
```
Muestra una lista de commit, cada commit tiene:
- Identificador SHA-1 unico 
- Detalles del committer 
- Marca de tiempo 
- Mensajes del commit 

Opciones 
- ``git log -p`` 
- ``git log --stat``
- ``git log --oneline``
- ``git log -graph``
- ``git log --author=""``

```bash
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git log --graph --pretty=format:'%x09 %h %ar (%an) %s'
*        f0a0096 17 hours ago (FloresVillar) commit inicial con README.md
```
Vemos la informacion del commit en un formato facil leer
Ejercicio:
```bash
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ echo "mi_contribucion" > MI_CONTRIBUCION.md
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ ls
MI_CONTRIBUCION.md  README.md
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ echo "README\n\nBienvenido la proyecto " > README.md
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ ls
MI_CONTRIBUCION.md  README.md
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git add .
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git commit -m "configura la documentacion base del repositorio"
[main 68762c5] configura la documentacion base del repositorio
 2 files changed, 2 insertions(+), 1 deletion(-)
 create mode 100644 MI_CONTRIBUCION.md
```
Luego agregmos codigo de ejemplo
```bash
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ echo "print(Hola Mundo)" > main.py
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ l
MI_CONTRIBUCION.md  README.md  main.py
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ cat main.py
print(Hola Mundo)
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git add .
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git commit -m "Agrega main.py"
[main 398ff3b] Agrega main.py
 1 file changed, 1 insertion(+)
 create mode 100644 main.py
```
Confirmamos en el log que esta correctamente registrado 
```bash
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git log --oneline
398ff3b (HEAD -> main) Agrega main.py
68762c5 configura la documentacion base del repositorio
f0a0096 commit inicial con README.md
```
Es una herramienta vital para navegar en el historial de nuestro codigo 
## Trabajar con ramas: La piedra angular de la colaboración
``git branch `` se puede usar para crear un historial del entorno paralelo <br>
Luego podemos fusionar esos múltiples entornos en uno, lo que permite que varias personas trabajen en ellos, dandole la flexibilidad para experimentar nuevas caracteristicas,correcciones de errores o incluso ideas totalmente vanguardistas sin afectar la base del código principal.

### git branch: Entendiendo los conceptos basicos de Git branch
Mostrando la lista de las ramas
```bash
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git branch
* main
```
creando una nueva rama
```bash
git branch feature/new-feature
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git branch
  feature/new-feature
* main
```
Las convenciones para los nombres de las ramas son importante para la comunicacion <br>
Un estandar comun es usar :
- feature/ 
- bugfix/
- hotix/

Seguido de una descripción, lo cual facilita que se entienda el proposito de la rama.<br>
Tambien se puede crear una rama a partir de una rama  o commit especifico, esto es util cuando se pretende crear una rama de caracteristicas(feature) o correción de errores(bugfix) que deba originarse desde una rama de desarrollo o stagging en lugar de desde nuestro branch  de trabajo actual.

```bash
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git branch feature/new-feature_2 f0a00966a0156667c7184f2e0d1638bf1f9a41a6
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git branch
  feature/new-feature
  feature/new-feature_2
* main
```
### git checkout switch: Cambiar entre ramas
En nuestro flujo de trabajo a menudo necesitamos cambiar de una rama a otra, en especial cuando se trabaja en multiples caracteristicas  o corrigiendo errores <br>
Cuando se trabaja en multiples ramas, volverse consciente del branch en la que se *está ACTIVAMENTE* es fundamental.<br>
En git, el termino HEAD se refire a la punta de la rama con la que se está trabajando activamente

Cambiar de la rama de trabajo actual es conoce como *cambiar de rama* el comando ``git checkout `` facilita ello

```bash
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git checkout feature/new-feature
Switched to branch 'feature/new-feature'
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git branch
* feature/new-feature
  feature/new-feature_2
  main
 ```
Cambiamos la posicion de HEAD , la punta de la rama a una rama llamada ``feature/new-feature``<br>
Con el comando ``git checkout `` cambia la posicion de HEAD (la punta de la rama) a una rama llamada ``feature/new-feature``<br>

### Ejercicios adicionales
#### Creando una rama desde una rama específica
Creamos el branch develop y movemos el HEAD a esa rama<br>
Creamos una nueva rama a partir de develop
```bash
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git branch develop
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git branch
  develop
* feature/new-feature
  feature/new-feature_2
  main
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git checkout develop
Switched to branch 'develop'
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git branch
* develop
  feature/new-feature
  feature/new-feature_2
  main
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git branch feature/login develop
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git checkout feature/login
Switched to branch 'feature/login'
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git branch
  develop
* feature/login
  feature/new-feature
  feature/new-feature_2
  main
```
#### Creando una rama desde un commit específico

```bash
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git log --oneline
398ff3b (HEAD -> feature/login, main, feature/new-feature, develop) Agrega main.py
68762c5 configura la documentacion base del repositorio
f0a0096 (feature/new-feature_2) commit inicial con README.md
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git branch hotfix/bugfix 68762c5
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git checkout hotfix/bugfix
Switched to branch 'hotfix/bugfix'
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git branch
  develop
  feature/login
  feature/new-feature
  feature/new-feature_2
* hotfix/bugfix
  main
```
Cambiando entre ramas con ``git switch`` una forma mas intuitiva.<br>
```bash
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git switch feature/new-feature
Switched to branch 'feature/new-feature'
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git branch
  develop
  feature/login
* feature/new-feature
  feature/new-feature_2
  hotfix/bugfix
  main
```
Para crear una nueva rama y cambiar a ella en un solo paso se puede usar ``git checkout -b``.
```bash
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git checkout -b feature/another-new-feature
Switched to a new branch 'feature/another-new-feature'
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git branch
  develop
* feature/another-new-feature
  feature/login
  feature/new-feature
  feature/new-feature_2
  hotfix/bugfix
  main  
```
``git switch -c `` es equivalente a ``git checkout -b``
 ```bash
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git branch
  develop
* feature/another-new-feature
  feature/login
  feature/new-feature
  feature/new-feature_2
  hotfix/bugfix
  main
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git switch -c feature/another-new-feature-switch
Switched to a new branch 'feature/another-new-feature-switch'
 ```
### git merge : Fusionando ramas
Una vez realizado los cambios y se hayan probado a fondo es posible poder integrar esos cambios nuevamente en el branch ``main`` u otra rama.<br>
Esta operacion se conoce como ```merge``.
```bash
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git checkout main
Switched to branch 'main'
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git merge feature/new-feature
Already up to date.
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git branch
  develop
  feature/another-new-feature
  feature/another-new-feature-switch
  feature/login
  feature/new-feature
  feature/new-feature_2
  hotfix/bugfix
* main
```
Se fusiona lineas con diferentes historiales.La fusión puede ser una operación sencilla ,pero esto puede complicarse si hay conflictos entre ramas.<br>
En tales casos se requerirá la intervención manual para resolver conflictos.

### git branch -d : Eliminando una rama 
Una vez que una rama ha sido fusionado  con éxito y ya no es necesaria, se  puede eliminar
```bash
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git branch -d feature/new-feature
Deleted branch feature/new-feature (was 398ff3b).
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git branch
  develop
  feature/another-new-feature
  feature/another-new-feature-switch
  feature/login
  feature/new-feature_2
  hotfix/bugfix
* main
```
### Preguntas
- Con los comandos de los cuales se dispone git add para preparar y git commit para ser rastreado y por supuesto git log, todos estos otorgan una organización clara
- Las ramas permiten crear entornos paralelos donde se puede desarrollar caracteristicas o "casos de usos" particulares
- 
```bash
esau@DESKTOP-A3RPEKP:~/Actividad6-CC3S2$ git log
commit 398ff3b968d1351000999f2dd569e1ac90ba5cb3 (HEAD -> main, feature/login, feature/another-new-feature-switch, feature/another-new-feature, develop)
Author: FloresVillar <efloresv@uni.pe>
Date:   Thu Oct 2 14:10:34 2025 -0500

    Agrega main.py

commit 68762c50a2f9a90262333d83ba8964406360d9aa (hotfix/bugfix)
Author: FloresVillar <efloresv@uni.pe>
Date:   Thu Oct 2 14:03:46 2025 -0500

    configura la documentacion base del repositorio

commit f0a00966a0156667c7184f2e0d1638bf1f9a41a6 (feature/new-feature_2)
Author: FloresVillar <efloresv@uni.pe>
Date:   Wed Oct 1 21:18:47 2025 -0500

    commit inicial con README.md
```
- 
```bash
``git branch new--git checkout new-->git checkout main-->git merge new
```
### Ejercicios
#### Ejercicio 1: Manejo avanzado de ramas y resolución de conflictos
Objetivo : Practicar 