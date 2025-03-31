from flask import Flask, render_template, request, jsonify
# Importar módulos de cifrado
from cifradores.afin import Cifrar as CifrarAfin
from cifradores.afin import Descifrar as DescifrarAfin
from cifradores.afin import DescifrarFuerzaBruta as DescifrarFuerzaBrutaAfin

from cifradores.adfgvx import Cifrar as CifrarAdfgvx
from cifradores.adfgvx import Descifrar as DescifrarAdfgvx
from cifradores.adfgvx import GenerarClaveAleatoria as GenerarClaveAleatoriaAdfgvx
from cifradores.adfgvx import GenerarCuadro as GenerarCuadroAdfgvx

app = Flask(__name__)

# Ruta principal
@app.route('/')
def PaginaPrincipal():
    return render_template('index.html')
# API para cifrar
@app.route('/api/cifrar', methods=['POST'])
def ApiCifrar():
    datos = request.json
    texto = datos.get('texto', '')
    a = int(datos.get('a', 1))
    b = int(datos.get('b', 0))

    resultado = CifrarAfin(texto, a, b)

    return jsonify({
        "resultado": resultado,
        "resultado_texto": resultado,
        "exito": not resultado.startswith("Error")
    })
# API para descifrar
@app.route('/api/descifrar', methods=['POST'])
def ApiDescifrar():
    datos = request.json
    texto = datos.get('texto', '')
    a = int(datos.get('a', 1))
    b = int(datos.get('b', 0))

    resultado = DescifrarAfin(texto, a, b)

    return jsonify({
        "resultado": resultado,
        "resultado_texto": resultado,
        "exito": not resultado.startswith("Error")
    })
# API para descifrar por fuerza bruta
@app.route('/api/fuerzaBruta', methods=['POST'])
def ApiFuerzaBruta():
    datos = request.json
    texto = datos.get('texto', '')

    resultados = DescifrarFuerzaBrutaAfin(texto)

    return jsonify({
        "resultados": resultados,
        "listaResultados": resultados,
        "exito": True
    })
# API para cifrar con ADFGVX
@app.route('/api/cifrarAdfgvx', methods=['POST'])
def ApiCifrarAdfgvx():
    datos = request.json
    texto = datos.get('texto', '')
    matriz = datos.get('matriz', '')
    clave = datos.get('clave', '')

    if not matriz:
        matriz = GenerarClaveAleatoriaAdfgvx()

    try:
        cuadro = GenerarCuadroAdfgvx(matriz)
        resultado = CifrarAdfgvx(texto, cuadro, clave)
        return jsonify({
            "resultado": resultado,
            "matriz": matriz,
            "exito": True
        })
    except ValueError as e:
        return jsonify({"resultado": f"Error: {str(e)}", "exito": False})
# API para descifrar con ADFGVX
@app.route('/api/descifrarAdfgvx', methods=['POST'])
def ApiDescifrarAdfgvx():
    datos = request.json
    texto = datos.get('texto', '')
    matriz = datos.get('matriz', '')
    clave = datos.get('clave', '')

    try:
        cuadro = GenerarCuadroAdfgvx(matriz)
        resultado = DescifrarAdfgvx(texto, cuadro, clave)
        return jsonify({
            "resultado": resultado,
            "exito": True
        })
    except ValueError as e:
        return jsonify({"resultado": f"Error: {str(e)}", "exito": False})
# API para generar una matriz aleatoria para ADFGVX
@app.route('/api/generarMatrizAdfgvx', methods=['GET'])
def ApiGenerarMatrizAdfgvx():
    try:
        matriz = GenerarClaveAleatoriaAdfgvx()
        return jsonify({"matriz": matriz, "exito": True})
    except Exception as e:
        return jsonify({"error": f"Error al generar matriz: {str(e)}", "exito": False})

if __name__ == '__main__':
    app.run(debug=True)
