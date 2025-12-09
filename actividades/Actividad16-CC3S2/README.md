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
