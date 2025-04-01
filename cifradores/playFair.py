def GenerarMatriz(clave):
    clave = clave.upper().replace(" ", "")
    clave = clave.replace("J", "I")
    matriz = []
    letrasUsadas = []
    for letra in clave:
        if letra not in letrasUsadas and letra.isalpha():
            letrasUsadas.append(letra)
    alfabeto = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    for letra in alfabeto:
        if letra not in letrasUsadas:
            letrasUsadas.append(letra)
    for i in range(0, 25, 5):
        matriz.append(letrasUsadas[i:i+5])
    return matriz

def EncontrarPosicion(matriz, letra):
    letra = letra.upper()
    if letra == 'J':
        letra = 'I'
    for i in range(5):
        for j in range(5):
            if matriz[i][j] == letra:
                return (i, j)
    return None

def PrepararBigramas(texto):
    texto = ''.join(c.upper() for c in texto if c.isalpha())
    texto = texto.replace("J", "I")
    bigramas = []
    i = 0
    while i < len(texto):
        if i == len(texto) - 1:
            bigramas.append(texto[i] + 'X')
            i += 1
        elif texto[i] == texto[i+1]:
            bigramas.append(texto[i] + 'X')
            i += 1
        else:
            bigramas.append(texto[i:i+2])
            i += 2
    return bigramas

def Cifrar(texto, clave):
    try:
        if not texto or not clave:
            return "Error: El texto y la clave son requeridos."
        if not any(c.isalpha() for c in clave):
            return "Error: La clave debe contener al menos una letra."
        matriz = GenerarMatriz(clave)
        bigramas = PrepararBigramas(texto)
        textoCifrado = ""
        for bigrama in bigramas:
            pos1 = EncontrarPosicion(matriz, bigrama[0])
            pos2 = EncontrarPosicion(matriz, bigrama[1])
            if pos1[0] == pos2[0]:
                textoCifrado += matriz[pos1[0]][(pos1[1] + 1) % 5]
                textoCifrado += matriz[pos2[0]][(pos2[1] + 1) % 5]
            elif pos1[1] == pos2[1]:
                textoCifrado += matriz[(pos1[0] + 1) % 5][pos1[1]]
                textoCifrado += matriz[(pos2[0] + 1) % 5][pos2[1]]
            else:
                textoCifrado += matriz[pos1[0]][pos2[1]]
                textoCifrado += matriz[pos2[0]][pos1[1]]
        return textoCifrado
    except Exception as e:
        return f"Error: {str(e)}"

def Descifrar(textoCifrado, clave):
    try:
        if not textoCifrado or not clave:
            return "Error: El texto cifrado y la clave son requeridos."
        if not any(c.isalpha() for c in clave):
            return "Error: La clave debe contener al menos una letra."
        matriz = GenerarMatriz(clave)
        bigramas = [textoCifrado[i:i+2] for i in range(0, len(textoCifrado), 2)]
        textoDescifrado = ""
        for bigrama in bigramas:
            pos1 = EncontrarPosicion(matriz, bigrama[0])
            pos2 = EncontrarPosicion(matriz, bigrama[1])
            if pos1[0] == pos2[0]:
                textoDescifrado += matriz[pos1[0]][(pos1[1] - 1) % 5]
                textoDescifrado += matriz[pos2[0]][(pos2[1] - 1) % 5]
            elif pos1[1] == pos2[1]:
                textoDescifrado += matriz[(pos1[0] - 1) % 5][pos1[1]]
                textoDescifrado += matriz[(pos2[0] - 1) % 5][pos2[1]]
            else:
                textoDescifrado += matriz[pos1[0]][pos2[1]]
                textoDescifrado += matriz[pos2[0]][pos1[1]]
        return textoDescifrado
    except Exception as e:
        return f"Error: {str(e)}"

def DescifrarFuerzaBruta(textoCifrado, palabrasClave=None):
    try:
        if not textoCifrado:
            return {"error": "El texto cifrado es requerido para la fuerza bruta.", "resultados": []}
        textoCifrado = ''.join(c.upper() for c in textoCifrado if c.isalpha())
        if len(textoCifrado) < 2:
            return {"error": "El texto cifrado debe tener al menos 2 caracteres alfabéticos.", "resultados": []}
        palabras_predeterminadas = [
            "CLAVE", "SECRETO", "ENIGMA", "CIFRADO", "CODIGO",
            "MENSAJE", "SEGURO", "OCULTO", "PRIVADO", "PLAYFAIR",
            "MATRIZ", "SISTEMA", "METODO", "PALABRA", "TEXTO"
        ]
        if palabrasClave and isinstance(palabrasClave, (list, tuple)) and len(palabrasClave) > 0:
            palabras_a_probar = [p.strip().upper() for p in palabrasClave if p.strip()]
        else:
            palabras_a_probar = palabras_predeterminadas

        if not palabras_a_probar:
            return {"error": "No hay palabras clave válidas para probar.", "resultados": []}

        resultados = []
        for clave in palabras_a_probar:
            if not any(c.isalpha() for c in clave):
                continue

            try:
                texto_descifrado = Descifrar(textoCifrado, clave)
                if isinstance(texto_descifrado, str) and not texto_descifrado.startswith("Error"):
                    vocales = sum(1 for c in texto_descifrado if c in "AEIOU")
                    consonantes_comunes = sum(1 for c in texto_descifrado if c in "NRSLT")
                    puntaje = (vocales * 1.5 + consonantes_comunes) / len(texto_descifrado) * 100

                    resultados.append({
                        "clave": clave,
                        "textoDescifrado": texto_descifrado,
                        "puntaje": round(puntaje, 2)
                    })
            except Exception:
                continue

        resultados = sorted(resultados, key=lambda x: x["puntaje"], reverse=True)
        if not resultados:
            return {
                "error": "No se encontraron resultados válidos con las claves probadas.",
                "resultados": []
            }

        resultados = resultados[:10]

        return {
            "error": None,
            "resultados": resultados
        }

    except Exception as e:
        return {
            "error": f"Error en la fuerza bruta: {str(e)}",
            "resultados": []
        }
