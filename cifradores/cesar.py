def Cifrar(texto, desplazamiento):
    resultado = ''
    for caracter in texto:
        if caracter.isalpha():
            inicio = ord('A') if caracter.isupper() else ord('a')
            resultado += chr(inicio + (ord(caracter) - inicio + desplazamiento) % 26)
        else:
            resultado += caracter
    return resultado

def Descifrar(textoCifrado, desplazamiento):
    return Cifrar(textoCifrado, -desplazamiento)

def DescifrarFuerzaBruta(textoCifrado):
    resultados = []
    for i in range(1, 26):
        posibleDescifrado = Descifrar(textoCifrado, i)
        resultados.append({
            "key": f"Desplazamiento {i}",
            "text": posibleDescifrado
        })
    return resultados
