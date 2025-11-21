from typing import List, Dict, Any
import json

class CompositeModule: 
    def __init__(self): 
        self._children = []
    def add(self, resource_dict):
        self._children.append(resource_dict)
    def export(self,base): 
        agregado = base.copy()
        agregado["resource"] = []
        for child in self._children: 
            agregado["resource"].extend(child.export()["resource"])
        return agregado
class ModuloRed:
    def export(self):
        return  {
             
            "resource":[ 
                {"null_resource":[
                    {"red":[
                        {
                            "triggers":{
                                "x" : 1
                            }
                        }
                    ]}
                ]}]}
class ModuloApp:
    def export(self):
        return {
            
            "resource":[
                {
                    "local_file":[
                        {
                            "app":[
                                {
                                    "content":"app",
                                    "filename":"app.txt"
                                }
                            ]
                        }
                    ]
                }
            ]
        } 

compuesto = CompositeModule()
compuesto.add(ModuloRed())
compuesto.add(ModuloApp())
base = {
    "terraform": {
        "required_providers": {
            "null": {"source": "hashicorp/null"},
            "local": {"source": "hashicorp/local"}
        }
    },
    "provider": {
        "null": {},
        "local": {}
    }
}
resultado =compuesto.export(base)
with open("main.tf.json","w") as f:
    json.dump(resultado,f,indent = 2)