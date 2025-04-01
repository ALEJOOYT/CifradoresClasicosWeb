from flask import Flask, render_template, request, jsonify
import json
# Importar módulos de cifrado
from cifradores.afin import Cifrar as CifrarAfin
from cifradores.afin import Descifrar as DescifrarAfin
from cifradores.afin import DescifrarFuerzaBruta as FuerzaBrutaAfin

from cifradores.adfgvx import Cifrar as CifrarAdfgvx
from cifradores.adfgvx import Descifrar as DescifrarAdfgvx
from cifradores.adfgvx import GenerarClaveAleatoria

from cifradores.playFair import Cifrar as CifrarPlayfair
from cifradores.playFair import Descifrar as DescifrarPlayfair
from cifradores.playFair import DescifrarFuerzaBruta as FuerzaBrutaPlayfair

from cifradores.cesar import Cifrar as CifrarCesar
from cifradores.cesar import Descifrar as DescifrarCesar
from cifradores.cesar import DescifrarFuerzaBruta as FuerzaBrutaCesar

from cifradores.hill import Cifrar as CifrarHill
from cifradores.hill import Descifrar as DescifrarHill
from cifradores.hill import GenerarMatrizAleatoria
from cifradores.hill import DescifrarFuerzaBruta as FuerzaBrutaHill

from cifradores.vigenere import Cifrar as CifrarVigenere
from cifradores.vigenere import Descifrar as DescifrarVigenere
from cifradores.vigenere import DescifrarFuerzaBruta as FuerzaBrutaVigenere

from cifradores.transposicionColumna import Cifrar as CifrarTransposicionColumna
from cifradores.transposicionColumna import Descifrar as DescifrarTransposicionColumna
from cifradores.transposicionColumna import DescifradoFuerzaBruta as FuerzaBrutaTransposicionColumna

from cifradores.transposicionRail import Cifrar as CifrarRailFence
from cifradores.transposicionRail import Descifrar as DescifrarRailFence
from cifradores.transposicionRail import DescifrarFuerzaBruta as FuerzaBrutaRailFence

app = Flask(__name__)

# Diccionario de funciones de cifrado y descifrado
CIFRADORES = {
    'cesar': {'cifrar': CifrarCesar, 'descifrar': DescifrarCesar},
    'afin': {'cifrar': CifrarAfin, 'descifrar': DescifrarAfin},
    'adfgvx': {'cifrar': CifrarAdfgvx, 'descifrar': DescifrarAdfgvx},
    'playfair': {'cifrar': CifrarPlayfair, 'descifrar': DescifrarPlayfair},
    'hill': {'cifrar': CifrarHill, 'descifrar': DescifrarHill},
    'vigenere': {'cifrar': CifrarVigenere, 'descifrar': DescifrarVigenere},
    'transposicionColumna': {'cifrar': CifrarTransposicionColumna, 'descifrar': DescifrarTransposicionColumna},
    'transposicionRail': {'cifrar': CifrarRailFence, 'descifrar': DescifrarRailFence}
}

# Diccionario de funciones de fuerza bruta
FUERZA_BRUTA = {
    'cesar': FuerzaBrutaCesar,
    'afin': FuerzaBrutaAfin,
    'playfair': FuerzaBrutaPlayfair,
    'hill': FuerzaBrutaHill,
    'vigenere': FuerzaBrutaVigenere,
    'transposicionColumna': FuerzaBrutaTransposicionColumna,
    'transposicionRail': FuerzaBrutaRailFence
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/procesar', methods=['POST'])
def ProcesarTexto():
    try:
        datos = request.get_json()
        operacion = datos.get('operacion')
        cifrador = datos.get('cifrador')
        texto = datos.get('texto')
        parametros = datos.get('parametros', {})

        if not all([operacion, cifrador, texto]):
            return jsonify({'error': 'Faltan parámetros requeridos'}), 400

        if cifrador not in CIFRADORES:
            return jsonify({'error': 'Cifrador no soportado'}), 400

        funcion = CIFRADORES[cifrador]['cifrar'] if operacion == 'cifrar' else CIFRADORES[cifrador]['descifrar']

        # Procesar según el cifrador
        if cifrador == 'cesar':
            resultado = funcion(texto, int(parametros['desplazamiento']))
        elif cifrador == 'afin':
            resultado = funcion(texto, int(parametros['a']), int(parametros['b']))
        elif cifrador == 'adfgvx':
            resultado = funcion(texto, parametros['clave'])
        elif cifrador in ['playfair', 'vigenere', 'transposicionColumna']:
            resultado = funcion(texto, parametros['clave'])
        elif cifrador == 'hill':
            if 'matriz' in parametros:
                matriz = json.loads(parametros['matriz'])
            else:
                return jsonify({'error': 'Se requiere la matriz para el cifrado Hill'}), 400
            resultado = funcion(texto, matriz)
        elif cifrador == 'transposicionRail':
            resultado = funcion(texto, int(parametros['rieles']))
        else:
            return jsonify({'error': 'Método de cifrado no soportado'}), 400

        return jsonify({'resultado': resultado})

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/operaciones-especiales', methods=['POST'])
def OperacionesEspeciales():
    try:
        datos = request.get_json()
        cifrador = datos.get('cifrador')
        operacion = datos.get('operacion')

        if not cifrador or not operacion:
            return jsonify({'error': 'Faltan parámetros requeridos'}), 400

        if cifrador == 'hill':
            if operacion == 'generarMatriz':
                matriz = GenerarMatrizAleatoria()
                return jsonify({'resultado': matriz})
            else:
                return jsonify({'error': 'Operación no soportada para el cifrador Hill'}), 400
        elif cifrador == 'adfgvx':
            if operacion == 'generarClave':
                clave = GenerarClaveAleatoria()
                return jsonify({'resultado': clave})
            else:
                return jsonify({'error': 'Operación no soportada para el cifrador ADFGVX'}), 400
        else:
            return jsonify({'error': 'Cifrador no soportado para operaciones especiales'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/fuerza_bruta', methods=['POST'])
def FuerzaBrutaTexto():
    try:
        datos = request.get_json()
        cifrador = datos.get('cifrador')
        texto = datos.get('texto')
        parametros = datos.get('parametros', {})

        if not cifrador or not texto:
            return jsonify({'error': 'Faltan parámetros requeridos'}), 400

        if cifrador not in FUERZA_BRUTA:
            return jsonify({'error': 'El cifrador seleccionado no soporta fuerza bruta'}), 400

        # Procesar según el cifrador
        if cifrador == 'cesar':
            resultados = FuerzaBrutaCesar(texto)
        elif cifrador == 'afin':
            resultados = FuerzaBrutaAfin(texto)
        elif cifrador == 'playfair':
            # Si hay palabras clave proporcionadas, usarlas
            palabras_clave = parametros.get('palabrasClave', None)
            if palabras_clave:
                # Convertir string de palabras clave separadas por comas a lista
                palabras_clave = [p.strip() for p in palabras_clave.split(',')]
            resultado = FuerzaBrutaPlayfair(texto, palabras_clave)
            
            # Manejar errores específicos de Playfair
            if resultado.get('error'):
                return jsonify({'error': resultado['error']}), 400
            
            # Formatear los resultados de Playfair
            resultados = []
            for r in resultado['resultados']:
                resultados.append(
                    f"Clave: {r['clave']} | "
                    f"Texto descifrado: {r['textoDescifrado']} | "
                    f"Puntaje: {r['puntaje']}%"
                )
        elif cifrador == 'hill':
            resultados = FuerzaBrutaHill(texto)
        elif cifrador == 'vigenere':
            max_largo = parametros.get('maxLargo', 4)
            top = parametros.get('top', 5)
            resultados = FuerzaBrutaVigenere(texto, max_largo, top)
        elif cifrador == 'transposicionColumna':
            longitud_clave = parametros.get('longitudClave', 4)
            resultados = FuerzaBrutaTransposicionColumna(texto, longitud_clave)
        elif cifrador == 'transposicionRail':
            clave_inicio = parametros.get('claveInicio', 2)
            clave_fin = parametros.get('claveFin', 10)
            resultados = FuerzaBrutaRailFence(texto, clave_inicio, clave_fin)
        else:
            return jsonify({'error': 'El cifrador seleccionado no soporta fuerza bruta'}), 400

        if not resultados:
            return jsonify({'error': 'No se encontraron resultados'}), 400

        return jsonify({'resultados': resultados})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
