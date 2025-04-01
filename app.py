from flask import Flask, render_template, request, jsonify
# Importar módulos de cifrado
from cifradores.afin import Cifrar as CifrarAfin
from cifradores.afin import Descifrar as DescifrarAfin

from cifradores.adfgvx import Cifrar as CifrarAdfgvx
from cifradores.adfgvx import Descifrar as DescifrarAdfgvx

from cifradores.playFair import Cifrar as CifrarPlayfair
from cifradores.playFair import Descifrar as DescifrarPlayfair

from cifradores.cesar import Cifrar as CifrarCesar
from cifradores.cesar import Descifrar as DescifrarCesar

from cifradores.hill import Cifrar as CifrarHill
from cifradores.hill import Descifrar as DescifrarHill

from cifradores.vernam import CifrarVernam as CifrarVernam
from cifradores.vernam import DescifrarVernam as DescifrarVernam

from cifradores.vigenere import Cifrar as CifrarVigenere
from cifradores.vigenere import Descifrar as DescifrarVigenere

from cifradores.atbash import Cifrar as CifrarAtbash
from cifradores.atbash import Descifrar as DescifrarAtbash

from cifradores.transposicionColumna import Cifrar as CifrarTransposicionColumna
from cifradores.transposicionColumna import Descifrar as DescifrarTransposicionColumna

from cifradores.transposicionFilas import Cifrar as CifrarTransposicionFilas
from cifradores.transposicionFilas import Descifrar as DescifrarTransposicionFilas

from cifradores.transposicionRail import Cifrar as CifrarRailFence
from cifradores.transposicionRail import Descifrar as DescifrarRailFence

app = Flask(__name__)

# Diccionario de funciones de cifrado y descifrado
CIFRADORES = {
    'cesar': {'cifrar': CifrarCesar, 'descifrar': DescifrarCesar},
    'afin': {'cifrar': CifrarAfin, 'descifrar': DescifrarAfin},
    'adfgvx': {'cifrar': CifrarAdfgvx, 'descifrar': DescifrarAdfgvx},
    'playfair': {'cifrar': CifrarPlayfair, 'descifrar': DescifrarPlayfair},
    'hill': {'cifrar': CifrarHill, 'descifrar': DescifrarHill},
    'vernam': {'cifrar': CifrarVernam, 'descifrar': DescifrarVernam},
    'vigenere': {'cifrar': CifrarVigenere, 'descifrar': DescifrarVigenere},
    'atbash': {'cifrar': CifrarAtbash, 'descifrar': DescifrarAtbash},
    'transposicionColumna': {'cifrar': CifrarTransposicionColumna, 'descifrar': DescifrarTransposicionColumna},
    'transposicionFilas': {'cifrar': CifrarTransposicionFilas, 'descifrar': DescifrarTransposicionFilas},
    'transposicionRail': {'cifrar': CifrarRailFence, 'descifrar': DescifrarRailFence}
}

@app.route('/')
def PaginaPrincipal():
    return render_template('index.html')

@app.route('/procesar', methods=['POST'])
def ProcesarTexto():
    try:
        datos = request.get_json()
        cifrador = datos.get('cifrador')
        operacion = datos.get('operacion')
        texto = datos.get('texto')
        parametros = datos.get('parametros', {})

        if not cifrador or not operacion or not texto:
            return jsonify({'error': 'Faltan parámetros requeridos'}), 400

        if cifrador not in CIFRADORES:
            return jsonify({'error': 'Cifrador no válido'}), 400

        funcion = CIFRADORES[cifrador]['cifrar' if operacion == 'cifrar' else 'descifrar']

        # Procesar parámetros según el tipo de cifrador
        if cifrador == 'cesar':
            resultado = funcion(texto, int(parametros['desplazamiento']))
        elif cifrador == 'afin':
            resultado = funcion(texto, int(parametros['a']), int(parametros['b']))
        elif cifrador in ['adfgvx', 'playfair', 'vigenere', 'transposicionColumna']:
            resultado = funcion(texto, parametros['clave'])
        elif cifrador == 'hill':
            # Convertir la matriz de texto a lista de números
            matriz = [int(x.strip()) for x in parametros['clave'].split(',')]
            resultado = funcion(texto, matriz)
        elif cifrador == 'vernam':
            if operacion == 'cifrar':
                resultado = CifrarVernam(texto)
            else:
                resultado = DescifrarVernam(texto, parametros['clave'])
        elif cifrador == 'atbash':
            resultado = funcion(texto)
        elif cifrador == 'transposicionFilas':
            resultado = funcion(texto, int(parametros['filas']))
        elif cifrador == 'transposicionRail':
            resultado = funcion(texto, int(parametros['rieles']))
        else:
            return jsonify({'error': 'Operación no soportada'}), 400

        return jsonify({'resultado': resultado})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)