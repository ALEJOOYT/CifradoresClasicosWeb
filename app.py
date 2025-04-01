from flask import Flask, render_template, request, jsonify
# Importar módulos de cifrado
from cifradores.afin import Cifrar as CifrarAfin
from cifradores.afin import Descifrar as DescifrarAfin
from cifradores.afin import DescifrarFuerzaBruta as DescifrarFuerzaBrutaAfin

from cifradores.adfgvx import Cifrar as CifrarAdfgvx
from cifradores.adfgvx import Descifrar as DescifrarAdfgvx
from cifradores.adfgvx import GenerarClaveAleatoria as GenerarClaveAleatoriaAdfgvx
from cifradores.adfgvx import GenerarCuadro as GenerarCuadroAdfgvx

from cifradores.playFair import Cifrar as CifrarPlayfair
from cifradores.playFair import Descifrar as DescifrarPlayfair
from cifradores.playFair import FuerzaBruta as DescifrarFuerzaBrutaPlayfair

from cifradores.cesar import Cifrar as CifrarCesar
from cifradores.cesar import Descifrar as DescifrarCesar
from cifradores.cesar import DescifrarFuerzaBruta as DescifrarFuerzaBrutaCesar

from cifradores.hill import Cifrar as CifrarHill
from cifradores.hill import Descifrar as DescifrarHill
from cifradores.hill import DescifrarFuerzaBruta as DescifrarFuerzaBrutaHill

from cifradores.vernam import CifrarVernam
from cifradores.vernam import DescifrarVernam

from cifradores.vigenere import Cifrar as CifrarVigenere
from cifradores.vigenere import Descifrar as DescifrarVigenere
from cifradores.vigenere import DescifrarFuerzaBruta as DescifrarFuerzaBrutaVigenere

from cifradores.atbah import Cifrar as CifrarAtbash
from cifradores.atbah import Descifrar as DescifrarAtbash

from cifradores.transposicionColumna import Cifrar as CifrarTransposicionColumna
from cifradores.transposicionColumna import Descifrar as DescifrarTransposicionColumna
from cifradores.transposicionColumna import DescifradoFuerzaBruta as DescifradoFuerzaBrutaTransposicionColumna

from cifradores.transposicionFilas import Cifrar as CifrarTransposicionFilas
from cifradores.transposicionFilas import Descifrar as DescifrarTransposicionFilas

from cifradores.transposicionRail import Cifrar as CifrarRailFence
from cifradores.transposicionRail import Descifrar as DescifrarRailFence
from cifradores.transposicionRail import DescifrarFuerzaBruta as DescifrarFuerzaBrutaRailFence
app = Flask(__name__)

# Ruta principal
@app.route('/')
def PaginaPrincipal():
    return render_template('index.html')


# API para cifrar Afin
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
# API para descifrar Afin
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
# API para descifrar por fuerza bruta Afin
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


# API para cifrar PlayFair
@app.route('/api/cifrarPlayFair', methods=['POST'])
def ApiCifrarPlayfair():
    datos = request.json
    texto = datos.get('texto', '')
    clave = datos.get('clave', '')
    resultado = CifrarPlayfair(texto, clave)
    return jsonify({"resultado": resultado, "exito": not resultado.startswith("Error")})
# API para Descifrar PlayFair
@app.route('/api/descifrarPlayFair', methods=['POST'])
def ApiDescifrarPlayfair():
    datos = request.json
    texto = datos.get('texto', '')
    clave = datos.get('clave', '')
    resultado = DescifrarPlayfair(texto, clave)
    return jsonify({"resultado": resultado, "exito": not resultado.startswith("Error")})
# API para Descifrar por fuerza bruta PlayFair
@app.route('/api/fuerzaBrutaPlayFair', methods=['POST'])
def ApiFuerzaBrutaPlayfair():
    datos = request.json
    texto = datos.get('texto', '')
    resultados = DescifrarFuerzaBrutaPlayfair(texto)
    return jsonify({"resultados": resultados, "exito": True})


# API para cifrar César
@app.route('/api/cifrarCesar', methods=['POST'])
def ApiCifrarCesar():
    datos = request.json
    texto = datos.get('texto', '')
    desplazamiento = int(datos.get('desplazamiento', 3))

    resultado = CifrarCesar(texto, desplazamiento)

    return jsonify({
        "resultado": resultado,
        "resultado_texto": resultado,
        "exito": not resultado.startswith("Error")
    })

# API para descifrar César
@app.route('/api/descifrarCesar', methods=['POST'])
def ApiDescifrarCesar():
    datos = request.json
    texto = datos.get('texto', '')
    desplazamiento = int(datos.get('desplazamiento', 3))

    resultado = DescifrarCesar(texto, desplazamiento)

    return jsonify({
        "resultado": resultado,
        "resultado_texto": resultado,
        "exito": not resultado.startswith("Error")
    })

# API para descifrar por fuerza bruta César
@app.route('/api/fuerzaBrutaCesar', methods=['POST'])
def ApiFuerzaBrutaCesar():
    datos = request.json
    texto = datos.get('texto', '')

    resultados = DescifrarFuerzaBrutaCesar(texto)

    return jsonify({
        "resultados": resultados,
        "listaResultados": resultados,
        "exito": True
    })


# API para cifrar Hill
@app.route('/api/cifrarHill', methods=['POST'])
def ApiCifrarHill():
    datos = request.json
    texto = datos.get('texto', '')
    claveStr = datos.get('clave', '')
    try:
        # Validar y convertir la clave de string a matriz
        filas = claveStr.strip().split('\n')
        clave = []
        for fila in filas:
            valores = [int(val) for val in fila.strip().split()]
            clave.append(valores)
        # Verificar que la matriz sea cuadrada
        if len(clave) != len(clave[0]):
            return jsonify({"resultado": "Error: La matriz debe ser cuadrada", "exito": False})
        resultado = CifrarHill(texto, clave)
        return jsonify({
            "resultado": resultado,
            "resultado_texto": resultado,
            "exito": not resultado.startswith("Error")
        })
    except Exception as e:
        return jsonify({"resultado": f"Error: {str(e)}", "exito": False})

# API para descifrar Hill
@app.route('/api/descifrarHill', methods=['POST'])
def ApiDescifrarHill():
    datos = request.json
    texto = datos.get('texto', '')
    claveStr = datos.get('clave', '')
    try:
        # Validar y convertir la clave de string a matriz
        filas = claveStr.strip().split('\n')
        clave = []
        for fila in filas:
            valores = [int(val) for val in fila.strip().split()]
            clave.append(valores)
        # Verificar que la matriz sea cuadrada
        if len(clave) != len(clave[0]):
            return jsonify({"resultado": "Error: La matriz debe ser cuadrada", "exito": False})
        resultado = DescifrarHill(texto, clave)
        return jsonify({
            "resultado": resultado,
            "resultado_texto": resultado,
            "exito": not resultado.startswith("Error")
        })
    except Exception as e:
        return jsonify({"resultado": f"Error: {str(e)}", "exito": False})

# API para descifrar por fuerza bruta Hill
@app.route('/api/fuerzaBrutaHill', methods=['POST'])
def ApiFuerzaBrutaHill():
    datos = request.json
    textoCifrado = datos.get('textoCifrado', '')
    textoOriginal = datos.get('textoOriginal', '')
    claveStr = datos.get('clave', '')
    try:
        # Validar y convertir la clave de string a matriz
        filas = claveStr.strip().split('\n')
        clave = []
        for fila in filas:
            valores = [int(val) for val in fila.strip().split()]
            clave.append(valores)
        # Verificar que la matriz sea cuadrada
        if len(clave) != len(clave[0]):
            return jsonify({"resultado": "Error: La matriz debe ser cuadrada", "exito": False})
        resultado = DescifrarFuerzaBrutaHill(textoCifrado, textoOriginal, clave)
        return jsonify({
            "resultado": resultado,
            "exito": not resultado.startswith("Error") and not resultado.startswith("No se encontró")
        })
    except Exception as e:
        return jsonify({"resultado": f"Error: {str(e)}", "exito": False})

# API para cifrar Vernam
@app.route('/api/cifrarVernam', methods=['POST'])
def ApiCifrarVernam():
    datos = request.json
    texto = datos.get('texto', '')
    try:
        textoCifrado, clave = CifrarVernam(texto)
        return jsonify({
            "resultado": textoCifrado,
            "clave": clave,
            "exito": True
        })
    except Exception as e:
        return jsonify({
            "resultado": f"Error: {str(e)}",
            "exito": False
        })

# API para descifrar Vernam
@app.route('/api/descifrarVernam', methods=['POST'])
def ApiDescifrarVernam():
    datos = request.json
    texto = datos.get('texto', '')
    clave = datos.get('clave', '')
    try:
        resultado = DescifrarVernam(texto, clave)
        return jsonify({
            "resultado": resultado,
            "exito": True
        })
    except Exception as e:
        return jsonify({
            "resultado": f"Error: {str(e)}",
            "exito": False
        })

# API para cifrar Vigenère
@app.route('/api/cifrarVigenere', methods=['POST'])
def ApiCifrarVigenere():
    datos = request.json
    texto = datos.get('texto', '')
    clave = datos.get('clave', '')
    try:
        resultado = CifrarVigenere(texto, clave)
        return jsonify({
            "resultado": resultado,
            "exito": not isinstance(resultado, str) or not resultado.startswith("Error")
        })
    except Exception as e:
        return jsonify({
            "resultado": f"Error: {str(e)}",
            "exito": False
        })

# API para descifrar Vigenère
@app.route('/api/descifrarVigenere', methods=['POST'])
def ApiDescifrarVigenere():
    datos = request.json
    texto = datos.get('texto', '')
    clave = datos.get('clave', '')
    try:
        resultado = DescifrarVigenere(texto, clave)
        return jsonify({
            "resultado": resultado,
            "exito": not isinstance(resultado, str) or not resultado.startswith("Error")
        })
    except Exception as e:
        return jsonify({
            "resultado": f"Error: {str(e)}",
            "exito": False
        })

# API para descifrar por fuerza bruta Vigenère
@app.route('/api/fuerzaBrutaVigenere', methods=['POST'])
def ApiFuerzaBrutaVigenere():
    datos = request.json
    texto = datos.get('texto', '')
    maxLargo = int(datos.get('maxLargo', 4))
    # El top ya no importa ya que estamos devolviendo todos los resultados,
    # pero lo dejamos para no romper la compatibilidad
    top = int(datos.get('top', 5))
    try:
        resultados = DescifrarFuerzaBrutaVigenere(texto, maxLargo, top)
        return jsonify({
            "resultados": resultados,
            "listaResultados": resultados,
            "exito": True
        })
    except Exception as e:
        return jsonify({
            "resultados": [],
            "listaResultados": [],
            "resultado": f"Error: {str(e)}",
            "exito": False
        })

# API para cifrar Transposición por Columna
@app.route('/api/cifrarTransposicionColumna', methods=['POST'])
def ApiCifrarTransposicionColumna():
    datos = request.json
    texto = datos.get('texto', '')
    clave = datos.get('clave', '')
    try:
        # Si la clave es un número, generar una clave alfabética secuencial
        if clave.isdigit():
            longitud = int(clave)
            # Generar una clave usando letras secuenciales (A-Z)
            clave = ''.join(chr(65 + i) for i in range(min(longitud, 26)))
        resultado = CifrarTransposicionColumna(texto, clave)
        return jsonify({
            "resultado": resultado,
            "exito": not isinstance(resultado, str) or not resultado.startswith("Error")
        })
    except Exception as e:
        return jsonify({
            "resultado": f"Error: {str(e)}",
            "exito": False
        })

# API para descifrar Transposición por Columna
@app.route('/api/descifrarTransposicionColumna', methods=['POST'])
def ApiDescifrarTransposicionColumna():
    datos = request.json
    texto = datos.get('texto', '')
    clave = datos.get('clave', '')
    try:
        # Si la clave es un número, generar una clave alfabética secuencial
        if clave.isdigit():
            longitud = int(clave)
            # Generar una clave usando letras secuenciales (A-Z)
            clave = ''.join(chr(65 + i) for i in range(min(longitud, 26)))
        resultado = DescifrarTransposicionColumna(texto, clave)
        return jsonify({
            "resultado": resultado,
            "exito": not isinstance(resultado, str) or not resultado.startswith("Error")
        })
    except Exception as e:
        return jsonify({
            "resultado": f"Error: {str(e)}",
            "exito": False
        })

# API para descifrar por fuerza bruta Transposición por Columna
@app.route('/api/fuerzaBrutaTransposicionColumna', methods=['POST'])
def ApiFuerzaBrutaTransposicionColumna():
    datos = request.json
    texto = datos.get('texto', '')
    claveInicio = int(datos.get('claveInicio', 1))
    claveFin = int(datos.get('claveFin', 3))
    if claveInicio < 1:
        return jsonify({
            "resultados": [],
            "listaResultados": [],
            "resultado": "Error: El valor de claveInicio debe ser mayor o igual a 1",
            "exito": False
        })
    if claveFin < claveInicio:
        return jsonify({
            "resultados": [],
            "listaResultados": [],
            "resultado": "Error: El valor de claveFin debe ser mayor o igual a claveInicio",
            "exito": False
        })
    try:
        resultados_totales = []
        # Iterar a través de cada longitud de clave en el rango
        for longitud in range(claveInicio, claveFin + 1):
            try:
                resultados_parciales = DescifradoFuerzaBrutaTransposicionColumna(texto, longitud)
                if resultados_parciales:
                    resultados_totales.extend(resultados_parciales)
            except Exception as e:
                # Si hay un error con una longitud específica, continuamos con las demás
                print(f"Error al procesar longitud {longitud}: {str(e)}")
                continue
        return jsonify({
            "resultados": resultados_totales,
            "listaResultados": resultados_totales,
            "exito": True
        })
    except Exception as e:
        return jsonify({
            "resultados": [],
            "listaResultados": [],
            "resultado": f"Error: {str(e)}",
            "exito": False
        })

# API para cifrar Atbash
@app.route('/api/cifrarAtbash', methods=['POST'])
def ApiCifrarAtbash():
    datos = request.json
    texto = datos.get('texto', '')
    try:
        resultado = CifrarAtbash(texto)
        return jsonify({
            "resultado": resultado,
            "exito": True
        })
    except Exception as e:
        return jsonify({
            "resultado": f"Error: {str(e)}",
            "exito": False
        })

# API para descifrar Atbash
@app.route('/api/descifrarAtbash', methods=['POST'])
def ApiDescifrarAtbash():
    datos = request.json
    texto = datos.get('texto', '')
    try:
        resultado = DescifrarAtbash(texto)
        return jsonify({
            "resultado": resultado,
            "exito": True
        })
    except Exception as e:
        return jsonify({
            "resultado": f"Error: {str(e)}",
            "exito": False
        })


# API para cifrar Rail Fence
@app.route('/api/cifrarRailFence', methods=['POST'])
def ApiCifrarRailFence():
    datos = request.json
    texto = datos.get('texto', '')
    clave = int(datos.get('clave', 2))
    
    if clave < 2:
        return jsonify({
            "resultado": "Error: La clave debe ser un número entero mayor o igual a 2",
            "exito": False
        })
        
    try:
        resultado = CifrarRailFence(texto, clave)
        return jsonify({
            "resultado": resultado,
            "exito": True
        })
    except Exception as e:
        return jsonify({
            "resultado": f"Error: {str(e)}",
            "exito": False
        })

# API para descifrar Rail Fence
@app.route('/api/descifrarRailFence', methods=['POST'])
def ApiDescifrarRailFence():
    datos = request.json
    texto = datos.get('texto', '')
    clave = int(datos.get('clave', 2))
    
    if clave < 2:
        return jsonify({
            "resultado": "Error: La clave debe ser un número entero mayor o igual a 2",
            "exito": False
        })
        
    try:
        resultado = DescifrarRailFence(texto, clave)
        return jsonify({
            "resultado": resultado,
            "exito": True
        })
    except Exception as e:
        return jsonify({
            "resultado": f"Error: {str(e)}",
            "exito": False
        })

# API para descifrar por fuerza bruta Rail Fence
@app.route('/api/fuerzaBrutaRailFence', methods=['POST'])
def ApiFuerzaBrutaRailFence():
    datos = request.json
    texto = datos.get('texto', '')
    claveInicio = int(datos.get('claveInicio', 2))
    claveFin = int(datos.get('claveFin', 10))
    
    if claveInicio < 2:
        return jsonify({
            "resultados": [],
            "listaResultados": [],
            "resultado": "Error: El valor inicial de la clave debe ser mayor o igual a 2",
            "exito": False
        })
    
    if claveFin < claveInicio:
        return jsonify({
            "resultados": [],
            "listaResultados": [],
            "resultado": "Error: El valor final de la clave debe ser mayor o igual al valor inicial",
            "exito": False
        })
        
    try:
        resultados = DescifrarFuerzaBrutaRailFence(texto, claveInicio, claveFin)
        # Transformar los resultados a un formato más amigable
        resultados_formateados = [{"rails": clave, "textoDescifrado": texto} for clave, texto in resultados]
        
        return jsonify({
            "resultados": resultados_formateados,
            "listaResultados": resultados_formateados,
            "exito": True
        })
    except Exception as e:
        return jsonify({
            "resultados": [],
            "listaResultados": [],
            "resultado": f"Error: {str(e)}",
            "exito": False
        })


# API para cifrar Transposición por Filas
@app.route('/api/cifrarTransposicionFilas', methods=['POST'])
def ApiCifrarTransposicionFilas():
    datos = request.json
    texto = datos.get('texto', '')
    clave = datos.get('clave', '')
    try:
        # Convertir la clave numérica a una cadena de caracteres
        clave_str = ''.join(chr(ord('A') + i % 26) for i in range(int(clave)))
        resultado = CifrarTransposicionFilas(texto, clave_str)
        return jsonify({
            'resultado': resultado,
            'exito': True
        })
    except Exception as e:
        return jsonify({
            'resultado': f'Error: {str(e)}',
            'exito': False
        })

# API para descifrar Transposición por Filas
@app.route('/api/descifrarTransposicionFilas', methods=['POST'])
def ApiDescifrarTransposicionFilas():
    datos = request.json
    texto = datos.get('texto', '')
    clave = datos.get('clave', '')
    try:
        # Convertir la clave numérica a una cadena de caracteres
        clave_str = ''.join(chr(ord('A') + i % 26) for i in range(int(clave)))
        resultado = DescifrarTransposicionFilas(texto, clave_str)
        return jsonify({
            'resultado': resultado,
            'exito': True
        })
    except Exception as e:
        return jsonify({
            'resultado': f'Error: {str(e)}',
            'exito': False
        })

# API para descifrar por fuerza bruta Transposición por Filas
@app.route('/api/fuerzaBrutaTransposicionFilas', methods=['POST'])
def ApiFuerzaBrutaTransposicionFilas():
    datos = request.json
    texto = datos.get('texto', '')
    claveInicio = int(datos.get('claveInicio', 2))
    claveFin = int(datos.get('claveFin', 10))
    if claveInicio < 2:
        return jsonify({
            'resultados': [],
            'listaResultados': [],
            'resultado': 'Error: El valor inicial de la clave debe ser mayor o igual a 2',
            'exito': False
        })
    if claveFin < claveInicio:
        return jsonify({
            'resultados': [],
            'listaResultados': [],
            'resultado': 'Error: El valor final de la clave debe ser mayor o igual al valor inicial',
            'exito': False
        })
    try:
        resultados = []
        # Para cada longitud de clave
        for longitud in range(claveInicio, claveFin + 1):
            # Generar una clave base con longitud 'longitud'
            clave_base = ''.join(chr(ord('A') + i % 26) for i in range(longitud))
            
            # Descifrar con esta clave
            texto_descifrado = DescifrarTransposicionFilas(texto, clave_base)
            resultados.append((str(longitud), texto_descifrado))
        
        # Transformar los resultados a un formato más amigable
        resultados_formateados = [{'permutacion': permutacion, 'texto': texto} for permutacion, texto in resultados]
        return jsonify({
            'resultados': resultados_formateados,
            'listaResultados': resultados_formateados,
            'exito': True
        })
    except Exception as e:
        return jsonify({
            'resultados': [],
            'listaResultados': [],
            'resultado': f'Error: {str(e)}',
            'exito': False
        })


if __name__ == '__main__':
    app.run(debug=True)