from flask import Flask
import os
import sys

PUERTO = int(os.environ.get("PORT","8081"))     #os.environ.get(clave,valor)
MENSAJE = os.environ.get("MENSAJE","Hola CC3S2 x2 ")
LANZAMIENTO = os.environ.get("LANZAMIENTO","v1.1" )

app =Flask(__name__)

@app.route("/") #localhost la raiz
def root():
    print(f" mensaje={MENSAJE},lanzamiento={LANZAMIENTO}",file=sys.stdout,flush=True)
    return {
        "estado":"ok",
        "mensaje":MENSAJE,
        "lanzamiento":LANZAMIENTO,
        "puerto":PUERTO
    }
if __name__=="__main__":
    app.run(host="0.0.0.0",port=PUERTO) 