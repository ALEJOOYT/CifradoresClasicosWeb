import math
import itertools

def Cifrar(mensaje, clave):
    cifrado = ""
    indiceClave = 0
    longitudMensaje = float(len(mensaje))
    listaMensaje = list(mensaje)
    listaClaveOrdenada = sorted(list(clave))

    columnas = len(clave)
    filas = int(math.ceil(longitudMensaje / columnas))
    relleno = int((filas * columnas) - longitudMensaje)
    listaMensaje.extend('_' * relleno)

    matriz = [listaMensaje[i: i + columnas] for i in range(0, len(listaMensaje), columnas)]

    for _ in range(columnas):
        indiceActual = clave.index(listaClaveOrdenada[indiceClave])
        cifrado += ''.join([fila[indiceActual] for fila in matriz])
        indiceClave += 1

    return cifrado

def Descifrar(cifrado, clave):
    mensaje = ""
    indiceClave = 0
    indiceMensaje = 0
    longitudMensaje = float(len(cifrado))
    listaMensaje = list(cifrado)

    columnas = len(clave)
    filas = int(math.ceil(longitudMensaje / columnas))
    listaClaveOrdenada = sorted(list(clave))

    matrizDescifrado = []
    for _ in range(filas):
        matrizDescifrado += [[None] * columnas]

    for _ in range(columnas):
        indiceActual = clave.index(listaClaveOrdenada[indiceClave])

        for j in range(filas):
            matrizDescifrado[j][indiceActual] = listaMensaje[indiceMensaje]
            indiceMensaje += 1
        indiceClave += 1

    try:
        mensaje = ''.join(sum(matrizDescifrado, []))
    except TypeError:
        raise TypeError("Este programa no puede manejar palabras repetidas.")

    cantidadRelleno = mensaje.count('_')
    if cantidadRelleno > 0:
        return mensaje[: -cantidadRelleno]

    return mensaje

def DescifradoFuerzaBruta(cifrado, longitudClaveOriginal):
    numeros = list(range(longitudClaveOriginal))
    posiblesPermutaciones = itertools.permutations(numeros)
    resultados = []

    for permutacion in posiblesPermutaciones:
        clave = ''.join(chr(65 + num) for num in permutacion)
        try:
            textoDescifrado = Descifrar(cifrado, clave)
            resultados.append({
                "permutacion": ''.join(str(num) for num in permutacion),
                "textoDescifrado": textoDescifrado
            })
        except Exception:
            continue

    return resultados
