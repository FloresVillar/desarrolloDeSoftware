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
