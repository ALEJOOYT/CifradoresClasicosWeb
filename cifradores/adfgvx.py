import itertools
import random
import string

COORDENADAS_ADFGVX = "ADFGVX"

caracteresPermitidos = string.ascii_uppercase + string.digits

def GenerarCuadroAdfgvx(matriz):
    cuadro = {}
    indice = 0
    for i in COORDENADAS_ADFGVX:
        for j in COORDENADAS_ADFGVX:
            cuadro[i + j] = matriz[indice]
            indice += 1
    return cuadro

def ValidarMatrizAdfgvx(cuadro):
    # Validate that the matrix has all 36 characters
    if len(cuadro) != 36:
        raise ValueError("La matriz ADFGVX debe contener exactamente 36 caracteres")
    
    # Validate all coordinates are valid ADFGVX combinations
    coordenadas_validas = set(i + j for i in COORDENADAS_ADFGVX for j in COORDENADAS_ADFGVX)
    if set(cuadro.keys()) != coordenadas_validas:
        raise ValueError("La matriz ADFGVX contiene coordenadas inválidas")

def CifrarAdfgvx(textoPlano, cuadro, clave):
    # Validate inputs
    if not textoPlano:
        raise ValueError("El texto a cifrar no puede estar vacío")
    if not clave:
        raise ValueError("La clave de transposición no puede estar vacía")
    
    # Validate matrix
    ValidarMatrizAdfgvx(cuadro)
    
    # Validate all characters in input text are in the matrix
    valores_permitidos = set(cuadro.values())
    caracteres_invalidos = set(textoPlano.upper()) - valores_permitidos
    if caracteres_invalidos:
        raise ValueError(f"El texto contiene caracteres no permitidos: {', '.join(sorted(caracteres_invalidos))}")
    
    # Continue with existing encryption logic
    intermedio = "".join([k for c in textoPlano.upper() for k, v in cuadro.items() if v == c])
    columnas = {i: "" for i in range(len(clave))}
    ciclo = itertools.cycle(range(len(clave)))
    for caracter in intermedio:
        columnas[next(ciclo)] += caracter
    claveConIndice = [(char, i) for i, char in enumerate(clave)]
    claveOrdenada = sorted(claveConIndice)
    return "".join(columnas[i] for _, i in claveOrdenada)

def DescifrarAdfgvx(textoCifrado, cuadro, clave):
    # Validate inputs
    if not textoCifrado:
        raise ValueError("El texto cifrado no puede estar vacío")
    if not clave:
        raise ValueError("La clave de transposición no puede estar vacía")
        
    # Validate matrix
    ValidarMatrizAdfgvx(cuadro)
    
    # Validate text contains only valid ADFGVX characters
    caracteres_validos = set(COORDENADAS_ADFGVX)
    caracteres_invalidos = set(textoCifrado.upper()) - caracteres_validos
    if caracteres_invalidos:
        raise ValueError(f"El texto cifrado contiene caracteres inválidos: {', '.join(sorted(caracteres_invalidos))}")
    
    # Validate text length is even (should be pairs of coordinates)
    if len(textoCifrado) % 2 != 0:
        raise ValueError("El texto cifrado debe tener una longitud par")
    
    # Continue with existing decryption logic
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
        else:
            raise ValueError(f"Par de coordenadas inválido encontrado: {par}")

    return textoPlano

def GenerarMatrizAleatoria() -> dict:
    # Generate a cuadro (dictionary) with ADFGVX coordinates and random unique characters
    caracteres_disponibles = list(string.ascii_uppercase + string.digits)  # A-Z and 0-9
    
    if len(caracteres_disponibles) < 36:
        raise ValueError("No hay suficientes caracteres para generar una matriz ADFGVX")
    
    # Obtener 36 caracteres únicos aleatorios
    caracteres_seleccionados = random.sample(caracteres_disponibles, 36)
    
    # Crear el cuadro ADFGVX
    cuadro = {}
    indice = 0
    for i in COORDENADAS_ADFGVX:
        for j in COORDENADAS_ADFGVX:
            cuadro[i + j] = caracteres_seleccionados[indice]
            indice += 1
    
    # Validar el cuadro generado
    ValidarMatrizAdfgvx(cuadro)
    
    return cuadro
