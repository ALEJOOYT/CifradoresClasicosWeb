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
    """
    Realiza un ataque por fuerza bruta al cifrado Afín probando todas las combinaciones
    posibles de claves (a,b) donde 'a' debe ser coprimo con 26 (el tamaño del alfabeto).
    
    Args:
        palabraCifrada (str): El texto cifrado a descifrar
        
    Returns:
        list: Una lista de diccionarios con posibles resultados, cada uno contiene:
              - 'a': El valor de 'a' utilizado
              - 'b': El valor de 'b' utilizado
              - 'textoDescifrado': El texto descifrado con esa clave
              - 'clave': Representación de la clave como (a,b)
    """
    posiblesResultados = []
    
    # Valores válidos de 'a' son aquellos que son coprimos con 26
    # En el cifrado Afín, estos son: 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25
    valores_a_validos = [a for a in range(1, TAMAÑO_ALFABETO) if SonCoprimos(a, TAMAÑO_ALFABETO)]
    
    # Probamos cada combinación válida
    for a in valores_a_validos:
        for b in range(TAMAÑO_ALFABETO):
            try:
                posibleTextoOriginal = Descifrar(palabraCifrada, a, b)
                
                # Solo agregamos resultados válidos (que no sean mensajes de error)
                if not posibleTextoOriginal.startswith("Error:"):
                    posiblesResultados.append({
                        "a": a,
                        "b": b,
                        "textoDescifrado": posibleTextoOriginal,
                        "clave": f"({a},{b})"
                    })
            except Exception as e:
                # Ignoramos cualquier error y continuamos con la siguiente combinación
                continue
    
    return posiblesResultados

