import os

def TextoANumeros(texto: str) -> list:
    """Convierte el texto en su representación numérica basada en ASCII."""
    return [ord(caracter) for caracter in texto]

def NumerosATexto(numeros: list) -> str:
    """Convierte una lista de números ASCII a texto.
    
    Para uso en el cifrado Vernam, esta función representa caracteres no imprimibles
    en formato hexadecimal para asegurar una salida limpia.
    """
    return ''.join(chr(numero) if 32 <= numero <= 126 else f'\\x{numero:02x}' for numero in numeros)

def Cifrar(textoPlano: str) -> tuple:
    """Cifra un mensaje con el cifrado Vernam (One-Time Pad).
    
    Returns:
        tuple: (textoCifrado, claveTexto) - El mensaje cifrado y la clave generada
    """
    numerosTextoPlano = TextoANumeros(textoPlano)
    clave = [os.urandom(1)[0] for _ in numerosTextoPlano]
    numerosTextoCifrado = [p ^ k for p, k in zip(numerosTextoPlano, clave)]
    
    # Codificar directamente el resultado sin información de depuración
    textoCifrado = NumerosATexto(numerosTextoCifrado)
    claveTexto = NumerosATexto(clave)
    
    return textoCifrado, claveTexto

def Descifrar(textoCifrado: str, clave: str) -> str:
    """Descifra un mensaje cifrado con el cifrado Vernam.
    
    Args:
        textoCifrado (str): El mensaje cifrado
        clave (str): La clave utilizada para cifrar
        
    Returns:
        str: El mensaje descifrado
    """
    # Manejo de posibles códigos hexadecimales en la entrada
    if '\\x' in textoCifrado:
        # Procesar textoCifrado si contiene caracteres hexadecimales
        textoCifrado = textoCifrado.encode().decode('unicode_escape')
    
    if '\\x' in clave:
        # Procesar clave si contiene caracteres hexadecimales
        clave = clave.encode().decode('unicode_escape')
    
    numerosTextoCifrado = TextoANumeros(textoCifrado)
    numerosClave = TextoANumeros(clave)
    numerosTextoDescifrado = [c ^ k for c, k in zip(numerosTextoCifrado, numerosClave)]
    
    # Devolver el resultado directamente sin información de depuración
    return NumerosATexto(numerosTextoDescifrado)
