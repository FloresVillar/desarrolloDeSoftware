# Actividad 9 : pytest + coverage + fistures + factories + mocking + TDD
## Requisitos tecnicos
```bash
(venv_act9) esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/actividades/Actividad9-CC3S2$ pip install -r requirements.txt
Requirement already satisfied: Werkzeug==2.1.2 in ./venv_act9/lib/python3.12/site-packages (from -r requirements.txt (line 2)) (2.1.2)
Requirement already satisfied: SQLAlchemy==1.4.46 in ./venv_act9/lib/python3.12/site-packages (from -r requirements.txt (line 3)) (1.4.46)
Requirement already satisfied: Flask==2.1.2 in ./venv_act9/lib/python3.12/site-packages (from -r requirements.txt (line 6)) (2.1.2)
Requirement already satisfied: Flask-SQLAlche......
```
## Makefile
El makefile , usamos algunas variables para lograr portabilidad y reproducibilidad.<br>
Usamos .PHONY para no tener problemas con nombres de archivos, en los targets de detallan las tareas de interes.<br>
En test_all ,por ejemplo, nos movemos a la carpeta *cd soluciones/aserciones_pruebas * luego ejecutamos las pruebas *$(PYTEST) -q *
```bash
test_all: deps 
	cd soluciones/aserciones_pruebas && $(PYTEST) -q || exit 1
	cd soluciones/pruebas_pytest	&& $(PYTEST) -q || exit 1
```



