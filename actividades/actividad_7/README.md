# Actividad 7 : Explorando estrategias de fusión en Git
## Preambulo
- git init
- git add ``<archivo>``
- git commit -m "Mensaje"
- git checkout -b ``<rama>``
- git log 

## Glosario Clave
- DAG (Directed Acyclic Graph): representacion del historial , los commits son nodos y las fusiones conectan padres
- Merge commit :
- Parent/ Parent Primario (#1):commits padre del merge , el primario es la rama donde estabas al ejecutar ``git merge``
- Rama (branch) : puerto movil a un commit
- Rebase: reescribe commits de un rama sobre otra parte para un historial lineal
- PR (pull request) solicitud de fusion 

visualizar de DAG ``gitk --all``
Nota Windows/WSL (fin de linea y permisos) Para evitar "falsos cambios" y problemas de EOL/permisos
```bash
git config core.autocrlf input 
git config core.filename false
```
organizacion que se sugiere, un repo por cada seccion o limpiar entre ejercicios
```bash
mkdir -p ~/git-fusiones/ej01 && cd ~/git-fusiones/ej01
```
## Objetivos de aprendizaje
Comprender y aplicar fast-forward , no -fast-forward y squash, reconociendo ventajas / limitaciones e impacto en el historial (trabajo indivudual/equipos) 

## Prerrequisitos
```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git config --list
user.email=efloresv@uni.pe
user.name=FloresVillar
credential.helper=store
init.defaultbranch=main
core.repositoryformatversion=0
core.filemode=true
core.bare=false
```
```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git branch
* main
```
```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git log --graph --oneline --decorate --all > e.log
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ cat e.log
* edc1d74 (HEAD -> main, origin/main, origin/feature-1, origin/HEAD) agregar archivo main.py
* 83d2cc6 Initial commit
```
## Contexto y estrategias 
Las fusiones integran trabajo de multiples ramas.Elegir bien impacta trazabilidad, limpieza y auditoria

## Resumen de estrategias
- --ff : mueve el puntero sin crear merge commit,ideal en trabajo individual o secuencial
```bash
A --- B  (main)
       \
        C --- D  (feature)

A --- B --- C --- D  (main, feature)
```
- --no-ff: crea merge commit con 2 padres (preserva punto de integracion).Util en colaboración y auditorías
```bash
A --- B  (main)
       \
        C --- D  (feature)

A --- B --- C --- D
           \       /
            \-----M   (main)
```
- --squash : aplana VARIOS commits de la feature en UNO en main.Mantiene main limpia; no crea merge commit ni enlaza la rama en el DAG (se pierde detalle intermedio)
```bash
A --- B --- C --- D (main)
       \
        E --- F --- G (feature)

# después del merge --squash
A --- B --- C --- D --- M (main)

```
*buenas prácticas<br> 
- en pipelines estrictos considerar git merge --ff-only 
- Alternativa : "Rebase + FF" (Rebase and merge) para linealidad con trazabilidad via PR*

## Ejemplos prácticos 
1. Fusion Fast-Forward (git merge -ff)
- Repo nuevo , commit inicial en main
```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git add .
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git commit -m "commit inicial"
[main (root-commit) c8a9900] commit inicial
 4 files changed, 4 insertions(+)
 create mode 100644 README.md
 create mode 100644 archivo.txt
 create mode 100644 e.log
 create mode 100644 main.py
```
- Se crea una nueva rama , luego cambiamos a la rama main y hacemos el merge
```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git checkout -b feature-1
Switched to a new branch 'feature-1'
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git checkout main && merge feature-1
Switched to branch 'main'
Command 'merge' not found, but can be installed with:
sudo apt install rcs
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git checkout main && git merge fe
ature-1
Already on 'main'
Already up to date.
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git log --graph --oneline --decorate --all --first-parent > evidencias/01-ff.log
bash: evidencias/01-ff.log: No such file or directory
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ mkdir evidencias
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git log --graph --oneline --decorate --all --first-parent > evidencias/01-ff.log
```
- Evidencia 
```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ cat evidencias/01-ff.log
* c8a9900 (HEAD -> main, feature-1) commit inicial
```
2. Fusión No-fast-forward (git merge --no-ff)
- 
```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ echo "fusion No-fast-foward" >> README.md
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git add README.md
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git checkout -b add-feature
Switched to a new branch 'add-feature'
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git branch
* add-feature
  feature-1
  main

esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git checkout main && git merge --
no-ff add-feature
M       README.md
Already on 'main'
Already up to date.
```
- Evidencias
```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git log --graph --oneline --decorate --all > evidencias/02-no-ff.log
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ cat evidencias/02-no-ff.log
* c8a9900 (HEAD -> main, feature-1, add-feature) commit inicial
```
3. Fusión Squash (git merge --squash)
```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ echo "git merge --squash" >> README.md
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git checkout -b feature-3
Switched to a new branch 'feature-3'
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git checkout main && git merge --squash feature-3
Switched to branch 'main'
Already up to date. (nothing to squash)
```
- Evidencias
```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git log --graph --oneline --decorate --all  > evidencias/03-squash.log
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ cat evidencias/03-squash.log
* 046b6cc (HEAD -> main, feature-3) mofica README.md
* c8a9900 (feature-1, add-feature) commit inicial
```
```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ tree -L 2 ~/Actividad7-CC3S2
/home/esau/Actividad7-CC3S2
├── README.md
├── archivo.txt
├── e.log
├── evidencias
│   ├── 01-ff.log
│   ├── 02-no-ff.log
│   └── 03-squash.log
└── main.py

2 directories, 7 files
```
## Ejercicios guiados 
1. (A) Desde main se cambia de rama a feature-1 , una vez allí se modifica README.md realizando la preparacion y rastreo, cambiamos a main y  realizamos el merge previo resolucion de conflictos
```bash

esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git checkout feature-1
Switched to branch 'feature-1'
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ ls
README.md  archivo.txt  e.log  evidencias  main.py
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ echo "A) ejercicio guiado --ff " >> README.md
 git add README.md
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git commit -m "modifica README.md"
[feature-1 9421c0f] modifica README.md
 1 file changed, 1 insertion(+), 1 deletion(-)
 esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git merge --ff feature-1
error: Merging is not possible because you have unmerged files.
hint: Fix them up in the work tree, and then use 'git add/rm <file>'
hint: as appropriate to mark resolution and make a commit.
fatal: Exiting because of an unresolved conflict.
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git add README.md
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git commit -m "guarda README en main"
[main b9e9684] guarda README en main
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ cat README.md

# Actividad7-CC3S2fusion No-fast-foward
# Actividad7-CC3S2A) ejercicip guiado --ff 
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git merge --ff feature-1
Already up to date.
```
- merge --ff realiza un merge lineal , main no deberia haber sido modificado, luego si lo fuera entonces seria un escenario no idela para merge --ff 

2. (B) Creamos una nueva rama feature-2, modificamos README.md, realizamos luego e stanging  y el seguimiento , luego en main modificamos tambien README.md ,luego git add y git commit. entonces tenemos este escenario
```bash
A --- B -- D (main)
       \
        C   (feature)

A --- B --- D-------- M
           \         /
            \-- C - /   (main)
```
Luego realizando merge --no--f
```bash
 git branch
  add-feature
  feature-1
  feature-2
  feature-3
* main
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git merge --no-f feature-2
Merge made by the 'ort' strategy.
 README.md | 2 ++
 1 file changed, 2 insertions(+)
```

3. (C)  Squash 
En main se modifica README (add y commit) movemos el HEAD a feature-3 modificamos README(add y commit 1) , nuvemante en main modificamos README(add y commit) 
```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git add README.md
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git commit -m "modifica README en main"
[main 3507be5] modifica README en main
 1 file changed, 1 insertion(+)
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git branch
  add-feature
  feature-1
  feature-2
  feature-3
* main
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git checkout feature-3
Switched to branch 'feature-3'
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ echo "mofica nuevamente rREADME" >> README.md
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git add README.md
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git commit -m "modifica nuevamente README"
[feature-3 fbb6476] modifica nuevamente README
 1 file changed, 1 insertion(+)
```
Al intentar git merge --squash
```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git merge --squash feature-3
Auto-merging README.md
CONFLICT (content): Merge conflict in README.md
Squash commit -- not updating HEAD
Automatic merge failed; fix conflicts and then commit the result.
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ nano README.md
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ cat README.md

# Actividad7-CC3S2fusion No-fast-foward
<<<<<<< HEAD
# Actividad7-CC3S2A) ejercicip guiado --ff 
B) --no-ff 
B) --no-f en main
modifica README en ejercicio C) squash
=======
git merge --squash
C)squash 
mofica nuevamente rREADME
>>>>>>> feature-3
```

luego de corregir conflictos

```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git add README.md
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git commit -m "prepara el merge --squash"
[main b77387c] prepara el merge --squash
 2 files changed, 4 insertions(+), 1 deletion(-)
 create mode 100644 archivoCsquash.txt
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git merge --squash feature-3
Auto-merging README.md
Squash commit -- not updating HEAD
Automatic merge went well; stopped before committing as requested
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2
```
```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git log --oneline --graph --all --decorate
* b77387c (HEAD -> main) prepara el merge --squash
* 3507be5 modifica README en main
*   2acc929 Merge branch 'feature-2'
|\  
| * 1782ad2 (feature-2) modifica REAMDE.md
* | 7c050af modifica README
|/  
*   b9e9684 guarda README en main
|\  
| * 9421c0f (feature-1) modifica README.md
| | * fbb6476 (feature-3) modifica nuevamente README
| | * fa11e58 crea arhivoCsquash.txt
| | * a201cdd modifica READE.md
| |/  
|/|   
* | 046b6cc mofica README.md
|/  
* c8a9900 (add-feature) commit inicial
```
Como se puede apreciar en el DAG , con --squash se pierde información intermedia.

## Conflictos reales  con no-fast-forward
En main modificamos index.html
```bash
git checkout -b feature-update
Switched to a new branch 'feature-update'
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ echo "<h1>Proyecto CC3S2 (feature)</h1>" > index.html
```
En feature-update 
```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ echo "<h1>Proyecto CC3S2 (feature)</h1>" > index.html
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git add index.html
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git commit -m "agrega index.html"
[feature-update 9d471d8] agrega index.html
 1 file changed, 1 insertion(+)
 create mode 100644 index.html
```
y nuevamente en main
```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git checkout main
Switched to branch 'main'
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ echo "<h1>Proyecto CC3S2 (main)</h1>" > index.html
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git add index.html
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git commit -m "modifica index.html"
[main d273f71] modifica index.html
 1 file changed, 1 insertion(+), 1 deletion(-)
```
Viendo el conflicto
```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git status
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
        both added:      index.html

no changes added to commit (use "git add" and/or "git commit -a")
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git diff
diff --cc index.html
index 2a547e2,e9f19fe..0000000
--- a/index.html
+++ b/index.html
@@@ -1,1 -1,1 +1,5 @@@
++<<<<<<< HEAD
 +<h1>Proyecto CC3S2 (main)</h1>
++=======
+ <h1>Proyecto CC3S2 (feature)</h1>
++>>>>>>> feature-update
```
evidencias
```graph
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ cat evidencias/04-conflic
tos.log
*   0eabc23 (HEAD -> main) resuelve conflicto en index.html
|\  
| * 9d471d8 (feature-update) agrega index.html
* | d273f71 modifica index.html
* | 0418736 agregfa index.html
* | 7ec60c7 cread index.html
|/  
*   3d6b0b6 Merge branch 'feature-3'
|\  
| * fbb6476 modifica nuevamente README
| * fa11e58 crea arhivoCsquash.txt
| * a201cdd modifica READE.md
* | b77387c prepara el merge --squash
* | 3507be5 modifica README en main
* |   2acc929 Merge branch 'feature-2'
|\ \  
| * | 1782ad2 modifica REAMDE.md
* | | 7c050af modifica README
|/ /  
* |   b9e9684 guarda README en main
|\ \  
| |/  
|/|   
| * 9421c0f modifica README.md
* | 046b6cc mofica README.md
|/  
* c8a9900 commit inicial
```
- Pasos adicionales : usamos el comando echo INFO > ARCHIVO <br>
Luego de cada cambio se realiza el staging y 
el seguimiento<br>
con git diff y git diff se revisa el conflicto<br> 
Luego de la resolución del conflicto no hubo problemas adicionales<br>
- Pull requests pequños hacia origen , uso de ramas que especifiquen las responsabilidades

