### Laboratorio CI/CD DevSecOps con github-actions
FLORES VILAR----20151445F<br>


Este repositorio entrega un pipeline completo de **DevSecOps** para un microservicio **Python** mínimo basado en `http.server`, con **Docker**, **Kubernetes (KinD)** y **GitHub Actions**. No usa `GITHUB_TOKEN` implícito, no requiere contraseñas ni secretos, y puede ejecutarse **100% local** con `Makefile`.

#### Estructura

- `src/` servicio HTTP (`/` y `/health`).
- `tests/` pruebas unitarias.
- `docker/` Dockerfile no-root y `HEALTHCHECK`.
- `compose.yaml` levantar servicio local para DAST.
- `k8s/` manifiestos y `kind-config.yaml`.
- `.github/workflows/ci-devsecops.yml` pipeline CI.
- `artifacts/` resultados de análisis (SBOM, SAST, SCA, DAST, scans).
- `.evidence/` evidencias (smoke tests, pods, etc.).
- `slsa/` ejemplo de layout para in-toto.
- `Makefile` tareas locales.

#### Requisitos locales

- Docker, Kind, kubectl
- Python 3.12
- Herramientas: `syft`, `grype`, `semgrep`, `bandit`, `pip-audit`, `in-toto-run`, (opcional `trivy`).
  > Instálalas según tu SO. El target `make ensure-tools` te indica faltantes.

#### Flujo local recomendado

```bash
make build           # construye imagen
make unit            # pruebas unitarias
make sast sca        # SAST + SCA
make sbom            # SBOM proyecto + imagen
make scan-image      # análisis de vulnerabilidades imagen
make compose-up      # lanza app en :8000
make dast            # ZAP baseline contra http://127.0.0.1:8000
make compose-down
make kind-up         # crea cluster KinD
make kind-load       # carga imagen local al cluster
make k8s-deploy      # despliega y espera rollout
make k8s-portforward # 127.0.0.1:30080 -> service
make smoke           # verifica /health en K8s
make attest          # ejemplo in-toto (local)
make evidence-pack   # tar.gz con artefactos y evidencias
```

#### GitHub Actions: conceptos clave

- **Workflow**: `.github/workflows/ci-devsecops.yml`. Se ejecuta en `push`, `pull_request` o manual via `workflow_dispatch`.
- **Jobs**: 1 job `pipeline` en `ubuntu-latest`.
- **Steps**: checkout, set up Python, construir imagen, pruebas, SAST/SCA, SBOM, escaneo de imagen, levantar `compose` y correr ZAP, recolectar artefactos.
- **Runners**: usa hosted runner; no requiere secretos.
- **Eventos y triggers**: definidos en la clave `on:` del workflow.
- **Secretos y variables**: **No requeridos** en este laboratorio. Evitamos pushes/registries externos.

#### Supply Chain (local)

- **SBOM** con `syft` (proyecto e imagen).
- **SCA** con `pip-audit`.
- **SAST** con `bandit` y `semgrep` custom `.semgrep.yml`.
- **Escaneo de imagen** con `grype` (y opcional `trivy`).
- **DAST** con `OWASP ZAP baseline` sobre servicio local/compose.
- **SLSA-like**: demostración de **in-toto** para registrar una evidencia del paso `build`.

#### Buenas prácticas incluidas

- Imagen **no root** y `slim` base.
- `HEALTHCHECK` en Docker y probes en K8s.
- Evidencias y artefactos en carpetas dedicadas.
- `imagePullPolicy: Never` + `kind load docker-image` para **KinD** offline.
- Port-forward para smoke tests sin exponer NodePort.

> Tip: Este repo puede integrarse a un **tablero Kanban** (Backlog -> Ready -> In Progress -> Code Review -> Testing -> Done) y capturar métricas (builds fallidos/exitosos, vulnerabilidades encontradas/mitigadas, etc.).

#### Objetivos del laboratorio
```bash
empaquetado de imagenes 
↓
test (test/)
↓
SAST /SCA 
↓
generacion de SBOM
↓escaneo de imagenes()
↓
levantar, DAST, checkHealth

```
#### ejercicio 3
1. 
```bash
bandit==1.7.9  #SAST 
semgrep==1.86.0 # estatico patrones
pip-audit==2.7.3 # requirements.txt
pytest==8.3.3 
requests==2.32.3
```
Breve analisis del funcionamiento de bandit, un ejemplo
```bash
```bash
# arg = archivo ; rm -rf
borrar(arg):
  os.system(f"rm {arg}")
  # ↓crea un subshell y 
  #sh -c "rm {arg}"  
  #sh -c "rm archivo ; rm -rf" #  # ←bandit evita esto
borrar("archivo ; rm -rf")
# se sugiere 
os.remove(arg)
```
Pero como o hace?, en una primera instancia uno pensaria que se compara lineas de codigo con "firmas" conocidas, osea analizar el codigo y buscar una cadena **os.sytem()** y comparar otras cadenas con posible inyeccion de comandos.. Nada parecido a ello, lo que hace es un analisis estatico de nuestro programa, pero, usando el arbol de sintaxis abstracta AST de python y algunas otras reglas.
Entonces se detallará que es un AST. Python toma nuestro .py , lo parsea y lo convierte en un arbol , entonces bandit podra 
- Analizar la estruuctura real del codigo
- Entender las llamadas , nombres y argumentos
- Detectar patrones en el codigo 
Tenemos , por ejemplo(cortesia de la IA):
Su arbol AST es:
```bash
Module
 └── FunctionDef(name='borrar')
      ├── arguments(args=[arg])
      └── body
           └── Expr
                └── Call
                     ├── func
                     │    └── Attribute
                     │         ├── value → Name(id='os')
                     │         └── attr='system'
                     └── args
                          └── JoinedStr  (f-string)
                               ├── Constant(value='rm ')
                               └── FormattedValue
                                    └── Name(id='arg')

```
Como se ve , su interpretacion es un tanto intuitivo.Lo que ahora hace bandit es usar sus **plugins/checks** cada cual detecta un patron de inseguridad, llamadas a os.system(), pero analizando cadenas sino mediante el AST , se buscan los nodos **call**,estos checks devuelven un **issue** con toda la info, el nombre del test, arichivo, linea, severidad. Luego bandit  recoge estos issues en un formato que nosostros especifiquemos(en el workflows por ejemplo se usan .json).
```bash
{
  "filename": "src/backup.py",
  "test_id": "B602",
  "issue_text": "Use of dangerous subprocess functions...",
  "line_number": 3,
  "severity": "HIGH",
  "confidence": "HIGH"
}
```
Sin embargo si vemos el AST, la cadena **borrar("archivo ; rm -rf")** , esto es, su valor , es transparente a bandit. Bueno aunque no lo analiza, chequea el call , ve que se usa el modulo os con un metodo system, lo considerará ya bastante peligroso.