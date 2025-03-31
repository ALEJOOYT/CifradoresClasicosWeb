import re
from itertools import permutations

# Genera la matriz 5x5
def GenerarMatrizPlayfair(palabraClave):
    palabraClave = palabraClave.upper().replace("J", "I")
    visto = set()
    matriz = []
    abecedario = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    for caracter in palabraClave + abecedario:
        if caracter not in visto:
            visto.add(caracter)
            matriz.append(caracter)
    return [matriz[i:i+5] for i in range(0, 25, 5)]

# Encuentra posición de una letra
def EncontrarPosiciones(matriz, caracter):
    for fila in range(5):
        for columna in range(5):
            if matriz[fila][columna] == caracter:
                return fila, columna

# Descifra un par de letras
def DescifrarPar(matriz, caracter1, caracter2):
    fila1, columna1 = EncontrarPosiciones(matriz, caracter1)
    fila2, columna2 = EncontrarPosiciones(matriz, caracter2)
    if fila1 == fila2:
        return matriz[fila1][(columna1 - 1) % 5] + matriz[fila2][(columna2 - 1) % 5]
    elif columna1 == columna2:
        return matriz[(fila1 - 1) % 5][columna1] + matriz[(fila2 - 1) % 5][columna2]
    else:
        return matriz[fila1][columna2] + matriz[fila2][columna1]

# Descifra todo el mensaje
def DescifrarMensaje(matriz, mensaje):
    textoDescifrado = ""
    for i in range(0, len(mensaje), 2):
        textoDescifrado += DescifrarPar(matriz, mensaje[i], mensaje[i+1])
    return textoDescifrado

# Genera claves posibles
def GenerarPalabrasClave(maxPalabrasClave=300000):
    base = "SEGURBICDFAHKLMNOPQTVWXYZ"  # Letras sin J
    #base = "TECNOLBGDIFAHKMPQRSUVWXYZ"
    #base = "CRIPTBODGEAHFKLMNQSUVWXYZ"
    contador = 0
    for r in range(8, 11):  # Claves de longitud entre 8 y 10
        for p in permutations(base, r):
            palabraClave = ''.join(p)
            yield palabraClave
            contador += 1
            if contador >= maxPalabrasClave:
                return

# Fuerza bruta con impresión directa
def FuerzaBrutaPlayfair(mensajeCifrado, maxPalabrasClave=1000):
    mensajeCifrado = re.sub(r'[^A-Z]', '', mensajeCifrado.upper().replace("J", "I"))
    print(f"Fuerza bruta sobre mensaje cifrado: {mensajeCifrado}")
    print(f"Total de claves a probar: {maxPalabrasClave}\n")
    for palabraClave in GenerarPalabrasClave(maxPalabrasClave):
        matriz = GenerarMatrizPlayfair(palabraClave)
        descifrado = DescifrarMensaje(matriz, mensajeCifrado)
        print(f"Clave: {palabraClave:<10} → Descifrado: {descifrado}")

# Ejecutar fuerza bruta
if __name__ == "__main__":
    mensajeCifrado = input("Introduce el mensaje cifrado (en pares de letras): ")
    maxPalabrasClave = int(input("¿Cuántas claves deseas probar?: "))
    FuerzaBrutaPlayfair(mensajeCifrado, maxPalabrasClave)
