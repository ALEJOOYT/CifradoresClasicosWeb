def OrdenarClave(clave):
    letrasConIndices = [(letra, i) for i, letra in enumerate(clave)]
    letrasOrdenadas = sorted(letrasConIndices, key=lambda x: x[0])
    orden = [indice for _, indice in letrasOrdenadas]
    return orden

def Cifrar(mensaje, clave):
    if not isinstance(clave, str):
        try:
            clave = str(clave)
        except:
            raise ValueError("La clave debe ser una cadena de texto")
    if not clave:
        raise ValueError("La clave no puede estar vacía")
    mensaje = mensaje.replace(" ", "")
    numFilas = len(clave)
    longitudMensaje = len(mensaje)
    numColumnas = (longitudMensaje + numFilas - 1) // numFilas
    matriz = [[''] * numColumnas for _ in range(numFilas)]
    indiceMensaje = 0
    for col in range(numColumnas):
        for fila in range(numFilas):
            if indiceMensaje < longitudMensaje:
                matriz[fila][col] = mensaje[indiceMensaje]
                indiceMensaje += 1
    ordenFilas = OrdenarClave(clave)
    mensajeCifrado = ""
    for indice in ordenFilas:
        mensajeCifrado += ''.join(matriz[indice])
    return mensajeCifrado

def Descifrar(mensajeCifrado, clave):
    if not isinstance(clave, str):
        try:
            clave = str(clave)
        except:
            raise ValueError("La clave debe ser una cadena de texto")
    if not clave:
        raise ValueError("La clave no puede estar vacía")
    numFilas = len(clave)
    longitudMensaje = len(mensajeCifrado)
    numColumnas = (longitudMensaje + numFilas - 1) // numFilas
    caracteresPorFila = longitudMensaje // numFilas
    filasExtra = longitudMensaje % numFilas
    matriz = [[''] * numColumnas for _ in range(numFilas)]
    ordenFilas = OrdenarClave(clave)
    indiceCifrado = 0
    for i, filaOriginal in enumerate(ordenFilas):
        longitudFila = caracteresPorFila + (1 if filaOriginal < filasExtra else 0)
        for col in range(longitudFila):
            if indiceCifrado < longitudMensaje:
                matriz[filaOriginal][col] = mensajeCifrado[indiceCifrado]
                indiceCifrado += 1
    mensajeDescifrado = ""
    for col in range(numColumnas):
        for fila in range(numFilas):
            if matriz[fila] and col < len(matriz[fila]) and matriz[fila][col]:
                mensajeDescifrado += matriz[fila][col]
    return mensajeDescifrado

def FormatearMensaje(mensaje, longitudBloque=5):
    mensajeFormateado = ''
    for i in range(0, len(mensaje), longitudBloque):
        mensajeFormateado += mensaje[i:i+longitudBloque] + ' '
    return mensajeFormateado.strip()

def MostrarMatriz(matriz):
    for fila in matriz:
        print(''.join(fila))

def CrearMatriz(mensaje, clave):
    if not isinstance(clave, str):
        try:
            clave = str(clave)
        except:
            raise ValueError("La clave debe ser una cadena de texto")
    if not clave:
        raise ValueError("La clave no puede estar vacía")
    mensaje = mensaje.replace(" ", "")
    numFilas = len(clave)
    longitudMensaje = len(mensaje)
    numColumnas = (longitudMensaje + numFilas - 1) // numFilas
    matriz = [[''] * numColumnas for _ in range(numFilas)]
    indiceMensaje = 0
    for col in range(numColumnas):
        for fila in range(numFilas):
            if indiceMensaje < longitudMensaje:
                matriz[fila][col] = mensaje[indiceMensaje]
                indiceMensaje += 1
            else:
                matriz[fila][col] = 'X'
    print("\nMatriz original:")
    print("Clave:", clave)
    for i, letra in enumerate(clave):
        print(f"{letra}: {' '.join(matriz[i])}")
    ordenFilas = OrdenarClave(clave)
    print("\nClave ordenada alfabéticamente:", ''.join(sorted(clave)))
    print("Orden de filas:", [i+1 for i in ordenFilas])
    print("\nMatriz reordenada:")
    for i in ordenFilas:
        print(f"{clave[i]}: {' '.join(matriz[i])}")
    return matriz