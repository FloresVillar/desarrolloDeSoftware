from jsonschema import validate,ValidationError
import os
from shutil import copyfile
import json
ENVS = []
for i in range(1,11):
    ENVS.append({"name": f"app{i}", "network": f"net{i}"})

M_DIR = "modules/simulated_app"
O_DIR = "environments_schema"

SCHEMA_V = {
    "type":"object",
    "properties":{
        "name" : {"type":"array"},
        "network":{"type":"array"}
    },
    "required":["name","network"]
}

SCHEMA_R = {
    "type" : "object",
    "properties":{
        "resource":{
            "type" : "array",
            "items":{
                "type":"object",
                "properties":{
                    "null_resource":{
                        "type":"array"
                    }
                },
                "required":["null_resource"]
            }
            
        }     
    },
    "required":["resource"] 
}

def render_write(env):
    env_dir = os.path.join(O_DIR,env["name"])
    os.makedirs(env_dir,exist_ok=True)
    copyfile(os.path.join(M_DIR,"network.tf.json"),os.path.join(env_dir,"red.tf.json"))
    plantilla  ={
        "resource" : [
            {
                "null_resource":[
                    {
                        env["name"]:[
                            {
                                "triggers":{
                                    "name":env["name"],
                                    "network":env["network"]
                                },
                                "provisioner":[
                                    {
                                        "local-exec":{
                                            "comnand":(f"echo 'arrancando'" f"{env['name']} en red {env["network"]}")
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }
    try:
        validate(instance=plantilla, schema=SCHEMA_R)
    except ValidateError as e:
        raise ValuError(f"error")
    with open(os.path.join(env_dir,"main.tf.json"),"w") as f:
        json.dump(plantilla, f, sort_keys=True,indent= 4)
    
if __name__=="__main__":
    if os.path.isdir(O_DIR):
        import shutil
        shutil.rmtree(O_DIR)
    for env in ENVS :
        render_write(env)
    print(f"ya genera{len(ENVS)} en {O_DIR}")