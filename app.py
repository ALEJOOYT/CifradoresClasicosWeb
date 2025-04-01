from flask import Flask, render_template, request, jsonify
import json
import logging
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

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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

        logger.debug(f"Procesando: operación={operacion}, cifrador={cifrador}")
        logger.debug(f"Parámetros recibidos: {parametros}")

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
            if 'matriz' not in parametros:
                logger.error("Falta el parámetro 'matriz' para el cifrador Hill")
                return jsonify({'error': 'Se requiere la matriz para el cifrado Hill. Por favor, asegúrate de que la matriz se haya enviado correctamente.'}), 400
            
            try:
                # Intentar cargar la matriz desde el parámetro
                matriz_str = parametros['matriz']
                logger.debug(f"Matriz recibida: {matriz_str}")
                
                if not matriz_str or matriz_str.isspace():
                    logger.error("La matriz está vacía")
                    return jsonify({'error': 'La matriz no puede estar vacía. Por favor, ingresa valores numéricos en la matriz.'}), 400
                
                # Determinar si la matriz está en formato plano o como matriz anidada
                if '[' in matriz_str:
                    # Formato de matriz anidada (JSON)
                    logger.debug("Procesando matriz en formato JSON")
                    try:
                        matriz = json.loads(matriz_str)
                        logger.debug(f"Matriz parseada (JSON): {matriz}")
                    except json.JSONDecodeError as e:
                        logger.error(f"Error al decodificar JSON: {str(e)}")
                        return jsonify({'error': f'Formato de matriz JSON inválido: {str(e)}'}), 400
                else:
                    # Formato plano de valores separados por comas y punto y coma
                    logger.debug("Procesando matriz en formato 'valor1,valor2;valor3,valor4'")
                    try:
                        # Dividir las filas por punto y coma
                        filas = matriz_str.strip().split(';')
                        matriz = []
                        
                        for fila in filas:
                            # Procesar cada fila (separada por comas)
                            valores_fila = []
                            for val in fila.split(','):
                                if val.strip():
                                    try:
                                        valores_fila.append(int(val.strip()))
                                    except ValueError:
                                        logger.error(f"Valor no numérico encontrado: '{val.strip()}'")
                                        return jsonify({'error': f"El valor '{val.strip()}' no es un número válido. Todos los elementos de la matriz deben ser números enteros."}), 400
                            matriz.append(valores_fila)
                        
                        logger.debug(f"Matriz procesada: {matriz}")
                        
                        # Verificar que la matriz no esté vacía
                        if not matriz:
                            logger.error("La matriz está vacía después del procesamiento")
                            return jsonify({'error': 'La matriz no puede estar vacía. Por favor, ingresa valores numéricos.'}), 400
                        
                        # Verificar si la matriz es cuadrada
                        num_filas = len(matriz)
                        if num_filas < 2:
                            logger.error("La matriz debe tener al menos 2 filas")
                            return jsonify({'error': 'La matriz debe tener al menos 2 filas para el cifrado Hill.'}), 400
                        
                        # Verificar que todas las filas tengan la misma longitud
                        longitud_esperada = len(matriz[0])
                        if longitud_esperada < 2:
                            logger.error("Cada fila debe tener al menos 2 columnas")
                            return jsonify({'error': 'Cada fila de la matriz debe tener al menos 2 columnas.'}), 400
                        
                        # Verificar que todas las filas tengan la misma longitud
                        for i, fila in enumerate(matriz):
                            if len(fila) != longitud_esperada:
                                logger.error(f"La fila {i+1} tiene una longitud diferente ({len(fila)}) a la esperada ({longitud_esperada})")
                                return jsonify({'error': f'La matriz debe ser cuadrada. La fila {i+1} tiene {len(fila)} elementos pero se esperaban {longitud_esperada}.'}), 400
                        
                        # Verificar que la matriz sea cuadrada
                        if num_filas != longitud_esperada:
                            logger.error(f"La matriz no es cuadrada: {num_filas} filas x {longitud_esperada} columnas")
                            return jsonify({'error': f'La matriz debe ser cuadrada. Actualmente tiene {num_filas} filas y {longitud_esperada} columnas.'}), 400
                        
                        logger.debug(f"Matriz cuadrada validada: {matriz}")
                    except Exception as e:
                        logger.error(f"Error al procesar los valores de la matriz: {str(e)}")
                        return jsonify({'error': f'Error al procesar los valores de la matriz: {str(e)}'}), 400
                
                # Validar que la matriz sea cuadrada
                # Estas validaciones ya se realizaron en el procesamiento anterior
                if not matriz:
                    logger.error("La matriz está vacía después del procesamiento")
                    return jsonify({'error': 'La matriz no puede estar vacía después del procesamiento.'}), 400
                
                logger.debug(f"Procesando con matriz: {matriz}")
                resultado = funcion(texto, matriz)
                logger.debug(f"Resultado obtenido: {resultado}")
                
            except ValueError as e:
                logger.error(f"Error de valor en la matriz: {str(e)}")
                return jsonify({'error': f'Formato de matriz inválido: {str(e)}. Asegúrate de que todos los valores sean números enteros.'}), 400
            except Exception as e:
                logger.error(f"Error inesperado al procesar la matriz: {str(e)}")
                return jsonify({'error': f'Error al procesar la matriz: {str(e)}. Por favor, verifica el formato de la matriz.'}), 400
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
        parametros = datos.get('parametros', {})

        if not cifrador or not operacion:
            return jsonify({'error': 'Faltan parámetros requeridos'}), 400

        if cifrador == 'hill':
            if operacion == 'generarMatriz':
                # Get the size parameter, default to 3 if not provided
                tamano = datos.get('tamano', 3)
                logger.debug(f"Generando matriz aleatoria de tamaño: {tamano}")
                try:
                    tamano = int(tamano)
                    if tamano < 2:
                        logger.error(f"Tamaño de matriz inválido: {tamano}")
                        return jsonify({'error': 'El tamaño de la matriz debe ser al menos 2x2'}), 400
                    if tamano > 10:
                        logger.warning(f"Tamaño de matriz grande: {tamano}")
                        return jsonify({'error': 'Para un mejor rendimiento, el tamaño máximo recomendado es 10x10'}), 400
                    matriz = GenerarMatrizAleatoria(tamano)
                    logger.debug(f"Matriz generada: {matriz}")
                    return jsonify({'resultado': matriz})
                except ValueError:
                    logger.error(f"Valor no numérico para tamaño: {tamano}")
                    return jsonify({'error': 'El tamaño de la matriz debe ser un número entero'}), 400
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
            # Si hay palabras clave proporcionadas, procesarlas
            palabras_clave = parametros.get('palabrasClave', None)
            if palabras_clave:
                # Si es una cadena, convertirla a lista
                if isinstance(palabras_clave, str):
                    palabras_clave = [p.strip() for p in palabras_clave.split(',')]
                # Si ya es una lista, asegurarse de que cada elemento sea una cadena
                elif isinstance(palabras_clave, list):
                    palabras_clave = [str(p).strip() for p in palabras_clave if p]
                else:
                    return jsonify({'error': 'Formato inválido para palabras clave'}), 400
            
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
