#monitor variables
variable "imagen_monitor" {
    description = "imagen monitor"
    type = string 
    default = "alpine:latest"
}

variable "nombre_contenedor" {
    description = "nombre contenedor"
    type = string 
    default = "edge-cache-monitor"
}

variable "nombre_red" {
    description = "nombre red para monitor"
    type        = string
}

variable "politica_reinicio" {
    description = " politica de reinicio"
    type = string
    default = "unless-stopped"
}
#montor varialbe.tf
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

resource "docker_image" "monitor" { 
  name = var.imagen_monitor
}

resource "docker_container" "monitor" {
  name = var.nombre_contenedor
  image = docker_image.monitor.image_id
  restart = var.politica_reinicio
  
  networks_advanced {
    name = var.nombre_red
  }

  command = [ "sh","-c","while true; do echo 'monitor en marha: ....'; sleep 10; done"]

  labels {
    label = "module"
    value = "monitor"
  }
}

output "nombre_contenedor" {
    value = docker_container.monitor.name
}

output "id_contenedor" {
    value = docker_container.monitor.id
}


#main locla-dev

# modulo monitor

module "monitor" {
  source = "../../modules/monitor"
  nombre_contenedor = "edge-cache-monitor"
  nombre_red        = docker_network.edge_cache.name
  politica_reinicio = var.restart_policy

  depends_on = [docker_network.edge_cache]
}

output "monitor_container" {
  value = module.monitor.nombre_contenedor
}