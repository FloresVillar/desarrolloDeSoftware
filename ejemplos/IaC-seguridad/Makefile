PY=python


tools:
	@echo "[tools] Escaneo de secretos y formato (simple)"
	@$(PY) tools/secrets_scan.py . || (echo "Posibles secretos detectados. Revisa." && exit 2)
	@echo "OK"

plan:
	@$(PY) tools/plan.py
	@echo "Plan en ./.evidence/plan.json"

policy:
	@curl -L -o opa https://openpolicyagent.org/downloads/v0.48.0/opa_linux_amd64
	@chmod +x opa
	@sudo mv opa /usr/local/bin/
	@if command -v opa >/dev/null 2>&1; then \
		opa eval -i ./.evidence/plan.json -d policies 'data.local.plan.deny'; \
		RC=$$?; \
		echo "OPA RC=$$RC"; \
		exit $$RC; \
	else \
		echo "opa no instalado; omitiendo policy gate"; \
	fi

apply:
	@$(PY) tools/apply.py

drift-check:
	@$(PY) tools/drift_check.py

sbom:
	@$(PY) tools/sbom.py .

test:
	@pytest -q

help:
	@echo "targets: tools | plan | policy | apply | drift-check | sbom | test | help | clean"

clean:
	@echo "[clean] borrando infraestructura local y evidencia"
	rm -rf data/*
	rm -rf .evidence/*
	@echo "[clean] reseteando state/state.json"
	@echo '{ "version": 1, "resources": [] }' > state/state.json
	@echo "listo"

.PHONY: evidence
evidence:
	@echo "Generando archivo de evidencia..."
	@tar -cvf evidence-$(shell date +%Y%m%d).tar .evidence/