import numpy as np
import string
import random
from sympy import Matrix, mod_inverse

def TextoANumeros(texto):
    return [string.ascii_uppercase.index(c) for c in texto.upper()]

def NumerosATexto(numeros):
    return ''.join(string.ascii_uppercase[n % 26] for n in numeros)

def RellenarTexto(texto, tamano):
    """Rellena el texto con 'X' hasta que su longitud sea múltiplo del tamaño de la matriz"""
    while len(texto) % tamano != 0:
        texto += 'X'
    return texto

def GenerarMatrizAleatoria(tamano=3):
    """
    Genera una matriz aleatoria invertible módulo 26 para el cifrado Hill
    
    Args:
        tamano (int): Tamaño de la matriz cuadrada (cualquier valor positivo)
        
    Returns:
        list: Matriz representada como lista de listas
    """
    if tamano < 2:
        raise ValueError("El tamaño de la matriz debe ser al menos 2x2")
        
    while True:
        # Generar matriz aleatoria con valores entre 0 y 25
        matriz = np.array([[random.randint(0, 25) for _ in range(tamano)] for _ in range(tamano)])
        
        # Comprobar si es invertible módulo 26
        try:
            matrizSympy = Matrix(matriz)
            determinante = int(matrizSympy.det()) % 26
            # La matriz es invertible si el determinante no es 0 y es coprimo con 26
            if determinante != 0 and np.gcd(determinante, 26) == 1:
                # Devolver como lista de listas para mejor serialización
                return matriz.tolist()
        except:
            continue

def ParsearMatriz(matrizTexto):
    """
    Parsea una matriz desde una representación de texto.
    Formato esperado: 'fila1;fila2;fila3' donde cada fila es una serie de números separados por comas.
    Ejemplo: '1,2,3;4,5,6;7,8,9' para una matriz 3x3
    
    Args:
        matrizTexto (str): Texto que representa la matriz
        
    Returns:
        numpy.ndarray: Matriz convertida a array de numpy
    """
    try:
        # Dividir por filas (separadas por punto y coma)
        filas = matrizTexto.strip().split(';')
        matriz = []
        
        for fila in filas:
            # Dividir cada fila en elementos (separados por comas)
            elementos = [int(x.strip()) for x in fila.split(',')]
            matriz.append(elementos)
            
        return np.array(matriz)
    except Exception as e:
        raise ValueError(f"Formato de matriz inválido: {str(e)}")
def ValidarMatriz(matriz):
    """
    Valida que la matriz sea cuadrada e invertible módulo 26
    
    Args:
        matriz: Puede ser una lista de listas, un array de NumPy o una cadena
               con el formato 'fila1;fila2;...' donde cada fila está separada por punto y coma
               
    Returns:
        numpy.ndarray: Matriz validada
    """
    try:
        # Si la matriz es una cadena, parsearla
        if isinstance(matriz, str):
            matriz = ParsearMatriz(matriz)
        # Si la matriz es una lista, convertirla a array de NumPy
        elif isinstance(matriz, list):
            matriz = np.array(matriz)
        
        # Verificar que la matriz sea cuadrada
        filas, columnas = matriz.shape
        if filas != columnas:
            raise ValueError("La matriz debe ser cuadrada (mismo número de filas y columnas)")
        # Verificar que la matriz sea invertible
        matrizSympy = Matrix(matriz)
        determinante = int(matrizSympy.det()) % 26
        
        if determinante == 0 or np.gcd(determinante, 26) != 1:
            raise ValueError("La matriz no es invertible módulo 26 (determinante no es coprimo con 26)")
        
        return matriz
    except Exception as e:
        raise ValueError(f"Matriz inválida: {str(e)}")

def Cifrar(texto, matriz):
    """
    Cifra un texto usando el cifrado Hill
    
    Args:
        texto (str): Texto a cifrar
        matriz: Puede ser una cadena con el formato 'fila1;fila2;[fila3]',
                una lista de listas o un array de NumPy
                
    Returns:
        str: Texto cifrado
    """
    try:
        matriz = ValidarMatriz(matriz)
        tamano = matriz.shape[0]  # Obtiene el tamaño de la matriz (2 o 3)
        
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
    """
    Descifra un texto usando el cifrado Hill
    
    Args:
        texto (str): Texto a descifrar
        matriz: Puede ser una cadena con el formato 'fila1;fila2;[fila3]',
                una lista de listas o un array de NumPy
                
    Returns:
        str: Texto descifrado
    """
    try:
        matriz = ValidarMatriz(matriz)
        tamano = matriz.shape[0]  # Obtiene el tamaño de la matriz (2 o 3)
        
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
    """
    Convierte una matriz a su representación en string con formato 'fila1;fila2;[fila3]'
    
    Args:
        matriz: Lista de listas o array de NumPy
        
    Returns:
        str: Representación en string de la matriz
    """
    if isinstance(matriz, np.ndarray):
        matriz = matriz.tolist()
        
    return ';'.join([','.join(map(str, fila)) for fila in matriz])
def DescifrarFuerzaBruta(textoCifrado):
    """
    Simula un ataque de fuerza bruta generando algunas posibles soluciones
    
    Args:
        textoCifrado (str): Texto cifrado a descifrar
        
    Returns:
        list: Lista de tuplas (descripción de la matriz, texto descifrado)
    """
    posiblesSoluciones = []
    
    # Genera soluciones con matrices de diferentes tamaños
    for tamano in [2, 3, 4, 5]:
        for i in range(3):  # 3 intentos con cada tamaño
            try:
                matriz = GenerarMatrizAleatoria(tamano)
                textoDescifrado = Descifrar(textoCifrado, matriz)
                matrizStr = MatrizToString(matriz)
                posiblesSoluciones.append((f"Matriz {tamano}x{tamano} #{i+1}: {matrizStr}", textoDescifrado))
            except Exception as e:
                continue
    
    return posiblesSoluciones
