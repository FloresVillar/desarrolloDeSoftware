# Resumen de la Lectura15
La infraestructura engloba todo lo necesario para ejecutar un app<br>
```bash
            almacenamiento
                    ↓
      computo  → INFRAESTRUCTURA ← red
                    ↑
            seguridad(politicas IAM)
```
Antes se configuraba todo esto desde CLI
## ¿Qué es IaC?
Infraestructura como codigo (infraestructura en archivos) , en este archivo declaramos la infraestructura que queremos<br>
```bash
    pasos ad-hoc            | definicion en archivos
    ssh server                  HCL o JSON(terraform),YAML (ansible)
    yum install nginx           qué recursos queremos
    ...
    crea la red                 "quiero una maquina con ngnix en la 
    luego la maquina                red X "
    despues instala nginx
```
```bash
recurso "aws_instance" "web"   {
    ami = "123"
    instance_type = "t2.micro"
} 
quiero(que debe existir) una instancia EC2 con estas caracteristicas
```

## ¿Qué no es IaC?
Ejecutar *configuracion.sh* sin los principios de IaC
 
## Principios de IaC 
```bash
        Reproducibilidad        Composibilidad
        (entornos identicos)     (no cambio innecesario de estado )
        Idempotencia            Envolvibilidad
```
Mientras Reproducibilidad e Idempotencias nos nos de alguna manera ya conocidas; veamos las dos propiedades nuevas<br>
Para ello revisemos la sintaxis de HCL(Hashicorp..) que es precisamente el lenguaje declarativo de configuracion que usaremos<br>
```bash
tipo_de_bloque "id1" "id2" {
    atributo = valor
    sub_bloques....
}
esto varia un poco dependiendo de que tipo de bloque es especifico se trate
resource tipo_definido_por_un_proveedor nombre_local {
    clave = valor
}
variable nombre_escogido {
    clave = valor  
}
recurso "aws_instance" "web"   {
    ami = "ami-0abcd1234"
    instance_type = "t2.micro"
} 
y module llama a las anteriores como lo haria una funcion
```

