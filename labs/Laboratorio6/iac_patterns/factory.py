from typing import Dict, Any
import uuid
from datetime import datetime,timezone
import json

class NullResourceFactory: 
    @staticmethod #no necesita una instancia
    def create(name, triggers) -> Dict[str, Any]: 
        triggers = triggers or {}
        # Agrega un trigger por defecto: UUID aleatorio para asegurar unicidad
        triggers.setdefault("factory_uuid", str(uuid.uuid4())) 
        triggers.setdefault("timestamp", str(datetime.now(timezone.utc)))
        # Retorna el recurso estructurado como se espera en archivos .tf.json
        return {
            "resource": [{
                "null_resource": [{
                    name: [{
                        "triggers": triggers
                    }]
                }]
            }]
        }

class TimeNullResourceFactory(NullResourceFactory):
    @staticmethod 
    def crear(nombre,fmt):
        ts = str(datetime.now(timezone.utc).strftime(fmt)) 
        triggers = {}
        triggers.setdefault("ts",ts)
        return {
            "terraform":{
                "required_providers":{
                    "null":{
                        "source":"hashicorp/null"
                    }
                }
            },
            "provider":{
                "null":{}
            },
            "resource":[{
                "null_resource":[
                    {
                        nombre:[{
                            "triggers" : triggers
                        }]
                    }
                ]
            }]
        }
formato = '%Y-%m-%d'
obj = TimeNullResourceFactory()
resultado = obj.crear("fabrica_prueba",formato)
print(resultado)

with open("fabrica.tf.json","w") as f:
    json.dump(resultado,f,indent=2)
print("archivo tf.json generado")