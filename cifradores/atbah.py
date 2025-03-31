def Cifrar(texto):
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alfabetoReverso = alfabeto[::-1]
    tablaTraduccion = str.maketrans(alfabeto + alfabeto.lower(), alfabetoReverso + alfabetoReverso.lower())
    return texto.translate(tablaTraduccion)

def Descifrar(texto):
    return Cifrar(texto)