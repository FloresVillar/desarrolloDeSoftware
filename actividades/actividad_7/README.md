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

## Variantes utiles DevOps/DevSecOps
1. (A) Fast-Forward Only (merge seguro)
Se pretende evitar merges implícitos , si no es FF , falla<br>
- 
```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git branch
* feature-ffonly
  main
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ echo "titulo archivo prueba" > archivo.txt
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git add archivo.txt
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git commit -m "agrega archivo.txt"
[feature-ffonly 2500464] agrega archivo.txt
 1 file changed, 1 insertion(+), 1 deletion(-)
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git merge --ff-only feature-ffonly
Already up to date.
```
evidencias
```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git log --oneline --graph --decorate --all --first-parent > evidencias/09-ff-only.log
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ cat evidencias/09-ff-only
.log
* 2500464 (HEAD -> feature-ffonly) agrega archivo.txt
* 4b2c244 (main) agrega 04-confictos
* 0eabc23 resuelve conflicto en index.html
* d273f71 modifica index.html
* 0418736 agregfa index.html
* 7ec60c7 cread index.html
* 3d6b0b6 Merge branch 'feature-3'
* b77387c prepara el merge --squash
* 3507be5 modifica README en main
* 2acc929 Merge branch 'feature-2'
* 7c050af modifica README
* b9e9684 guarda README en main
* 046b6cc mofica README.md
* c8a9900 commit inicial
```
2. (B) Rebase + FF (historial lineal con PRs)
Linealidad sin merge commits
```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git add archivo2.txt
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ echo "archivo 3" > archivo3.txt
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git commit -m "agregando archivo2"
[feature-rebase 501f5f5] agregando archivo2
 1 file changed, 1 insertion(+)
 create mode 100644 archivo2.txt
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git add archivo3.txt
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git commit -m "agrega archivo3"
[feature-rebase c1868f9] agrega archivo3
 1 file changed, 1 insertion(+)
 create mode 100644 archivo3.txt
```
fetch y rebase
```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git fetch origin 
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git rebase origin/main
Current branch feature-rebase is up to date.
```
fetch trae los cambios del repo remoto origin y descarga la info, pero no toca las ramas actuales<br>
Luego con rebase aplicamos los commit de feature-rebase en main
- integrando
```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$  git merge feature-rebase
Updating 4b2c244..56a9a48
Fast-forward
 archivo.txt               |  2 +-
 archivo1.txt              |  1 +
 archivo2.txt              |  2 ++
 archivo3.txt              |  1 +
 evidencias/09-ff-only.log | 14 ++++++++++++++
 5 files changed, 19 insertions(+), 1 deletion(-)
 create mode 100644 archivo1.txt
 create mode 100644 archivo2.txt
 create mode 100644 archivo3.txt
 create mode 100644 evidencias/09-ff-only.log
```
- evidencias
```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git log --graph --oneline --decorate --all --first-parent > evidencias/10-rebase-ff.log
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ ls
README.md     archivo2.txt        e.log       main.py
archivo.txt   archivo3.txt        evidencias
archivo1.txt  archivoCsquash.txt  index.html
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ cd evidencias
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2/evidencias$ ls
01-ff.log     03-squash.log      09-ff-only.log
02-no-ff.log  04-conflictos.log  10-rebase-ff.log
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2/evidencias$ tree -L 3 ~/Actividad7-CC3S2
/home/esau/Actividad7-CC3S2
├── README.md
├── archivo.txt
├── archivo1.txt
├── archivo2.txt
├── archivo3.txt
├── archivoCsquash.txt
├── e.log
├── evidencias
│   ├── 01-ff.log
│   ├── 02-no-ff.log
│   ├── 03-squash.log
│   ├── 04-conflictos.log
│   ├── 09-ff-only.log
│   └── 10-rebase-ff.log
├── index.html
└── main.py

2 directories, 15 files
```
3. (C) Merge con validacón previa(sin comitear)<br>
Se pretende correr linters, tests, escaneres antes de sellar el merge<br>

```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git checkout -b feature-validate
Switched to a new branch 'feature-validate'
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ echo "merge con validacion" >> README.md
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git add README.md
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git branch
  feature-ffonly
  feature-rebase
* feature-validate
  main
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git checkout main 
M       README.md
Switched to branch 'main'
Your branch is ahead of 'origin/main' by 5 commits.
  (use "git push" to publish your local commits)
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ echo "merge con validacion" >> README.md
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git add README.md
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git merge --no-commit --no-ff feature-validate
Already up to date.
```
4. 
```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ ls
README.md     archivo2.txt        e.log       main.py
archivo.txt   archivo3.txt        evidencias  scripts.sh
archivo1.txt  archivoCsquash.txt  index.html
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ bash -n scripts.sh
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git log --graph --oneline --decorate --all > evidencias/11-pre-commit-merge.log
```

```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ cat evidencias/11-pre-comm
it-merge.log
* bfbff88 (HEAD -> main) agrega evidencias
* 56a9a48 (feature-validate, feature-rebase) modifica archivo1
* 3f55485 modifica archivo2
* c1868f9 agrega archivo3
* 501f5f5 agregando archivo2
* 2500464 (feature-ffonly) agrega archivo.txt
* 4b2c244 (origin/main) agrega 04-confictos
*   0eabc23 resuelve conflicto en index.html
|\  
| * 9d471d8 agrega index.html
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
```
evidencias
```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ tree -L 3 ~/Actividad7-CC3S2
/home/esau/Actividad7-CC3S2
├── README.md
├── archivo.txt
├── archivo1.txt
├── archivo2.txt
├── archivo3.txt
├── archivoCsquash.txt
├── e.log
├── evidencias
│   ├── 01-ff.log
│   ├── 02-no-ff.log
│   ├── 03-squash.log
│   ├── 04-conflictos.log
│   ├── 09-ff-only.log
│   ├── 10-rebase-ff.log
│   └── 11-pre-commit-merge.log
├── index.html
├── main.py
└── scripts.sh
```
4. (D) Octupus Merge (varias ramas a la vez)  

```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git checkout -b feat-b
Switched to a new branch 'feat-b'
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ echo "feat-b" >> README.md
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git add README.md
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git commit -m "modifica feat-b"
[feat-b f929a76] modifica feat-b
 1 file changed, 1 insertion(+)
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git checkout main
Switched to branch 'main'
Your branch is ahead of 'origin/main' by 7 commits.
  (use "git push" to publish your local commits)
```
```bash
  (use "git push" to publish your local commits)
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git log --graph --oneline --decorate --all > evidencias/12-octupus.log
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ cat evidencias/12-octupus.
log
* f929a76 (feat-b) modifica feat-b
* bd1c9ae (HEAD -> main) agrega evidencias
* bfbff88 (feat-a) agrega evidencias
* 56a9a48 (feature-validate, feature-rebase) modifica archivo1
* 3f55485 modifica archivo2
```
5. (E) Subtree (Integrar subproyectos conservando historial)<br>
Vendorizar /incrustar un repo externo en un subdirectorio 

- Opción liviana
```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git remote -v
origin  https://github.com/FloresVillar/Actividad7-CC3S2.git (fetch)
origin  https://github.com/FloresVillar/Actividad7-CC3S2.git (push)
```
```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git subtree add --prefix=vendor/demo  https://github.com/FloresVillar/Actividad7-CC3S2.git main
git fetch https://github.com/FloresVillar/Actividad7-CC3S2.git main
From https://github.com/FloresVillar/Actividad7-CC3S2
 * branch            main       -> FETCH_HEAD
Added dir 'vendor/demo'
```

- sincronizando 
```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git subtree pull --prefix=
vendor/demo  https://github.com/FloresVillar/Actividad7-CC3S2.git m
ain
From https://github.com/FloresVillar/Actividad7-CC3S2
 * branch            main       -> FETCH_HEAD
Already up to date.
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ 

````
evidencias
```bash
sau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git log --graph --oneline --decorate --all > evidencias/13-subtree.log
```

6. (F) Sesgos de resolucion y normalizacion(algoritmo ORT)
```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git checkout -b feature-1
Switched to a new branch 'feature-1'
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ echo "sesgos de resolucion" >> README.md
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git add .
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git commit -m "sesgos de resolucion"
[feature-1 eb4b133] sesgos de resolucion
 3 files changed, 78 insertions(+)
 create mode 100644 evidencias/12-octupus.log
 create mode 100644 evidencias/13-subtree.log


 esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git checkout -b feature-2
Switched to a new branch 'feature-2'
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ echo "sesgo de resolucion"
 >> README.md
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git add README.md
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git commit -m "sesgo de resolucion en feature-2"
[feature-2 785d409] sesgo de resolucion en feature-2
 1 file changed, 1 insertion(+)

```
- solo conflictos
```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git merge -X ours feature-1
Updating f322e73..eb4b133
Fast-forward
 README.md                 |  1 +
 evidencias/12-octupus.log | 36 +++++++++++++++++++++++++++++
 evidencias/13-subtree.log | 41 ++++++++++++++++++++++++++++++++++
 3 files changed, 78 insertions(+)
 create mode 100644 evidencias/12-octupus.log
 create mode 100644 evidencias/13-subtree.log
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git merge -X ours feature-
2
Auto-merging README.md
Merge made by the 'ort' strategy.
```

- sensibilidad
```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git merge -X find-renames=90% feature-1
Already up to date.
esau@DESKTOP-A3RPEK
```
Se uso el comando merge -X<br>
Evidencias
```bash
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ git log --graph --oneline --decorate --all > evidencias/14-x-strategy.log
esau@DESKTOP-A3RPEKP:~/Actividad7-CC3S2$ cat  evidencias/14-x-strat
egy.log
*   5fea6ed (HEAD -> main) Merge branch 'feature-2'
|\  
| * 785d409 (feature-2) sesgo de resolucion en feature-2
* | eb4b133 (feature-1) sesgos de resolucion
|/  
*   f322e73 Add 'vendor/demo/' from commit '4b2c2444ce16fbdd3ae29a10aa5cae1098381738'
|\  
| | * f929a76 (feat-b) modifica feat-b
| |/  
|/|   
* | bd1c9ae agrega evidencias
* | bfbff88 (feat-a) agrega evidencias
* | 56a9a48 (feature-validate, feature-rebase) modifica archivo1
* | 3f55485 modifica archivo2
* | c1868f9 agrega archivo3
* | 501f5f5 agregando archivo2
* | 2500464 (feature-ffonly) agrega archivo.txt
|/  
* 4b2c244 (origin/main) agrega 04-confictos
*   0eabc23 resuelve conflicto en index.html
|\  
| * 9d471d8 agrega index.html
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