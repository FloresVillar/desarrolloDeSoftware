# Implementa la función summarize y el CLI.
# Requisitos:
# - summarize(nums) -> dict con claves: count, sum, avg
# - Valida que nums sea lista no vacía y elementos numéricos (acepta strings convertibles a float).
# - CLI: python -m app "1,2,3" imprime: sum=6.0 avg=2.0 count=3

def summarize(nums):  # TODO: tipado opcional 
    if not nums:
        raise ValueError("vacio")
    numeros = []
    for e in nums:
        try:
            f = float(e)
            numeros.append(f)
        except ValueError:
            raise ValueError("no es numerico")
    total = sum(numeros); cuenta = len(numeros) ; promedio = total/cuenta
    return {"count":cuenta,"sum":total,"avg":promedio} 

if __name__ == "__main__":
    import sys
    raw = sys.argv[1] if len(sys.argv) > 1 else ""
    items = []
    for p in raw.split(","): 
        if p.strip():
            items.append(p.strip())
    # TODO: validar items y llamar summarize, luego imprimir el formato solicitado
    print("TODO: implementar CLI (python -m app \"1,2,3\")")
    try:
        resultado = summarize(items)
        print(f"sum = {resultado['sum']} avg ={resultado['avg']} count={resultado['count']}")
    except ValueError:
        raise ValueError("no validado")
        sys.exit(1)

# sintaxis try except ![try except] (https://docs.python.org/3/tutorial/errors.html)