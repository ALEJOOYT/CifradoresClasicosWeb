import itertools
import string
import random

charsetPredeterminado = string.ascii_uppercase + string.digits

# Definir el cuadro ADFGVX estándar
CUADRO_ADFGVX = {
    'AA': 'N', 'AD': 'A', 'AF': '4', 'AG': 'B', 'AV': 'C', 'AX': '5',
    'DA': 'D', 'DD': 'E', 'DF': '6', 'DG': 'F', 'DV': 'G', 'DX': '7',
    'FA': 'H', 'FD': 'I', 'FF': '8', 'FG': 'J', 'FV': 'K', 'FX': '9',
    'GA': 'L', 'GD': 'M', 'GF': '0', 'GG': 'O', 'GV': 'P', 'GX': '1',
    'VA': 'Q', 'VD': 'R', 'VF': '2', 'VG': 'S', 'VV': 'T', 'VX': '3',
    'XA': 'U', 'XD': 'V', 'XF': 'W', 'XG': 'X', 'XV': 'Y', 'XX': 'Z'
}

def GenerarClaveAleatoria(longitud=10):
    """Genera una clave aleatoria para el cifrado"""
    caracteres = string.ascii_uppercase
    return ''.join(random.choice(caracteres) for _ in range(longitud))

def Cifrar(textoPlano, clave):
    if not textoPlano or not clave:
        raise ValueError("El texto y la clave son requeridos")
    
    # Limpiar el texto plano (solo letras y números)
    textoPlano = ''.join(c for c in textoPlano.upper() if c.isalnum())
    if not textoPlano:
        raise ValueError("El texto debe contener al menos un carácter válido")
    
    try:
        # Usar el cuadro fijo
        # Buscar cada carácter del texto en el cuadro y obtener sus coordenadas
        intermedio = ""
        for c in textoPlano:
            found = False
            for k, v in CUADRO_ADFGVX.items():
                if v == c:
                    intermedio += k
                    found = True
                    break
            if not found:
                continue
        
        if not intermedio:
            raise ValueError("No se pudo cifrar el texto con el cuadro proporcionado")
            
        # Distribuir el texto intermedio en columnas según la clave
        columnas = {i: "" for i in range(len(clave))}
        ciclo = itertools.cycle(range(len(clave)))
        for caracter in intermedio:
            columnas[next(ciclo)] += caracter
        
        # Reordenar las columnas según el orden alfabético de la clave
        claveConIndice = [(char, i) for i, char in enumerate(clave)]
        claveOrdenada = sorted(claveConIndice)
        
        return "".join(columnas[i] for _, i in claveOrdenada)
    except Exception as e:
        raise ValueError(f"Error al cifrar: {str(e)}")

def Descifrar(textoCifrado, clave):
    if not textoCifrado or not clave:
        raise ValueError("El texto cifrado y la clave son requeridos")
    
    try:
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
        for i in range(0, len(intermedio), 2):
            if i + 1 < len(intermedio):
                par = intermedio[i:i+2]
                if par in CUADRO_ADFGVX:
                    textoPlano += CUADRO_ADFGVX[par]

        if not textoPlano:
            raise ValueError("No se pudo descifrar el texto con la clave proporcionada")
            
        return textoPlano
    except Exception as e:
        raise ValueError(f"Error al descifrar: {str(e)}")
