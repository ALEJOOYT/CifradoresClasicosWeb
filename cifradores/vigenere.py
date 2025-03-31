import itertools
import string
import os

def LimpiarConsola():
    os.system('cls' if os.name == 'nt' else 'clear')

def PalabrasComunes():
    # Lista de palabras comunes en español
    return set([
        "hola", "adios", "casa", "tiempo", "vida", "mundo", "gracias", "persona",
        "trabajo", "amor", "dia", "año", "ciudad", "familia", "agua", "comida",
        "amigo", "mañana", "noche", "escuela", "universidad", "estudiante", "profesor",
        "libro", "papel", "palabra", "mensaje", "carta", "entre", "sobre", "para",
        "como", "cuando", "donde", "porque", "aunque", "desde", "hasta", "durante",
        "mientras", "siempre", "nunca", "ahora", "antes", "despues", "mucho", "poco",
        "todo", "nada", "algo", "alguien", "nadie", "cada", "cualquier", "otro",
        "mismo", "tanto", "tan", "solo", "bueno", "malo", "feliz", "triste",
        "grande", "pequeño", "nuevo", "viejo", "alto", "bajo", "largo", "corto",
        "importante", "necesario", "posible", "imposible", "facil", "dificil",
        "rapido", "lento", "fuerte", "debil", "primera", "ultima", "siguiente",
        "anterior", "principal", "secundario", "diferente", "similar", "mejor", "peor",
        "este", "ese", "aquel", "uno", "dos", "tres", "cuatro", "cinco", "seis",
        "siete", "ocho", "nueve", "diez", "cien", "mil", "millon", "poder", "querer",
        "deber", "tener", "hacer", "ver", "oir", "sentir", "pensar", "saber", "conocer",
        "hablar", "decir", "escribir", "leer", "entender", "comprender", "recordar",
        "olvidar", "comenzar", "terminar", "comer", "beber", "dormir", "despertar",
        "caminar", "correr", "saltar", "nadar", "volar", "caer", "subir", "bajar"
    ])

def GenerarClave(texto, clave):
    clave = list(clave)
    for i in range(len(texto) - len(clave)):
        clave.append(clave[i % len(clave)])
    return "".join(clave)

def Cifrar(textoPlano, clave):
    textoCifrado = []
    clave = GenerarClave(textoPlano, clave)
    for t, k in zip(textoPlano, clave):
        if t.isalpha():
            base = ord('A') if t.isupper() else ord('a')
            cifrado = (ord(t) - base + ord(k.lower()) - ord('a')) % 26
            textoCifrado.append(chr(cifrado + base))
        else:
            textoCifrado.append(t)
    return "".join(textoCifrado)

def Descifrar(textoCifrado, clave):
    textoDescifrado = []
    clave = GenerarClave(textoCifrado, clave)
    for t, k in zip(textoCifrado, clave):
        if t.isalpha():
            base = ord('A') if t.isupper() else ord('a')
            descifrado = (ord(t) - base - (ord(k.lower()) - ord('a'))) % 26
            textoDescifrado.append(chr(descifrado + base))
        else:
            textoDescifrado.append(t)
    return "".join(textoDescifrado)

def PuntuacionLegibilidad(texto, diccionario):
    palabras = ''.join(c if c.isalpha() else ' ' for c in texto.lower()).split()
    return sum(1 for palabra in palabras if palabra in diccionario)

def DescifrarFuerzaBrutaVigenere(textoCifrado, maxLargo=4, top=5):
    diccionario = PalabrasComunes()
    abecedario = string.ascii_lowercase
    resultados = []

    for largo in range(1, maxLargo + 1):
        for claveTuple in itertools.product(abecedario, repeat=largo):
            clave = ''.join(claveTuple)
            descifrado = Descifrar(textoCifrado, clave)
            puntuacion = PuntuacionLegibilidad(descifrado, diccionario)
            # Incluir todos los resultados, sin filtrar por puntuación
            resultados.append({
                'clave': clave,
                'textoDescifrado': descifrado,
                'puntuacion': puntuacion
            })

    resultados.sort(key=lambda x: x['puntuacion'], reverse=True)

    # Devolver todos los resultados sin aplicar el límite top
    return resultados if resultados else []
