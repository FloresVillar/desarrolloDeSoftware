import copy
from typing import Dict, Any
import json

recurso = {
    "resource" :[{
        "null_resource":[{
            "proto_prueba":[
                {
                    "triggers":{
                        "version":"1.0"
                    }
                }
            ]
        }]
    }]
}

class ResourcePrototype: 
    def __init__(self, resource_dict: Dict[str, Any]) -> None:
        self._resource_dict = resource_dict
    def clonar(self, mutador=lambda d: d) -> "ResourcePrototype":
        # Copia profunda para evitar mutaciones al recurso original
        new_dict = copy.deepcopy(self._resource_dict)
        # Aplica la función mutadora para modificar el clon si se desea
        mutador(new_dict)
        # Devuelve un nuevo prototipo con el contenido clonado
        return ResourcePrototype(new_dict)
    @property
    def data(self) -> Dict[str, Any]: 
        return self._resource_dict

def mutador(new_dict):
    new_dict["resource"][0]["null_resource"][0]["proto_prueba"][0]["triggers"]["welcome"] = "¡Hola!"
    new_dict["resource"].append({"local_file" : [{
        "welcome_txt": [{
            "content": "Bienvenido",
            "filename": "${path.module}/bienvenida.txt"
        }]
    }]})

obj = ResourcePrototype(recurso)
resultado = obj.clonar(mutador)
with open("prototype.tf.json","w") as f:
    json.dump(resultado.data,f,indent=2)
#luego terraform apply