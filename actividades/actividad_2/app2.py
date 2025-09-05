from flask import Flask
import os
import sys

PUERT = int(os.environ.get("PUERTO","8081"))     #os.environ.get(clave,valor)
MENS = os.environ.get("MENSAJE","Hola CC3S2 x2 ")
LANZ = os.environ.get("LANZAMIENTO","v1.1" )

app =Flask(__name__)

@app.route("/") #localhost la raiz
def root():
    print(f" mensaje={MENS},lanzamiento={LANZ}",file=sys.stdout,flush=True)
    return {
        "estado":"ok",
        "mensaje":MENS,
        "lanzamiento":LANZ,
        "puerto":PUERT
    }
if __name__=="__main__":
    app.run(host="0.0.0.0",port=PUERT) 