# Cifrador PlayFair
# Esta implementación sigue el estándar del proyecto con funciones en camelCase y documentación en español

def generarMatriz(clave):
    """
    Genera la matriz 5x5 para el cifrado PlayFair basada en la clave proporcionada.
    
    Args:
        clave (str): Palabra clave para generar la matriz.
        
    Returns:
        list: Matriz 5x5 para el cifrado PlayFair.
    """
    # Convertir a mayúsculas y eliminar espacios
    clave = clave.upper().replace(" ", "")
    
    # Reemplazar J por I (convención del cifrado PlayFair)
    clave = clave.replace("J", "I")
    
    # Generar matriz 5x5
    matriz = []
    letras_usadas = []
    
    # Primero añadimos las letras de la clave sin repetir
    for letra in clave:
        if letra not in letras_usadas and letra.isalpha():
            letras_usadas.append(letra)
    
    # Luego completamos con el resto del alfabeto (sin J)
    alfabeto = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # Sin J
    for letra in alfabeto:
        if letra not in letras_usadas:
            letras_usadas.append(letra)
    
    # Crear matriz 5x5
    for i in range(0, 25, 5):
        matriz.append(letras_usadas[i:i+5])
    
    return matriz

def encontrarPosicion(matriz, letra):
    """
    Encuentra la posición de una letra en la matriz.
    
    Args:
        matriz (list): Matriz 5x5 del cifrado PlayFair.
        letra (str): Letra a buscar.
        
    Returns:
        tuple: Coordenadas (fila, columna) de la letra en la matriz.
    """
    letra = letra.upper()
    # Reemplazar J por I (convención del cifrado PlayFair)
    if letra == 'J':
        letra = 'I'
    
    for i in range(5):
        for j in range(5):
            if matriz[i][j] == letra:
                return (i, j)
    
    return None

def prepararBigramas(texto):
    """
    Prepara el texto en bigramas (pares de letras) para el cifrado PlayFair.
    
    Args:
        texto (str): Texto a preparar.
        
    Returns:
        list: Lista de bigramas preparados para el cifrado.
    """
    # Convertir a mayúsculas, eliminar espacios y caracteres no alfabéticos
    texto = ''.join(c.upper() for c in texto if c.isalpha())
    
    # Reemplazar J por I (convención del cifrado PlayFair)
    texto = texto.replace("J", "I")
    
    # Crear bigramas
    bigramas = []
    i = 0
    while i < len(texto):
        # Si llegamos al final con un carácter impar, añadir 'X'
        if i == len(texto) - 1:
            bigramas.append(texto[i] + 'X')
            i += 1
        # Si los dos caracteres son iguales, insertar 'X'
        elif texto[i] == texto[i+1]:
            bigramas.append(texto[i] + 'X')
            i += 1
        else:
            bigramas.append(texto[i:i+2])
            i += 2
    
    return bigramas

def cifrar(texto, clave):
    """
    Cifra un texto usando el cifrado PlayFair.
    
    Args:
        texto (str): Texto a cifrar.
        clave (str): Clave para generar la matriz.
        
    Returns:
        str: Texto cifrado.
    """
    try:
        # Validar entrada
        if not texto or not clave:
            return "Error: El texto y la clave son requeridos."
            
        if not any(c.isalpha() for c in clave):
            return "Error: La clave debe contener al menos una letra."
        
        # Generar matriz
        matriz = generarMatriz(clave)
        
        # Preparar bigramas
        bigramas = prepararBigramas(texto)
        
        # Cifrar cada bigrama
        texto_cifrado = ""
        for bigrama in bigramas:
            # Encontrar posiciones
            pos1 = encontrarPosicion(matriz, bigrama[0])
            pos2 = encontrarPosicion(matriz, bigrama[1])
            
            # Si están en la misma fila
            if pos1[0] == pos2[0]:
                texto_cifrado += matriz[pos1[0]][(pos1[1] + 1) % 5]
                texto_cifrado += matriz[pos2[0]][(pos2[1] + 1) % 5]
            # Si están en la misma columna
            elif pos1[1] == pos2[1]:
                texto_cifrado += matriz[(pos1[0] + 1) % 5][pos1[1]]
                texto_cifrado += matriz[(pos2[0] + 1) % 5][pos2[1]]
            # Si forman un rectángulo
            else:
                texto_cifrado += matriz[pos1[0]][pos2[1]]
                texto_cifrado += matriz[pos2[0]][pos1[1]]
        
        return texto_cifrado
    
    except Exception as e:
        return f"Error: {str(e)}"

def descifrar(textoCifrado, clave):
    """
    Descifra un texto cifrado con PlayFair.
    
    Args:
        textoCifrado (str): Texto cifrado.
        clave (str): Clave para generar la matriz.
        
    Returns:
        str: Texto descifrado.
    """
    try:
        # Validar entrada
        if not textoCifrado or not clave:
            return "Error: El texto cifrado y la clave son requeridos."
            
        if not any(c.isalpha() for c in clave):
            return "Error: La clave debe contener al menos una letra."
        
        # Generar matriz
        matriz = generarMatriz(clave)
        
        # Preparar bigramas (el texto cifrado ya debería estar formateado correctamente)
        bigramas = []
        for i in range(0, len(textoCifrado), 2):
            if i + 1 < len(textoCifrado):
                bigramas.append(textoCifrado[i:i+2])
        
        # Descifrar cada bigrama
        texto_descifrado = ""
        for bigrama in bigramas:
            # Encontrar posiciones
            pos1 = encontrarPosicion(matriz, bigrama[0])
            pos2 = encontrarPosicion(matriz, bigrama[1])
            
            # Si están en la misma fila
            if pos1[0] == pos2[0]:
                texto_descifrado += matriz[pos1[0]][(pos1[1] - 1) % 5]
                texto_descifrado += matriz[pos2[0]][(pos2[1] - 1) % 5]
            # Si están en la misma columna
            elif pos1[1] == pos2[1]:
                texto_descifrado += matriz[(pos1[0] - 1) % 5][pos1[1]]
                texto_descifrado += matriz[(pos2[0] - 1) % 5][pos2[1]]
            # Si forman un rectángulo
            else:
                texto_descifrado += matriz[pos1[0]][pos2[1]]
                texto_descifrado += matriz[pos2[0]][pos1[1]]
        
        return texto_descifrado
    
    except Exception as e:
        return f"Error: {str(e)}"

def fuerzaBruta(textoCifrado, palabrasClave=None):
    """
    Descifra un texto cifrado con PlayFair mediante fuerza bruta.
    
    Args:
        textoCifrado (str): Texto cifrado a descifrar.
        palabrasClave (list, optional): Lista de posibles claves. 
            Si no se proporciona, se usará un conjunto de palabras comunes.
        
    Returns:
        list: Lista de posibles descifrados con sus claves correspondientes.
    """
    try:
        # Validar entrada
        if not textoCifrado:
            return []
        
        # Lista predeterminada de palabras clave comunes si no se proporciona
        if palabrasClave is None:
            palabrasClave = [
                "CLAVE", "PASSWORD", "CRYPTOGRAPHY", "SECURITY", "CIPHER",
                "SECRET", "CONFIDENTIAL", "CLASSIFIED", "PRIVATE", "SECURE",
                "ENCRYPTION", "DECRYPTION", "ALGORITHM", "KEY", "CODE",
                "PLAYFAIR", "MATRIX", "KEYWORD", "PUZZLE", "ENIGMA"
            ]
        
        # Almacenar resultados
        resultados = []
        
        # Probar cada palabra clave
        for clave in palabrasClave:
            textoDescifrado = descifrar(textoCifrado, clave)
            
            # Solo agregar resultados exitosos (que no contienen errores)
            if not textoDescifrado.startswith("Error"):
                resultados.append({
                    "clave": clave,
                    "textoDescifrado": textoDescifrado
                })
        
        return resultados
    
    except Exception as e:
        return []

