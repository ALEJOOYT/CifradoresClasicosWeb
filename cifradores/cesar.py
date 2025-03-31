def CifrarCesar(texto, desplazamiento):
    resultado = ''
    for caracter in texto:
        if caracter.isalpha():
            inicio = ord('A') if caracter.isupper() else ord('a')
            resultado += chr(inicio + (ord(caracter) - inicio + desplazamiento) % 26)
        else:
            resultado += caracter
    return resultado

def DescifrarCesar(textoCifrado, desplazamiento):
    return CifrarCesar(textoCifrado, -desplazamiento)

def FuerzaBrutaCesar(textoCifrado):
    resultados = []
    for i in range(1, 26):
        posibleDescifrado = DescifrarCesar(textoCifrado, i)
        resultados.append((i, posibleDescifrado))
    print("\nResultados de Fuerza Bruta:")
    for i, descifrado in resultados:
        print(f"Desplazamiento {i}: {descifrado}")
    return resultados