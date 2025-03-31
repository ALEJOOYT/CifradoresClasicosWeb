import os

def TextoANumeros(texto: str) -> list:
    """Convierte el texto en su representación numérica basada en ASCII."""
    return [ord(caracter) for caracter in texto]

def NumerosATexto(numeros: list) -> str:
    """Convierte una lista de números ASCII a texto."""
    return ''.join(chr(numero) for numero in numeros)

def CifrarVernam(textoPlano: str) -> tuple:
    """Cifra un mensaje con el cifrado Vernam (One-Time Pad)."""
    numerosTextoPlano = TextoANumeros(textoPlano)
    clave = [os.urandom(1)[0] for _ in numerosTextoPlano]
    numerosTextoCifrado = [p ^ k for p, k in zip(numerosTextoPlano, clave)]

    textoCifrado = NumerosATexto(numerosTextoCifrado)
    claveTexto = NumerosATexto(clave)

    return textoCifrado, claveTexto

def DescifrarVernam(textoCifrado: str, clave: str) -> str:
    """Descifra un mensaje cifrado con el cifrado Vernam."""
    numerosTextoCifrado = TextoANumeros(textoCifrado)
    numerosClave = TextoANumeros(clave)
    numerosTextoDescifrado = [c ^ k for c, k in zip(numerosTextoCifrado, numerosClave)]
    return NumerosATexto(numerosTextoDescifrado)