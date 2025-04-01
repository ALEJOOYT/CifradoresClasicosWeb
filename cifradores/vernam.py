import os

def TextoANumeros(texto: str) -> list:
    return [ord(caracter) for caracter in texto]

def NumerosATexto(numeros: list) -> str:
    return ''.join(chr(numero) if 32 <= numero <= 126 else f'\\x{numero:02x}' for numero in numeros)

def Cifrar(textoPlano: str) -> tuple:
    numerosTextoPlano = TextoANumeros(textoPlano)
    clave = [os.urandom(1)[0] for _ in numerosTextoPlano]
    numerosTextoCifrado = [p ^ k for p, k in zip(numerosTextoPlano, clave)]
    textoCifrado = NumerosATexto(numerosTextoCifrado)
    claveTexto = NumerosATexto(clave)
    return textoCifrado, claveTexto

def Descifrar(textoCifrado: str, clave: str) -> str:
    if '\\x' in textoCifrado:
        textoCifrado = textoCifrado.encode().decode('unicode_escape')
    if '\\x' in clave:
        clave = clave.encode().decode('unicode_escape')
    numerosTextoCifrado = TextoANumeros(textoCifrado)
    numerosClave = TextoANumeros(clave)
    numerosTextoDescifrado = [c ^ k for c, k in zip(numerosTextoCifrado, numerosClave)]
    return NumerosATexto(numerosTextoDescifrado)
