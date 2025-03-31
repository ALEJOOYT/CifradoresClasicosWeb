import itertools
import random
import string

charsetPredeterminado = string.ascii_uppercase + string.digits

def GenerarCuadro(matriz):
    adfgvx = "ADFGVX"
    cuadro = {}
    indice = 0
    for i in adfgvx:
        for j in adfgvx:
            cuadro[i + j] = matriz[indice]
            indice += 1
    return cuadro

def Cifrar(textoPlano, cuadro, clave):
    intermedio = "".join([k for c in textoPlano.upper() for k, v in cuadro.items() if v == c])
    columnas = {i: "" for i in range(len(clave))}
    ciclo = itertools.cycle(range(len(clave)))
    for caracter in intermedio:
        columnas[next(ciclo)] += caracter
    claveConIndice = [(char, i) for i, char in enumerate(clave)]
    claveOrdenada = sorted(claveConIndice)
    return "".join(columnas[i] for _, i in claveOrdenada)

def Descifrar(textoCifrado, cuadro, clave):
    longitudClave = len(clave)
    longitudTexto = len(textoCifrado)
    base = longitudTexto // longitudClave
    extra = longitudTexto % longitudClave

    longitudesColumnas = {i: base + (1 if i < extra else 0) for i in range(longitudClave)}

    claveConIndice = [(char, i) for i, char in enumerate(clave)]
    claveOrdenada = sorted(claveConIndice)
    columnas = {}
    posicion = 0
    for _, indice in claveOrdenada:
        longitud = longitudesColumnas[indice]
        columnas[indice] = textoCifrado[posicion:posicion + longitud]
        posicion += longitud

    intermedio = ""
    maxLongitud = max(longitudesColumnas.values())
    for i in range(maxLongitud):
        for j in range(longitudClave):
            if i < longitudesColumnas[j] and i < len(columnas[j]):
                intermedio += columnas[j][i]

    textoPlano = ""
    for i in range(0, len(intermedio) - 1, 2):
        par = intermedio[i:i+2]
        if par in cuadro:
            textoPlano += cuadro[par]

    return textoPlano

def GenerarClaveAleatoria() -> str:
    # Crear una lista de todos los caracteres posibles
    todosLosCaracteres = list(charsetPredeterminado)

    # Asegurarse de que hay al menos 36 caracteres disponibles
    if len(todosLosCaracteres) < 36:
        raise ValueError("No hay suficientes caracteres para generar una clave Polybius de 36 caracteres")

    # Mezclar los caracteres aleatoriamente
    random.shuffle(todosLosCaracteres)

    # Tomar los primeros 36 caracteres
    clavePolybius = ''.join(todosLosCaracteres[:36])

    return clavePolybius