from flask import request,Flask,jsonify,make_response
import os
import sys
import hashlib,json

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

class Recurso:
    def __init__(self,a,b):
        self.x = a;self.y = b
    def get_variables(self):
        return {"x":self.x,"y":self.y}

ETAG = {} #no es necesario , el cliente lo guarda

@app.route("/recurso")
def recurso():
    r = Recurso(1,2).get_variables()
    cuerpo = json.dumps(r)
    etag_recurso = hashlib.md5(cuerpo.encode()).hexdigest()
    etag_cliente = request.headers.get("If-None-Match") 
    if etag_cliente == etag_recurso:
        respuesta = make_response("",304)
        respuesta.headers["Etag"] = etag_recurso
        return respuesta
    else:
        respuesta = make_response(cuerpo,"200")
        respuesta.headers["Content-Type"] = "application/json"
        respuesta.headers["Etag"] = etag_recurso
        respuesta.headers["Cache-Control"] = "no-cache"
        return respuesta

@app.route("/api/ping")
def ping():
    return jsonify({
        "mensaje" : "saludo desde ping",
        "x_request_id" : request.headers.get("X-Request-ID"),
        "traceparent" : request.headers.get("traceparent")
    }) 

@app.route("/items/123")
def items():
    return jsonify({"campo":"123"})

ordenes_cache = {}

@app.route("/ordenes",methods=["POST"])
def orden():
    idem_llave = request.headers.get("Idempotency-Key")
    cuerpo = request.get_json(force=True)
    if not idem_llave:
        return jsonify({"error":"no hay Idempotency-Key"}),400
    if idem_llave in ordenes_cache:
        respuesta_anterior = ordenes_cache[idem_llave]
        return jsonify(respuesta_anterior),200
    orden = {
        "id":hashlib.md5(idem_llave.encode()).hexdigest()[:8],
        "sku":cuerpo.get("sku"),
        "qty":cuerpo.get("qty"),
        "status":"creado"
    }
    ordenes_cache[idem_llave] = orden
    return jsonify(orden),201

@route("/saludz")
def salud_z():
    return jsonify({"salud":"z"})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=PUERT) 