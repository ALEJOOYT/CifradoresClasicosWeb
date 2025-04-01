import numpy as np
import string
import random
from sympy import Matrix, mod_inverse

def TextoANumeros(texto):
    return [string.ascii_uppercase.index(c) for c in texto.upper()]

def NumerosATexto(numeros):
    return ''.join(string.ascii_uppercase[n % 26] for n in numeros)

def RellenarTexto(texto, tamano):
    while len(texto) % tamano != 0:
        texto += 'X'
    return texto

def GenerarMatrizAleatoria(tamano=3):
    if tamano not in [2, 3]:
        raise ValueError("El tamaño de la matriz solo puede ser 2x2 o 3x3")
    while True:
        matriz = np.array([[random.randint(0, 25) for _ in range(tamano)] for _ in range(tamano)])
        try:
            matrizSympy = Matrix(matriz)
            determinante = int(matrizSympy.det()) % 26
            if determinante != 0 and np.gcd(determinante, 26) == 1:
                return matriz.tolist()
        except:
            continue

def ParsearMatriz(matrizTexto):
    try:
        filas = matrizTexto.strip().split(';')
        matriz = []
        for fila in filas:
            elementos = [int(x.strip()) for x in fila.split(',')]
            matriz.append(elementos)
        return np.array(matriz)
    except Exception as e:
        raise ValueError(f"Formato de matriz inválido: {str(e)}")

def FormatearMatrizBonita(matriz):
    if isinstance(matriz, list):
        matriz = np.array(matriz)
    filas, columnas = matriz.shape
    resultado = "┌" + "─" * (columnas * 4 - 1) + "┐\n"
    for i, fila in enumerate(matriz):
        resultado += "│ " + " ".join(f"{x:2d}" for x in fila) + " │\n"
    resultado += "└" + "─" * (columnas * 4 - 1) + "┘"
    return resultado

def ValidarMatriz(matriz):
    try:
        if isinstance(matriz, str):
            matriz = ParsearMatriz(matriz)
        elif isinstance(matriz, list):
            matriz = np.array(matriz)
        filas, columnas = matriz.shape
        if filas != columnas:
            raise ValueError("La matriz debe ser cuadrada (mismo número de filas y columnas)")
        if filas not in [2, 3]:
            raise ValueError("Solo se permiten matrices de 2x2 o 3x3")
        matrizSympy = Matrix(matriz)
        determinante = int(matrizSympy.det()) % 26
        if determinante == 0 or np.gcd(determinante, 26) != 1:
            raise ValueError("La matriz no es invertible módulo 26 (determinante no es coprimo con 26)")
        return matriz
    except Exception as e:
        raise ValueError(f"Matriz inválida: {str(e)}")

def Cifrar(texto, matriz):
    try:
        matriz = ValidarMatriz(matriz)
        tamano = matriz.shape[0]
        texto = RellenarTexto(texto.upper(), tamano)
        numeros = TextoANumeros(texto)
        numerosCifrados = []
        for i in range(0, len(numeros), tamano):
            bloque = np.array(numeros[i:i+tamano])
            resultado = np.dot(matriz, bloque) % 26
            numerosCifrados.extend(resultado)
        return NumerosATexto(numerosCifrados)
    except Exception as e:
        raise ValueError(f"Error al cifrar: {str(e)}")

def Descifrar(texto, matriz):
    try:
        matriz = ValidarMatriz(matriz)
        tamano = matriz.shape[0]
        numeros = TextoANumeros(texto.upper())
        numerosDescifrados = []
        matrizSympy = Matrix(matriz)
        matrizInversa = matrizSympy.inv_mod(26)
        matrizInversa = np.array(matrizInversa.tolist(), dtype=int)
        for i in range(0, len(numeros), tamano):
            bloque = np.array(numeros[i:i+tamano])
            resultado = np.dot(matrizInversa, bloque) % 26
            numerosDescifrados.extend(resultado)
        textoDescifrado = NumerosATexto(numerosDescifrados)
        return textoDescifrado.rstrip('X')
    except Exception as e:
        raise ValueError(f"Error al descifrar: {str(e)}")

def MatrizToString(matriz):
    if isinstance(matriz, np.ndarray):
        matriz = matriz.tolist()
    return ';'.join([','.join(map(str, fila)) for fila in matriz])
def DescifrarFuerzaBruta(textoCifrado):
    posiblesSoluciones = []
    for tamano in [2, 3]:
        for i in range(3):
            try:
                matriz = GenerarMatrizAleatoria(tamano)
                textoDescifrado = Descifrar(textoCifrado, matriz)
                matrizStr = MatrizToString(matriz)
                matrizFormateada = FormatearMatrizBonita(matriz)
                posiblesSoluciones.append((
                    f"Matriz {tamano}x{tamano} #{i+1}:\n{matrizFormateada}",
                    textoDescifrado
                ))
            except Exception as e:
                continue
    return posiblesSoluciones
