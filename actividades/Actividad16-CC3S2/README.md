# Actividad 16
Antes que nada, se tiene que realizar un mea culpa, debido a que seguir las indicaciones de la AI sin saber realmente que se estaba haciendo , puede ser y de hecho fue fatal.En particular estos comandos
```bash
git filter-repo --invert-paths --path actividades/Actividad16-CC3S2/README.md
git push --force
```
Se intento **git log, git reflog** ,sin resultado favorable alguno.La ai no es tan inteligente si el usuario no lo es , claramente.

## Parte A
### A1
1. El monorepositorio permite la declaracion de la infraestructura basica inicial
2. El monorepositorio se rompe(ci lento por ejemplo) porque todos los modulos se componen en un unico **main.tf.json**.
3. identificar **modules/network** → extraer el historial **git filter-repo** → revisar **git log** → configurar **terraform validate,plan** , definimos el backend remoto **terraform {backend "s3" {..}}** → publicar la primera version semantica **git tag v1.0.0** → actulizar consumo en el monorepositorio original **source**
 
### A2
El versionado semantico indica el cuanto podria romper la nueva version, que tan compatibles son las nuevas funciones y si hay cambios menores respectivamente.Eso los especifican el MAJOR.MINOR.PATCH.Respecto a la etiqueta firmada, es coherente con el grado de compatibilidad que queremos , de modo que si tiene una certeza .

### A3
Cada modulo, proveedor o binario puede exponer una vulnerabilidad, de modo que usamos SBOM para generar la lista de componentes del modulo y asi validamos que lo que descargamos coincida con lo aprobado, bloqueamos binarios sin verificar (lockfile). La procedencia firmada SLSA nos mostrará que commit genero una version especifica de un modulo.Si no conocemos la procedencia no se tendra garantia de integridad.
En tanto que las etiquetas firmadas,indica que en produccion lo anterior se hizo. 
### A4
En lo referente a secretos , por ejemplo para usar **boto3** y poder manipular objetos aws se requiere establecer la conexion , ingresar el Acces Key ID    y el Secret Access Key.
```bash
boto3.Session = {
    aws_access...ACCESS KEY ID
    aws_secret...ACCESS KEY ID
}
```
Se podria usar un gestor de secretos como via **aws_secretmanager_secret**, los roles de IAM son otra herramienta, se puede definir un rol con politicas especificas correspondiente para acceder ver leer o escribir tal o cual recurso.Tamien tendrian que tener una validez de pocos minutos, como las claves de verificacion usuales. Desde luego la separacion  de entornos , las claves deben ser propias de sus respectivos ambitos **dev** o **prod** , es recomendable usar ambos indistintamente.
Acerca de privilegio minimo en AIM, entiendo que aws hace propio estos principios y los concreta en las politicas (que tiene muuchos) de los roles para los instancias iam.
En IaC-seguridad se usa la receta **tools** quien ejecuta **secrets_scan.py** este script es muy interesante, algo sencillo pero potente , buscamos expresion (Patterns) que contengan 
```bash
re.compile(r'api[_-]?key\s*[:=]\s*["\']?[A-Za-z0-9_\-]{12,}'),
    re.compile(r'secret\s*[:=]\s*["\']?[A-Za-z0-9_\-]{12,}'),
    re.compile(r'password\s*[:=]\s*["\']?.{6,}')
``` 
De modo que se dara un mensaje de advertencia, una forma aterrizada y no transparente de detectar secretos.
### A5
Declarar y levantar infraestructura no es algo trivial, no se confia sin tener certeza de que los controles han sido solventados correctamente.Corroborando lo anterior via SBOM firmados (los componentes son confiables).De momento lo mas cercano son los resultados de **plan, apply** , estos nos permiten ver que configuraciones tenemos y quermos aplicar.
Desde luego los **drift** (desvios) se detectan via el ya conocido terraform apply.Toda la info que mantiene tfstate permitira que luego pueda auditarse adecuadamente, sin tener que buscar nada mas ,toda la info esta para unicamente ser leida.

## Parte B
### 1 
```bash
Requirement already satisfied: pluggy<2,>=1.5 in ./bdd/lib/python3.12/site-packages (from pytest==8.3.3->-r requirements.txt (line 2)) (1.6.0)
(bdd) esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/ejemplos/IaC-seguridad$ cp .env.example .env
(bdd) esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/ejemplos/IaC-seguridad$ make plan
Plan guardado en: ./.evidence/plan.json
Plan en ./.evidence/plan.json
```
Al ejecutar la receta plan via **make plan** hacemos **@ $(PY) tools/plan.y** , e script plan.py  , es aqui donde comparamos el estado deseado **desired** vs el estado actual **state** , el deseado se declara en **config.yaml** 
```bash
svc = BucketService(storage, evidence_dir)

    desired = svc.load_desired("desired/config.yaml")
    state = load_json("state/state.json")
    plan = svc.plan(desired, state)
```
### 2
El archivo .json generado es    
```bash
{
  "creates": [
    {
      "type": "bucket",
      "name": "research-artifacts",
      "public": false,
      "classification": "Restricted",
      "allowed_prefix": "experiments/"
    },
    {
      "type": "bucket",
      "name": "docs",
      "public": false,
      "classification": "Internal",
      "allowed_prefix": "handbooks/"
    }
  ],
  "updates": [],
  "outputs": {
    "count_desired_buckets": 2,
    "count_state_buckets": 0
  }
}
```
### 3 
Mientras que la receta policy via **make policy**  ejecuta el comando opa con muchas banderas, brevemente algo de OPA antes, opa permite evaluar politicas de seguridad definiendo primero una politica como 
```bash
package terraform

# Requiere entrada tipo tfplan para Conftest/OPA
#politica.rego
deny[msg] {
  some k
  output := input.planned_values.outputs[k]
  val := output.value
  is_string(val)
  re_match("(?i)(key|secret|password|token|api[_-]?key)", val)
  msg := sprintf("El output '%s' puede contener un secreto sensible", [k])
}
``` 
Y luego comprobando si nuestro tfplan la cumple **opa eval --format=pretty --data politica.rego --input tfplan.json "data.terraform.deny"**
En nuestro caso se hace esto via la receta **policy** de nuestro Makefile, antes se añaden 3 lineas de comando a la receta para obtener el ejecutable, darle permisos de ejecucion y guardarlo en la ruta los binarios
```bash
@curl -L -o opa https://openpolicyagent.org/downloads/latest/opa_linux_amd64
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

```
vemos que **opa eval -i ./.evidence/plan.json -d policies 'data.local.plan.** sigue la sintaxis opa eval -input PLAN/ESTADO -data POLITICA REGLA_A_EVALUAR , antes se cambia una de las politicas de policies usando **re_match("(?i)(key|secret|token|password)", sprintf("%v", [v]))**, la salida devuelta es 
```bash
(bdd) esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/ejemplos/IaC-seguridad$ make policy
{
  "result": [
    {
      "expressions": [
        {
          "value": [],
          "text": "data.local.plan.deny",
          "location": {
            "row": 1,
            "col": 1
          }
        }
      ]
    }
  ]
}
OPA RC=0
```
Una lista vacia de errores, RC=0
### 4