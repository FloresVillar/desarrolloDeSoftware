import os, json, click
from jsonschema import validate,ValidationError

MODULE_DIR = "modules/simulated_app"
OUT_DIR    = "environments"

def render_and_write(env):
    """Crea un entorno con su main.tf.json y copia de red."""
    env_dir = os.path.join(OUT_DIR, env["name"])
    os.makedirs(env_dir, exist_ok=True)

    # Contenido mínimo del main.tf.json
    config_recurso = {
        "resource": [
            {
                "null_resource": [
                    {
                        env["name"]: [
                            {
                                "triggers": {
                                    "name": env["name"],
                                    "network": env["network"]
                                },
                                "provisioner": [
                                    {
                                        "local-exec": {
                                            "command": f"echo 'Servidor {env['name']} en red {env['network']}'"
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
    #with open(os.path.join(env_dir, "main.tf.json"), "w") as fp:
    #json.dump(config, fp, indent=4) 
@click.option("--count",  default=3,  help="Número de entornos a generar")
@click.option("--prefix", default="env", help="Prefijo de los entornos")
def main(count, prefix):
    """Genera varios entornos Terraform simples."""
    if os.path.isdir(OUT_DIR):
        import shutil
        shutil.rmtree(OUT_DIR)
    envs = [{"name": f"{prefix}{i}", "network": f"net{i}"} for i in range(1, count + 1)]
    for env in envs:
        render_and_write(env)
    click.echo(f"Generados {count} entornos en '{OUT_DIR}/' con prefijo '{prefix}'")
    
if __name__ == "__main__":
    main()
