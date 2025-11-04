VENV=venv_act9
PY=$(VENV)/bin/python 
PIP=$(VENV)/bin/pip 
PYTEST=$(VENV)/bin/pytest

.PHONY: venv deps test_all test_unit cov clean
venv: 
	python -m venv $(VENV)

deps:
	$(PIP) install -r requirements.txt

test_all: deps 
	cd soluciones/aserciones_pruebas && $(PYTEST) -q || exit 1
	cd soluciones/pruebas_pytest	&& $(PYTEST) -q || exit 1

test_unit:
	cd soluciones && $(PYTEST) -m "unit" -q

cov:
	cd soluciones/coverage_pruebas && $(PYTEST) --cov=models --cov-repor term-missing -q

clean:
	rm -rf .pytest **/__pycache__ htmlcov .coverage 

