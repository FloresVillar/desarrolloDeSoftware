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
