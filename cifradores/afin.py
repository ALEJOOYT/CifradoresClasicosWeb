import math

# Constantes del cifrado Afín
alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
TAMAÑO_ALFABETO = len(alfabeto)

# Función para calcular el inverso multiplicativo módulo m
def CalcularInversoMultiplicativo(a, m):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return 1

# Función para verificar si dos números son coprimos
def SonCoprimos(a, b):
    return math.gcd(a, b) == 1

# Función para Cifrar un mensaje usando el cifrado Afín
def Cifrar(palabra, a, b):
    if not SonCoprimos(a, TAMAÑO_ALFABETO):
        return "Error: El valor de 'a' debe ser coprimo con el tamaño del alfabeto."

    resultado = ""
    for letra in palabra.upper():
        if letra in alfabeto:
            indice = alfabeto.index(letra)
            nuevoIndice = (a * indice + b) % TAMAÑO_ALFABETO
            resultado += alfabeto[nuevoIndice]
        else:
            resultado += letra

    return resultado

# Función para Descifrar un mensaje cifrado con el cifrado Afín
def Descifrar(palabraCifrada, a, b):
    if not SonCoprimos(a, TAMAÑO_ALFABETO):
        return "Error: El valor de 'a' debe ser coprimo con el tamaño del alfabeto."

    aInverso = CalcularInversoMultiplicativo(a, TAMAÑO_ALFABETO)
    resultado = ""

    for letra in palabraCifrada.upper():
        if letra in alfabeto:
            indice = alfabeto.index(letra)
            nuevoIndice = (aInverso * (indice - b)) % TAMAÑO_ALFABETO
            resultado += alfabeto[nuevoIndice]
        else:
            resultado += letra

    return resultado

# Función para Descifrar usando fuerza bruta
def DescifrarFuerzaBruta(palabraCifrada):
    posiblesResultados = []

    for a in range(1, TAMAÑO_ALFABETO):
        if SonCoprimos(a, TAMAÑO_ALFABETO):
            for b in range(TAMAÑO_ALFABETO):
                posibleTextoOriginal = Descifrar(palabraCifrada, a, b)
                posiblesResultados.append({
                    "a": a,
                    "b": b,
                    "textoDescifrado": posibleTextoOriginal
                })

    return posiblesResultados

