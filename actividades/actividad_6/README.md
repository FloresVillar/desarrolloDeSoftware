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
