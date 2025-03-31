from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

# Constantes del cifrado Afín
alfabeto = "abcdefghijklmnñopqrstuvwxyz"
TAMAÑO_ALFABETO = len(alfabeto)

# Función para calcular el inverso multiplicativo módulo m
def calcularInversoMultiplicativo(a, m):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return 1

# Función para verificar si dos números son coprimos
def sonCoprimos(a, b):
    return math.gcd(a, b) == 1

# Función para cifrar un mensaje usando el cifrado Afín
def cifrar(palabra, a, b):
    if not sonCoprimos(a, TAMAÑO_ALFABETO):
        return "Error: El valor de 'a' debe ser coprimo con el tamaño del alfabeto."

    resultado = ""
    for letra in palabra.lower():
        if letra in alfabeto:
            indice = alfabeto.index(letra)
            nuevoIndice = (a * indice + b) % TAMAÑO_ALFABETO
            resultado += alfabeto[nuevoIndice]
        else:
            resultado += letra

    return resultado

# Función para descifrar un mensaje cifrado con el cifrado Afín
def descifrar(palabraCifrada, a, b):
    if not sonCoprimos(a, TAMAÑO_ALFABETO):
        return "Error: El valor de 'a' debe ser coprimo con el tamaño del alfabeto."

    aInverso = calcularInversoMultiplicativo(a, TAMAÑO_ALFABETO)
    resultado = ""

    for letra in palabraCifrada.lower():
        if letra in alfabeto:
            indice = alfabeto.index(letra)
            nuevoIndice = (aInverso * (indice - b)) % TAMAÑO_ALFABETO
            resultado += alfabeto[nuevoIndice]
        else:
            resultado += letra

    return resultado

# Función para descifrar usando fuerza bruta
def descifrarFuerzaBruta(palabraCifrada):
    posiblesResultados = []

    for a in range(1, TAMAÑO_ALFABETO):
        if sonCoprimos(a, TAMAÑO_ALFABETO):
            for b in range(TAMAÑO_ALFABETO):
                posibleTextoOriginal = descifrar(palabraCifrada, a, b)
                posiblesResultados.append({
                    "a": a,
                    "b": b,
                    "textoDescifrado": posibleTextoOriginal
                })

    return posiblesResultados

# Ruta principal
@app.route('/')
def paginaPrincipal():
    return render_template('index.html')

# API para cifrar
@app.route('/api/cifrar', methods=['POST'])
def apiCifrar():
    datos = request.json
    texto = datos.get('texto', '')
    a = int(datos.get('a', 1))
    b = int(datos.get('b', 0))

    resultado = cifrar(texto, a, b)

    return jsonify({
        "resultado": resultado,
        "resultado_texto": resultado,
        "exito": not resultado.startswith("Error")
    })

# API para descifrar
@app.route('/api/descifrar', methods=['POST'])
def apiDescifrar():
    datos = request.json
    texto = datos.get('texto', '')
    a = int(datos.get('a', 1))
    b = int(datos.get('b', 0))

    resultado = descifrar(texto, a, b)

    return jsonify({
        "resultado": resultado,
        "resultado_texto": resultado,
        "exito": not resultado.startswith("Error")
    })

# API para descifrar por fuerza bruta
@app.route('/api/fuerzaBruta', methods=['POST'])
def apiFuerzaBruta():
    datos = request.json
    texto = datos.get('texto', '')

    resultados = descifrarFuerzaBruta(texto)

    return jsonify({
        "resultados": resultados,
        "listaResultados": resultados,
        "exito": True
    })

if __name__ == '__main__':
    app.run(debug=True)

