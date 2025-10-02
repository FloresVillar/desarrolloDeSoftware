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




