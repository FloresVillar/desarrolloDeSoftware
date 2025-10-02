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
