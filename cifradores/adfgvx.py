import random
import string
import re
from typing import List, Tuple, Dict

# Constantes para el cifrado ADFGVX
ADFGVX = ['A', 'D', 'F', 'G', 'V', 'X']
DEFAULT_CHARSET = string.ascii_lowercase + string.digits  # a-z, 0-9

def generate_random_polybius_key() -> str:
    """
    Genera una disposición aleatoria de 36 caracteres únicos para el cuadro de Polybius.
    Utiliza letras minúsculas (a-z) y dígitos (0-9).
    
    Returns:
        str: Cadena de 36 caracteres únicos aleatorios.
    """
    # Crear una lista de todos los caracteres posibles
    all_chars = list(DEFAULT_CHARSET)
    
    # Asegurarse de que hay al menos 36 caracteres disponibles
    if len(all_chars) < 36:
        raise ValueError("No hay suficientes caracteres para generar una clave Polybius de 36 caracteres")
    
    # Mezclar los caracteres aleatoriamente
    random.shuffle(all_chars)
    
    # Tomar los primeros 36 caracteres
    polybius_key = ''.join(all_chars[:36])
    
    return polybius_key

def create_polybius_square(key: str) -> Dict[str, str]:
    """
    Crea un cuadro de Polybius 6x6 usando la clave proporcionada.
    
    Args:
        key (str): Cadena de 36 caracteres únicos para llenar el cuadro.
        
    Returns:
        Dict[str, str]: Diccionario que mapea cada carácter a su coordenada ADFGVX.
    """
    # Validar que la clave tenga exactamente 36 caracteres únicos
    if len(key) != 36 or len(set(key)) != 36:
        raise ValueError("La clave debe tener exactamente 36 caracteres únicos")
    
    polybius = {}
    index = 0
    
    # Crear el cuadro de Polybius
    for i in range(6):
        for j in range(6):
            char = key[index]
            polybius[char] = ADFGVX[i] + ADFGVX[j]
            index += 1
    
    return polybius

def create_inverse_polybius(polybius: Dict[str, str]) -> Dict[str, str]:
    """
    Crea un cuadro de Polybius inverso para el descifrado.
    
    Args:
        polybius (Dict[str, str]): Cuadro de Polybius original.
        
    Returns:
        Dict[str, str]: Diccionario que mapea cada coordenada ADFGVX a su carácter.
    """
    return {v: k for k, v in polybius.items()}

def encrypt_with_polybius(text: str, polybius: Dict[str, str]) -> str:
    """
    Encripta el texto usando el cuadro de Polybius.
    
    Args:
        text (str): Texto a encriptar.
        polybius (Dict[str, str]): Cuadro de Polybius.
        
    Returns:
        str: Texto intermedio encriptado.
    """
    encrypted = ""
    
    # Convertir texto a minúsculas y eliminar caracteres no mapeados
    text = text.lower()
    
    for char in text:
        if char in polybius:
            encrypted += polybius[char]
        elif char == ' ':
            continue  # Ignorar espacios
    
    return encrypted

def apply_columnar_transposition(text: str, key: str) -> str:
    """
    Aplica transposición columnar al texto usando la clave dada.
    
    Args:
        text (str): Texto a transponer.
        key (str): Clave de transposición.
        
    Returns:
        str: Texto transpuesto.
    """
    # Validar que la clave tenga caracteres únicos
    if len(key) != len(set(key)):
        raise ValueError("La clave de transposición debe tener caracteres únicos")
    
    # Calcular número de filas necesarias
    cols = len(key)
    rows = -(-len(text) // cols)  # Redondeo hacia arriba
    
    # Crear matriz y llenar con el texto
    matrix = [[''] * cols for _ in range(rows)]
    index = 0
    
    for i in range(rows):
        for j in range(cols):
            if index < len(text):
                matrix[i][j] = text[index]
                index += 1
    
    # Obtener el orden de las columnas basado en la clave
    key_order = sorted(range(len(key)), key=lambda k: key[k])
    
    # Leer las columnas en el orden de la clave
    transposed = ""
    for j in key_order:
        for i in range(rows):
            if matrix[i][j]:
                transposed += matrix[i][j]
    
    return transposed

def reverse_columnar_transposition(text: str, key: str) -> str:
    """
    Invierte la transposición columnar usando la clave dada.
    
    Args:
        text (str): Texto transpuesto.
        key (str): Clave de transposición.
        
    Returns:
        str: Texto original antes de la transposición.
    """
    # Validar que la clave tenga caracteres únicos
    if len(key) != len(set(key)):
        raise ValueError("La clave de transposición debe tener caracteres únicos")
    
    # Calcular dimensiones de la matriz
    cols = len(key)
    rows = -(-len(text) // cols)  # Redondeo hacia arriba
    
    # Calcular longitud de cada columna
    col_lengths = [rows] * cols
    remaining = rows * cols - len(text)
    
    # Ajustar longitudes para la última fila incompleta
    key_order = sorted(range(len(key)), key=lambda k: key[k])
    for i in range(remaining):
        col_lengths[key_order[cols - 1 - i]] -= 1
    
    # Crear matriz vacía
    matrix = [[''] * cols for _ in range(rows)]
    
    # Llenar la matriz con el texto, siguiendo el orden de la clave
    index = 0
    for j in key_order:
        for i in range(col_lengths[j]):
            matrix[i][j] = text[index]
            index += 1
    
    # Leer la matriz por filas
    original = ""
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j]:
                original += matrix[i][j]
    
    return original

def cifrar(texto: str, matriz: str, clave: str) -> str:
    """
    Cifra un texto usando el cifrado ADFGVX.
    
    Args:
        texto (str): Texto a cifrar.
        matriz (str): Matriz de 36 caracteres para el cuadro de Polybius.
        clave (str): Clave de transposición.
        
    Returns:
        str: Texto cifrado.
    """
    try:
        # Crear cuadro de Polybius
        polybius = create_polybius_square(matriz)
        
        # Paso 1: Sustituir caracteres con el cuadro Polybius
        intermediate = encrypt_with_polybius(texto, polybius)
        
        # Paso 2: Aplicar transposición columnar
        cifrado = apply_columnar_transposition(intermediate, clave)
        
        return cifrado
    
    except ValueError as e:
        return f"Error: {str(e)}"

def descifrar(texto: str, matriz: str, clave: str) -> str:
    """
    Descifra un texto cifrado con ADFGVX.
    
    Args:
        texto (str): Texto cifrado.
        matriz (str): Matriz de 36 caracteres para el cuadro de Polybius.
        clave (str): Clave de transposición.
        
    Returns:
        str: Texto descifrado.
    """
    try:
        # Validar que el texto cifrado solo contenga letras ADFGVX
        if not all(c in ADFGVX for c in texto):
            return "Error: El texto cifrado debe contener solo letras A, D, F, G, V, X"
        
        # Crear cuadro de Polybius
        polybius = create_polybius_square(matriz)
        inverse_polybius = create_inverse_polybius(polybius)
        
        # Paso 1: Invertir la transposición columnar
        intermediate = reverse_columnar_transposition(texto, clave)
        
        # Paso 2: Decodificar usando el cuadro Polybius invertido
        descifrado = ""
        for i in range(0, len(intermediate), 2):
            if i + 1 < len(intermediate):
                pair = intermediate[i:i+2]
                if pair in inverse_polybius:
                    descifrado += inverse_polybius[pair]
        
        return descifrado
    
    except ValueError as e:
        return f"Error: {str(e)}"

