import json 
import os
import sys

ruta_api_key = os.path.expanduser("~/.config/secure.json")

if not os.path.exists(ruta_api_key):
    sys.exit("no existe la ruta")
data = None
with os.open(ruta_api_key,"r") as f:
    data= f.load()
api_key = data.get("api-key")
if not api_key:
    sys.exit("clave no encontrada")
