Ejercicio 3: "Pruebas de humo" y "Pruebas de regresión"
- Pruebas de humo locales ultrarrápidos

Imagina que tienes tres módulos en tu proyecto. Describe qué tres comandos básicos de Terraform ejecutarías en un smoke test unificado para "pasar la primera barrera" en menos de 30 segundos.
**terraform fmt -check** detecta cumplimiento de formato, no falsos positivos
**terraform validate** sintaxis, las palabras reservadas.
**terraform plan -refresh=false** revisa estado local. 

Justifica por qué cada comando (por ejemplo, fmt, validate, plan -refresh=false) aporta valor inmediato y evita falsos positivos en fases más profundas.

- Planes "golden" para regresión

Diseña un procedimiento teórico para generar y versionar un "plan dorado" de Terraform (plan-base.json) que sirva de referencia.

terraform plan -out=raw.plan
terraform show -json raw.plan > plan.json


¿Cómo detectarías diferencias semánticas (cambios involuntarios en recursos) sin que pequeñas variaciones de orden o metadatos ("timestamp", "UUID") disparen falsos fallos?

le quitamos timeatamps
jq 'del(.variables) | del(.. | .timestamp?)' plan.json > plan-base.json
luego a git



- Actualización consciente de regresión (opcional)


Propón una política de equipo que regule cuándo se actualizan los planes dorados. Por ejemplo: "solo al liberar una versión mayor" o "previa revisión de al menos dos compañeros".
¿Qué criterios objetivos definirías para aprobar o rechazar la actualización de un plan dorado?