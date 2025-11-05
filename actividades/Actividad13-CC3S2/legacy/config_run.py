import os
import json

with open("config.cfg","r") as file_config:
    puerto = file_config.read().split("=")[1].strip()
with open("run.sh","r") as file_run:
    comando = file_run.read().split("\n")[2].split(" ")[0].strip()
cuerpo_terraform_json = { "resource" : [
{
    "null_resource" :[
        {
            "config_run": {
                "provisioner":{
                    "local-exec":{
                        "command":f"{comando} 'ARRANCA puerto {puerto} '"
                    } 
                }
            }
        }
    ]
}

]}

with open("main.tf.json","w") as file:
    json.dump(cuerpo_terraform_json,file,sort_keys = True,indent = 4)