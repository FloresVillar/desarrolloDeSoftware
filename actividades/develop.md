
## Agregar modulo monitor (Terraform)
La nueva infraestructura otorga flexilibilidad y es el estilo que se usara para la creacion del nuevo modulo monitor, este simula (en un primer estadio) ejecutando comandos cada cierto tiempo.
Entonces se declara la infraestructura para dicho modulo, en variables.tf
Se tiene la informacion siguiente:  informacion de la imagen, del contenedor, de la red y la politica de reinicio, respesctivamente

Mientras que en main se declara como sera la creacion del contenedor en base a una imagen , cuyo valor se obtiene expandiendo (inyectando) desde variables.tf, el codigo es util como documentacion.Se sabe que  **default = "alpine:latest"** es suficiente para terraform, pues se comunicara con el daemmon docker para construir la imagen y el consiguiente contenedor.

Lo mas interesante es el bloque 
```bash
command = [ "sh","-c","while true; do echo 'monitor en marha: ....'; sleep 10; done"]

```
Dentro del resource "docker_container" "monitor" { }  , que es el monitor encargado de la creacion de los logs cada cierto tiempo

En local-dev, se realiza la composicion del modulo monitor, que se suma a los ya existentes backend  y proxy , este bloque es crucial
```bash
module "monitor" {
  source = "../../modules/monitor"
  nombre_contenedor = "edge-cache-monitor"
  nombre_red        = docker_network.edge_cache.name
  politica_reinicio = var.restart_policy

  depends_on = [docker_network.edge_cache]
}

```
De modo tal que le pasamos los valores de las variables a las variables en monitor.
Se ejecuta de la siguiente manera 
```bash
docker rm -f edge-cache-monitor # limpia el contenedor existente
terraform init
terraform apply
Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
```
Se ha levantado la infraestructura , construido el contenedor y lanzado el servicio dentro del contenedor , en una misma red ,  junto con los otros contenedores con servicios dentro de ellos.
