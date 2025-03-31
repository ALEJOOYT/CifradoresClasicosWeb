from flask import Flask, render_template, request, jsonify
# Importar módulos de cifrado
from cifradores.afin import cifrar as cifrar_afin
from cifradores.afin import descifrar as descifrar_afin
from cifradores.afin import descifrarFuerzaBruta
from cifradores.adfgvx import cifrar as cifrar_adfgvx
from cifradores.adfgvx import descifrar as descifrar_adfgvx
from cifradores.adfgvx import generate_random_polybius_key

app = Flask(__name__)

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

    resultado = cifrar_afin(texto, a, b)

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

    resultado = descifrar_afin(texto, a, b)

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

# API para cifrar con ADFGVX
@app.route('/api/cifrarAdfgvx', methods=['POST'])
def apiCifrarAdfgvx():
    datos = request.json
    texto = datos.get('texto', '')
    matriz = datos.get('matriz', '')
    clave_transposicion = datos.get('clave', '')  # Changed from 'claveTransposicion' to 'clave' to match frontend

    # Generar una matriz aleatoria si no se proporciona una
    if not matriz:
        matriz = generate_random_polybius_key()

    try:
        resultado = cifrar_adfgvx(texto, matriz, clave_transposicion)
        return jsonify({
            "resultado": resultado,
            "resultado_texto": resultado,
            "matriz": matriz,  # Devolver la matriz para que el usuario la vea
            "exito": not resultado.startswith("Error")
        })
    except ValueError as e:
        return jsonify({
            "resultado": f"Error: {str(e)}",
            "resultado_texto": f"Error: {str(e)}",
            "exito": False
        })

# API para descifrar con ADFGVX
@app.route('/api/descifrarAdfgvx', methods=['POST'])
def apiDescifrarAdfgvx():
    datos = request.json
    texto = datos.get('texto', '')
    matriz = datos.get('matriz', '')
    clave_transposicion = datos.get('clave', '')  # Changed from 'claveTransposicion' to 'clave' to match frontend

    try:
        resultado = descifrar_adfgvx(texto, matriz, clave_transposicion)
        return jsonify({
            "resultado": resultado,
            "resultado_texto": resultado,
            "exito": not resultado.startswith("Error")
        })
    except ValueError as e:
        return jsonify({
            "resultado": f"Error: {str(e)}",
            "resultado_texto": f"Error: {str(e)}",
            "exito": False
        })
# API para generar matriz aleatoria para ADFGVX
@app.route('/api/generarMatrizAdfgvx', methods=['GET'])
def apiGenerarMatrizAdfgvx():
    try:
        matriz = generate_random_polybius_key()
        return jsonify({
            "matriz": matriz,
            "exito": True
        })
    except Exception as e:
        return jsonify({
            "error": f"Error al generar matriz: {str(e)}",
            "exito": False
        })

if __name__ == '__main__':
    app.run(debug=True)
