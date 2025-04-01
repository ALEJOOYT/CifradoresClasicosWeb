def Cifrar(texto, clave):
    cerca = [['\n' for _ in range(len(texto))] for _ in range(clave)]
    direccionAbajo = False
    fila, columna = 0, 0

    for i in range(len(texto)):
        if fila == 0 or fila == clave - 1:
            direccionAbajo = not direccionAbajo
        cerca[fila][columna] = texto[i]
        columna += 1
        fila += 1 if direccionAbajo else -1

    resultado = []
    for i in range(clave):
        for j in range(len(texto)):
            if cerca[i][j] != '\n':
                resultado.append(cerca[i][j])
    return "".join(resultado)

def Descifrar(cifrado, clave):
    cerca = [['\n' for _ in range(len(cifrado))] for _ in range(clave)]
    direccionAbajo = None
    fila, columna = 0, 0

    for i in range(len(cifrado)):
        if fila == 0:
            direccionAbajo = True
        if fila == clave - 1:
            direccionAbajo = False
        cerca[fila][columna] = '*'
        columna += 1
        fila += 1 if direccionAbajo else -1

    indice = 0
    for i in range(clave):
        for j in range(len(cifrado)):
            if cerca[i][j] == '*' and indice < len(cifrado):
                cerca[i][j] = cifrado[indice]
                indice += 1

    resultado = []
    fila, columna = 0, 0
    for i in range(len(cifrado)):
        if fila == 0:
            direccionAbajo = True
        if fila == clave - 1:
            direccionAbajo = False
        if cerca[fila][columna] != '*':
            resultado.append(cerca[fila][columna])
            columna += 1
        fila += 1 if direccionAbajo else -1
    return "".join(resultado)

def DescifrarFuerzaBruta(cifrado, claveInicio=2, claveFin=10):
    resultados = []
    for clave in range(claveInicio, claveFin + 1):
        try:
            descifrado = Descifrar(cifrado, clave)
            resultados.append((clave, descifrado))
        except:
            continue
    return resultados
