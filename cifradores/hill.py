import numpy as np
import string
from sympy import Matrix, mod_inverse

def TextoANumeros(texto):
    alfabeto = string.ascii_uppercase
    return [alfabeto.index(caracter) for caracter in texto.upper() if caracter in alfabeto]

def NumerosATexto(numeros):
    alfabeto = string.ascii_uppercase
    return ''.join(alfabeto[num % 26] for num in numeros)

def RellenarTexto(texto, tamano):
    while len(texto) % tamano != 0:
        texto += 'X'
    return texto

def Cifrar(texto, clave):
    tamano = len(clave)
    texto = RellenarTexto(texto, tamano)
    numeros = TextoANumeros(texto)
    numerosCifrados = []
    for i in range(0, len(numeros), tamano):
        bloque = np.array(numeros[i:i+tamano]).reshape(-1, 1)
        bloqueCifrado = np.dot(clave, bloque) % 26
        numerosCifrados.extend(bloqueCifrado.flatten())

    return NumerosATexto(numerosCifrados)

def Descifrar(texto, clave):
    tamano = len(clave)
    numeros = TextoANumeros(texto)
    numerosDescifrados = []
    matrizSympy = Matrix(clave)
    determinante = int(matrizSympy.det()) % 26
    determinanteInv = mod_inverse(determinante, 26)
    claveInv = (determinanteInv * matrizSympy.adjugate()) % 26
    claveInv = np.array(claveInv).astype(int)
    for i in range(0, len(numeros), tamano):
        bloque = np.array(numeros[i:i+tamano]).reshape(-1, 1)
        bloqueDescifrado = np.dot(claveInv, bloque) % 26
        numerosDescifrados.extend(bloqueDescifrado.flatten())
    textoDescifrado = NumerosATexto(numerosDescifrados)
    return textoDescifrado.rstrip('X')

def DescifrarFuerzaBruta(textoCifrado, textoOriginal, clave):
    textoDescifrado = Descifrar(textoCifrado, clave)
    print(f"Texto descifrado: {textoDescifrado}")
    if textoDescifrado == textoOriginal:
        print(f"Clave encontrada: \n{clave}")
        return textoDescifrado
    else:
        print("No se encontró una clave válida.")
        return "No se encontró una clave válida."