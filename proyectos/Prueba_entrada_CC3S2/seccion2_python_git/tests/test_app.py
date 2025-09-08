import pytest
#from app.app import summarize
#se define los datos reutilizables , luego los test unitarios propiamente
#siguiendo el patron Arrange-Act-Assert (arrancar - actuar - afirmar) 

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

@pytest.fixture
def datos_reutilizables(): #arrancamos
    return ["1", "2", "3"]

def normal(sample):
    # Arrange–Act–Assert
    # Act    
    #with pytest.raises(NotImplementedError):
    #    summarize(sample)
    resultado = summarize(datos_reutilizables) #actuamos
    assert resultado["sum"] == 6   #afirmamos
    assert resultado["count"] == 3
    assert resultado["avg"] == 2

def borde():
    with pytest.raises(Exception):
        summarize([])

def error():
    with pytest.raises(Exception):
        summarize(["a", "2"])

# documentacion ![pytest](https://docs.pytest.org/en/7.1.x/how-to/assert.html#asserting-with-the-assert-statement)
#para guardar en coverage.txt revisando la documentacion , un tanto rebuscasda,se usa pytest-cov
#que intutitivamente es para cov cobertura , ``pytest --cov=app --cov-report=term-missing | tee coverage.txt ``
# como se ve se mide a app, y se busca a los archivos que empiecen por test_*.py, y se ejcutan las funciones normal, borde  y error