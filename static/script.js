// Funciones para el CifradorClassicosWeb
document.addEventListener('DOMContentLoaded', function () {
    // Asignar eventos a los botones
    document.getElementById('botonCifrar').addEventListener('click', manejarCifrado);
    document.getElementById('botonDescifrar').addEventListener('click', manejarDescifrado);
    document.getElementById('botonFuerzaBruta').addEventListener('click', manejarFuerzaBruta);

    // Asignar evento al selector de cifrado
    document.getElementById('tipoCifrado').addEventListener('change', function () {
        mostrarFormulariosCifrado();
    });

    // Asignar eventos a los botones de generar matriz aleatoria
    document.getElementById('generarMatrizAdfgvx').addEventListener('click', function () {
        generarMatrizAleatoria('matrizAdfgvxCifrado');
    });

    document.getElementById('generarMatrizAdfgvxDescifrado').addEventListener('click', function () {
        generarMatrizAleatoria('matrizAdfgvxDescifrado');
    });

    // Mostrar los formularios correctos al cargar la página
    mostrarFormulariosCifrado();
});

// Función para mostrar/ocultar elementos según el tipo de cifrado seleccionado
function mostrarFormulariosCifrado() {
    const tipoCifrado = document.getElementById('tipoCifrado').value;
    const elementosAfin = document.querySelectorAll('.solo-afin');
    const elementosAdfgvx = document.querySelectorAll('.solo-adfgvx');
    const elementosPlayFair = document.querySelectorAll('.solo-playFair');
    const elementosCesar = document.querySelectorAll('.solo-cesar');
    const elementosHill = document.querySelectorAll('.solo-hill');
    const elementosVernam = document.querySelectorAll('.solo-vernam');
    const elementosVigenere = document.querySelectorAll('.solo-vigenere');

    if (tipoCifrado === 'afin') {
        elementosAfin.forEach(elem => elem.style.display = 'block');
        elementosAdfgvx.forEach(elem => elem.style.display = 'none');
        elementosPlayFair.forEach(elem => elem.style.display = 'none');
        elementosCesar.forEach(elem => elem.style.display = 'none');
        elementosPlayFair.forEach(elem => elem.style.display = 'none');
        elementosCesar.forEach(elem => elem.style.display = 'none');
        elementosHill.forEach(elem => elem.style.display = 'none');
        elementosVernam.forEach(elem => elem.style.display = 'none');
        elementosAdfgvx.forEach(elem => elem.style.display = 'block');
        elementosPlayFair.forEach(elem => elem.style.display = 'none');
        elementosCesar.forEach(elem => elem.style.display = 'none');
        elementosHill.forEach(elem => elem.style.display = 'none');
        elementosVernam.forEach(elem => elem.style.display = 'none');
    } else if (tipoCifrado === 'playFair') {
        elementosAfin.forEach(elem => elem.style.display = 'none');
        elementosAdfgvx.forEach(elem => elem.style.display = 'none');
        elementosPlayFair.forEach(elem => elem.style.display = 'block');
        elementosCesar.forEach(elem => elem.style.display = 'none');
        elementosHill.forEach(elem => elem.style.display = 'none');
        elementosVernam.forEach(elem => elem.style.display = 'none');
    } else if (tipoCifrado === 'hill') {
        elementosAfin.forEach(elem => elem.style.display = 'none');
        elementosAdfgvx.forEach(elem => elem.style.display = 'none');
        elementosPlayFair.forEach(elem => elem.style.display = 'none');
        elementosCesar.forEach(elem => elem.style.display = 'none');
        elementosHill.forEach(elem => elem.style.display = 'block');
        elementosVernam.forEach(elem => elem.style.display = 'none');
    } else if (tipoCifrado === 'cesar') {
        elementosAfin.forEach(elem => elem.style.display = 'none');
        elementosAdfgvx.forEach(elem => elem.style.display = 'none');
        elementosPlayFair.forEach(elem => elem.style.display = 'none');
        elementosCesar.forEach(elem => elem.style.display = 'block');
        elementosHill.forEach(elem => elem.style.display = 'none');
        elementosVernam.forEach(elem => elem.style.display = 'none');
    } else if (tipoCifrado === 'vernam') {
        elementosAfin.forEach(elem => elem.style.display = 'none');
        elementosAdfgvx.forEach(elem => elem.style.display = 'none');
        elementosPlayFair.forEach(elem => elem.style.display = 'none');
        elementosCesar.forEach(elem => elem.style.display = 'none');
        elementosHill.forEach(elem => elem.style.display = 'none');
        elementosVernam.forEach(elem => elem.style.display = 'block');
        elementosVigenere.forEach(elem => elem.style.display = 'none');
    } else if (tipoCifrado === 'vigenere') {
        elementosAfin.forEach(elem => elem.style.display = 'none');
        elementosAdfgvx.forEach(elem => elem.style.display = 'none');
        elementosPlayFair.forEach(elem => elem.style.display = 'none');
        elementosCesar.forEach(elem => elem.style.display = 'none');
        elementosHill.forEach(elem => elem.style.display = 'none');
        elementosVernam.forEach(elem => elem.style.display = 'none');
        elementosVigenere.forEach(elem => elem.style.display = 'block');
    }
}

// Función para manejar el cifrado
function manejarCifrado(evento) {
    // Ya no necesitamos preventDefault ya que estamos usando botones, no envío de formularios

    const tipoCifrado = document.getElementById('tipoCifrado').value;

    if (tipoCifrado === 'afin') {
        manejarCifradoAfin();
    } else if (tipoCifrado === 'adfgvx') {
        manejarCifradoAdfgvx();
    } else if (tipoCifrado === 'playFair') {
        manejarCifradoPlayFair();
    } else if (tipoCifrado === 'cesar') {
        manejarCifradoCesar();
    } else if (tipoCifrado === 'hill') {
        manejarCifradoHill();
    } else if (tipoCifrado === 'vernam') {
        manejarCifradoVernam();
    } else if (tipoCifrado === 'vigenere') {
        manejarCifradoVigenere();
    } else if (tipoCifrado === 'transposicionColumna') {
        manejarCifradoTransposicionColumna();
    }
}

// Función para manejar el cifrado Afín
function manejarCifradoAfin() {
    const textoPlano = document.getElementById('textoPlano').value;
    const valorA = document.getElementById('valorACifrado').value;
    const valorB = document.getElementById('valorBCifrado').value;

    // Validar los campos
    if (!textoPlano || !valorA || !valorB) {
        mostrarError('errorCifrado', 'Por favor, complete todos los campos');
        return;
    }

    // Mostrar indicador de carga
    document.getElementById('cargandoCifrado').classList.add('mostrar');
    document.getElementById('resultadoCifrado').textContent = '';
    document.getElementById('errorCifrado').textContent = '';

    // Realizar la petición al backend
    fetch('/api/cifrar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            texto: textoPlano,
            a: valorA,
            b: valorB
        })
    })
        .then(respuesta => respuesta.json())
        .then(datos => {
            document.getElementById('cargandoCifrado').classList.remove('mostrar');
            if (datos.error) {
                mostrarError('errorCifrado', datos.error);
            } else {
                document.getElementById('resultadoCifrado').textContent = datos.resultado;
            }
        })
        .catch(error => {
            document.getElementById('cargandoCifrado').classList.remove('mostrar');
            mostrarError('errorCifrado', 'Error al comunicarse con el servidor: ' + error.message);
        });
}

// Función para manejar el cifrado ADFGVX
function manejarCifradoAdfgvx() {
    const textoPlano = document.getElementById('textoPlanoAdfgvx').value;
    const matriz = document.getElementById('matrizAdfgvxCifrado').value;
    const clave = document.getElementById('claveAdfgvxCifrado').value;

    // Validar los campos
    if (!textoPlano || !matriz || !clave) {
        mostrarError('errorCifrado', 'Por favor, complete todos los campos');
        return;
    }

    // Validar la matriz
    if (matriz.length !== 36) {
        mostrarError('errorCifrado', 'La matriz debe contener exactamente 36 caracteres');
        return;
    }

    // Validar que la matriz tenga caracteres únicos
    if (new Set(matriz.split('')).size !== 36) {
        mostrarError('errorCifrado', 'La matriz debe contener 36 caracteres únicos');
        return;
    }

    // Validar que la clave no esté vacía y no tenga caracteres repetidos
    if (clave.length === 0) {
        mostrarError('errorCifrado', 'La clave de transposición no puede estar vacía');
        return;
    }

    if (new Set(clave.split('')).size !== clave.length) {
        mostrarError('errorCifrado', 'La clave de transposición no debe contener caracteres repetidos');
        return;
    }

    // Mostrar indicador de carga
    document.getElementById('cargandoCifrado').classList.add('mostrar');
    document.getElementById('resultadoCifrado').textContent = '';
    document.getElementById('errorCifrado').textContent = '';

    // Realizar la petición al backend
    fetch('/api/cifrarAdfgvx', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            texto: textoPlano,
            matriz: matriz,
            clave: clave
        })
    })
        .then(respuesta => respuesta.json())
        .then(datos => {
            document.getElementById('cargandoCifrado').classList.remove('mostrar');
            if (datos.error) {
                mostrarError('errorCifrado', datos.error);
            } else {
                document.getElementById('resultadoCifrado').textContent = datos.resultado;
            }
        })
        .catch(error => {
            document.getElementById('cargandoCifrado').classList.remove('mostrar');
            mostrarError('errorCifrado', 'Error al comunicarse con el servidor: ' + error.message);
        });
}

// Función para manejar el descifrado
function manejarDescifrado(evento) {
    // Ya no necesitamos preventDefault ya que estamos usando botones, no envío de formularios

    const tipoCifrado = document.getElementById('tipoCifrado').value;

    if (tipoCifrado === 'afin') {
        manejarDescifradoAfin();
    } else if (tipoCifrado === 'adfgvx') {
        manejarDescifradoAdfgvx();
    } else if (tipoCifrado === 'playFair') {
        manejarDescifradoPlayFair();
    } else if (tipoCifrado === 'cesar') {
        manejarDescifradoCesar();
    } else if (tipoCifrado === 'hill') {
        manejarDescifradoHill();
    } else if (tipoCifrado === 'vernam') {
        manejarDescifradoVernam();
    } else if (tipoCifrado === 'vigenere') {
        manejarDescifradoVigenere();
    } else if (tipoCifrado === 'transposicionColumna') {
        manejarDescifradoTransposicionColumna();
    }
}

// Función para manejar el descifrado Afín
function manejarDescifradoAfin() {
    const textoCifrado = document.getElementById('textoCifrado').value;
    const valorA = document.getElementById('valorADescifrado').value;
    const valorB = document.getElementById('valorBDescifrado').value;

    // Validar los campos
    if (!textoCifrado || !valorA || !valorB) {
        mostrarError('errorDescifrado', 'Por favor, complete todos los campos');
        return;
    }

    // Mostrar indicador de carga
    document.getElementById('cargandoDescifrado').classList.add('mostrar');
    document.getElementById('resultadoDescifrado').textContent = '';
    document.getElementById('errorDescifrado').textContent = '';

    // Realizar la petición al backend
    fetch('/api/descifrar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            texto: textoCifrado,
            a: valorA,
            b: valorB
        })
    })
        .then(respuesta => respuesta.json())
        .then(datos => {
            document.getElementById('cargandoDescifrado').classList.remove('mostrar');
            if (datos.error) {
                mostrarError('errorDescifrado', datos.error);
            } else {
                document.getElementById('resultadoDescifrado').textContent = datos.resultado;
            }
        })
        .catch(error => {
            document.getElementById('cargandoDescifrado').classList.remove('mostrar');
            mostrarError('errorDescifrado', 'Error al comunicarse con el servidor: ' + error.message);
        });
}

// Función para manejar el descifrado ADFGVX
function manejarDescifradoAdfgvx() {
    const textoCifrado = document.getElementById('textoCifradoAdfgvx').value;
    const matriz = document.getElementById('matrizAdfgvxDescifrado').value;
    const clave = document.getElementById('claveAdfgvxDescifrado').value;

    // Validar los campos
    if (!textoCifrado || !matriz || !clave) {
        mostrarError('errorDescifrado', 'Por favor, complete todos los campos');
        return;
    }

    // Validar la matriz
    if (matriz.length !== 36) {
        mostrarError('errorDescifrado', 'La matriz debe contener exactamente 36 caracteres');
        return;
    }

    // Validar que la matriz tenga caracteres únicos
    if (new Set(matriz.split('')).size !== 36) {
        mostrarError('errorDescifrado', 'La matriz debe contener 36 caracteres únicos');
        return;
    }

    // Validar que la clave no esté vacía y no tenga caracteres repetidos
    if (clave.length === 0) {
        mostrarError('errorDescifrado', 'La clave de transposición no puede estar vacía');
        return;
    }

    if (new Set(clave.split('')).size !== clave.length) {
        mostrarError('errorDescifrado', 'La clave de transposición no debe contener caracteres repetidos');
        return;
    }

    // Validar que el texto cifrado solo contenga los caracteres A, D, F, G, V, X
    const adfgvxRegex = /^[ADFGVX]+$/i;
    if (!adfgvxRegex.test(textoCifrado)) {
        mostrarError('errorDescifrado', 'El texto cifrado ADFGVX solo debe contener los caracteres A, D, F, G, V y X');
        return;
    }

    // Mostrar indicador de carga
    document.getElementById('cargandoDescifrado').classList.add('mostrar');
    document.getElementById('resultadoDescifrado').textContent = '';
    document.getElementById('errorDescifrado').textContent = '';

    // Realizar la petición al backend
    fetch('/api/descifrarAdfgvx', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            texto: textoCifrado,
            matriz: matriz,
            clave: clave
        })
    })
        .then(respuesta => respuesta.json())
        .then(datos => {
            document.getElementById('cargandoDescifrado').classList.remove('mostrar');
            if (datos.error) {
                mostrarError('errorDescifrado', datos.error);
            } else {
                document.getElementById('resultadoDescifrado').textContent = datos.resultado;
            }
        })
        .catch(error => {
            document.getElementById('cargandoDescifrado').classList.remove('mostrar');
            mostrarError('errorDescifrado', 'Error al comunicarse con el servidor: ' + error.message);
        });
}

// Función para manejar el descifrado por fuerza bruta (para Afín y PlayFair)
function manejarFuerzaBruta() {
    const tipoCifrado = document.getElementById('tipoCifrado').value;

    if (tipoCifrado === 'afin') {
        manejarFuerzaBrutaAfin();
    } else if (tipoCifrado === 'playFair') {
        manejarFuerzaBrutaPlayFair();
    } else if (tipoCifrado === 'cesar') {
        manejarFuerzaBrutaCesar();
    } else if (tipoCifrado === 'hill') {
        manejarFuerzaBrutaHill();
    } else if (tipoCifrado === 'vigenere') {
        manejarFuerzaBrutaVigenere();
    } else if (tipoCifrado === 'transposicionColumna') {
        manejarFuerzaBrutaTransposicionColumna();
    }
}

// Función para manejar el descifrado por fuerza bruta para Afín
function manejarFuerzaBrutaAfin() {
    const textoCifrado = document.getElementById('textoFuerzaBruta').value;

    // Validar que se haya ingresado texto
    if (!textoCifrado) {
        mostrarError('errorFuerzaBruta', 'Por favor, ingrese el texto cifrado');
        return;
    }

    // Mostrar indicador de carga
    document.getElementById('cargandoFuerzaBruta').classList.add('mostrar');
    document.getElementById('resultadoFuerzaBruta').innerHTML = '';
    document.getElementById('errorFuerzaBruta').textContent = '';

    // Realizar la petición al backend
    fetch('/api/fuerzaBruta', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            texto: textoCifrado
        })
    })
        .then(respuesta => respuesta.json())
        .then(datos => {
            document.getElementById('cargandoFuerzaBruta').classList.remove('mostrar');
            if (datos.error) {
                mostrarError('errorFuerzaBruta', datos.error);
            } else {
                mostrarResultadosFuerzaBruta(datos.resultados);
            }
        })
        .catch(error => {
            document.getElementById('cargandoFuerzaBruta').classList.remove('mostrar');
            mostrarError('errorFuerzaBruta', 'Error al comunicarse con el servidor: ' + error.message);
        });
}

// Función para mostrar los resultados del descifrado por fuerza bruta
function mostrarResultadosFuerzaBruta(resultados) {
    const contenedor = document.getElementById('resultadoFuerzaBruta');

    if (!resultados || resultados.length === 0) {
        contenedor.innerHTML = '<p>No se encontraron posibles descifraciones.</p>';
        return;
    }

    let html = '<ul class="listaResultados">';

    resultados.forEach(item => {
        html += `<li>
            <strong>A = ${item.a}, B = ${item.b}</strong>
            <p>${item.textoDescifrado || item.texto}</p>
        </li>`;
    });

    html += '</ul>';
    contenedor.innerHTML = html;
}

// Función para mostrar mensajes de error
function mostrarError(elementoId, mensaje) {
    const elementoError = document.getElementById(elementoId);
    elementoError.textContent = mensaje;
    elementoError.classList.add('mostrar');

    // Ocultar el mensaje después de 5 segundos
    setTimeout(() => {
        elementoError.classList.remove('mostrar');
    }, 5000);
}

// Función para limpiar formularios
function limpiarFormulario(formularioId) {
    document.getElementById(formularioId).reset();

    // Determinar los elementos a limpiar según el formulario
    let errorId, resultadoId;

    switch (formularioId) {
        case 'formCifrado':
            errorId = 'errorCifrado';
            resultadoId = 'resultadoCifrado';
            break;
        case 'formDescifrado':
            errorId = 'errorDescifrado';
            resultadoId = 'resultadoDescifrado';
            break;
        case 'formFuerzaBruta':
            errorId = 'errorFuerzaBruta';
            resultadoId = 'resultadoFuerzaBruta';
            break;
    }

    // Limpiar mensajes y resultados
    document.getElementById(errorId).textContent = '';

    if (formularioId === 'formFuerzaBruta') {
        document.getElementById(resultadoId).innerHTML = '';
    } else {
        document.getElementById(resultadoId).textContent = '';
    }

}

// Función para generar una matriz aleatoria para el cifrado ADFGVX
function generarMatrizAleatoria(elementId) {
    // Mostrar indicador de carga
    const seccion = elementId === 'matrizAdfgvxCifrado' ? 'Cifrado' : 'Descifrado';
    document.getElementById('cargando' + seccion).classList.add('mostrar');
    document.getElementById('error' + seccion).textContent = '';

    // Realizar la petición al backend
    fetch('/api/generarMatrizAdfgvx', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(respuesta => respuesta.json())
        .then(datos => {
            document.getElementById('cargando' + seccion).classList.remove('mostrar');
            if (datos.error) {
                mostrarError('error' + seccion, datos.error);
            } else {
                document.getElementById(elementId).value = datos.matriz;
            }
        })
        .catch(error => {
            document.getElementById('cargando' + seccion).classList.remove('mostrar');
            mostrarError('error' + seccion, 'Error al generar matriz: ' + error.message);
        });
}
// Función para manejar el cifrado PlayFair
function manejarCifradoPlayFair() {
    const textoPlano = document.getElementById('textoPlanoPlayFair').value;
    const clave = document.getElementById('clavePlayFairCifrado').value;

    // Validar los campos
    if (!textoPlano || !clave) {
        mostrarError('errorCifrado', 'Por favor, complete todos los campos');
        return;
    }

    // Mostrar indicador de carga
    document.getElementById('cargandoCifrado').classList.add('mostrar');
    document.getElementById('resultadoCifrado').textContent = '';
    document.getElementById('errorCifrado').textContent = '';

    // Realizar la petición al backend
    fetch('/api/cifrarPlayFair', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            texto: textoPlano,
            clave: clave
        })
    })
        .then(respuesta => respuesta.json())
        .then(datos => {
            document.getElementById('cargandoCifrado').classList.remove('mostrar');
            if (datos.error) {
                mostrarError('errorCifrado', datos.error);
            } else {
                document.getElementById('resultadoCifrado').textContent = datos.resultado;
            }
        })
        .catch(error => {
            document.getElementById('cargandoCifrado').classList.remove('mostrar');
            mostrarError('errorCifrado', 'Error al comunicarse con el servidor: ' + error.message);
        });
}

// Función para manejar el descifrado PlayFair
function manejarDescifradoPlayFair() {
    const textoCifrado = document.getElementById('textoCifradoPlayFair').value;
    const clave = document.getElementById('clavePlayFairDescifrado').value;

    // Validar los campos
    if (!textoCifrado || !clave) {
        mostrarError('errorDescifrado', 'Por favor, complete todos los campos');
        return;
    }

    // Mostrar indicador de carga
    document.getElementById('cargandoDescifrado').classList.add('mostrar');
    document.getElementById('resultadoDescifrado').textContent = '';
    document.getElementById('errorDescifrado').textContent = '';

    // Realizar la petición al backend
    fetch('/api/descifrarPlayFair', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            texto: textoCifrado,
            clave: clave
        })
    })
        .then(respuesta => respuesta.json())
        .then(datos => {
            document.getElementById('cargandoDescifrado').classList.remove('mostrar');
            if (datos.error) {
                mostrarError('errorDescifrado', datos.error);
            } else {
                document.getElementById('resultadoDescifrado').textContent = datos.resultado;
            }
        })
        .catch(error => {
            document.getElementById('cargandoDescifrado').classList.remove('mostrar');
            mostrarError('errorDescifrado', 'Error al comunicarse con el servidor: ' + error.message);
        });
}

// Función para manejar la fuerza bruta PlayFair
function manejarFuerzaBrutaPlayFair() {
    const textoCifrado = document.getElementById('textoFuerzaBruta').value;

    // Validar que se haya ingresado texto
    if (!textoCifrado) {
        mostrarError('errorFuerzaBruta', 'Por favor, ingrese el texto cifrado');
        return;
    }

    // Mostrar indicador de carga
    document.getElementById('cargandoFuerzaBruta').classList.add('mostrar');
    document.getElementById('resultadoFuerzaBruta').innerHTML = '';
    document.getElementById('errorFuerzaBruta').textContent = '';

    // Realizar la petición al backend
    fetch('/api/fuerzaBrutaPlayFair', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            texto: textoCifrado
        })
    })
        .then(respuesta => respuesta.json())
        .then(datos => {
            document.getElementById('cargandoFuerzaBruta').classList.remove('mostrar');
            if (datos.error) {
                mostrarError('errorFuerzaBruta', datos.error);
            } else {
                mostrarResultadosFuerzaBrutaPlayFair(datos.resultados);
            }
        })
        .catch(error => {
            document.getElementById('cargandoFuerzaBruta').classList.remove('mostrar');
            mostrarError('errorFuerzaBruta', 'Error al comunicarse con el servidor: ' + error.message);
        });
}

// Función para mostrar los resultados del descifrado por fuerza bruta PlayFair
function mostrarResultadosFuerzaBrutaPlayFair(resultados) {
    const contenedor = document.getElementById('resultadoFuerzaBruta');

    if (!resultados || resultados.length === 0) {
        contenedor.innerHTML = '<p>No se encontraron posibles descifraciones.</p>';
        return;
    }

    let html = '<ul class="listaResultados">';

    resultados.forEach(item => {
        html += `<li>
            <strong>Clave: ${item.clave}</strong>
            <p>${item.textoDescifrado || item.texto}</p>
        </li>`;
    });

    html += '</ul>';
    contenedor.innerHTML = html;
}

// Función para manejar el cifrado César
function manejarCifradoCesar() {
    const textoPlano = document.getElementById('textoPlanoCesar').value;
    const desplazamiento = document.getElementById('desplazamientoCifrado').value;

    // Validar los campos
    if (!textoPlano || !desplazamiento) {
        mostrarError('errorCifrado', 'Por favor, complete todos los campos');
        return;
    }

    // Mostrar indicador de carga
    document.getElementById('cargandoCifrado').classList.add('mostrar');
    document.getElementById('resultadoCifrado').textContent = '';
    document.getElementById('errorCifrado').textContent = '';

    // Realizar la petición al backend
    fetch('/api/cifrarCesar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            texto: textoPlano,
            desplazamiento: desplazamiento
        })
    })
        .then(respuesta => respuesta.json())
        .then(datos => {
            document.getElementById('cargandoCifrado').classList.remove('mostrar');
            if (datos.error) {
                mostrarError('errorCifrado', datos.error);
            } else {
                document.getElementById('resultadoCifrado').textContent = datos.resultado;
            }
        })
        .catch(error => {
            document.getElementById('cargandoCifrado').classList.remove('mostrar');
            mostrarError('errorCifrado', 'Error al comunicarse con el servidor: ' + error.message);
        });
}

// Función para manejar el descifrado César
function manejarDescifradoCesar() {
    const textoCifrado = document.getElementById('textoCifradoCesar').value;
    const desplazamiento = document.getElementById('desplazamientoDescifrado').value;

    // Validar los campos
    if (!textoCifrado || !desplazamiento) {
        mostrarError('errorDescifrado', 'Por favor, complete todos los campos');
        return;
    }

    // Mostrar indicador de carga
    document.getElementById('cargandoDescifrado').classList.add('mostrar');
    document.getElementById('resultadoDescifrado').textContent = '';
    document.getElementById('errorDescifrado').textContent = '';

    // Realizar la petición al backend
    fetch('/api/descifrarCesar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            texto: textoCifrado,
            desplazamiento: desplazamiento
        })
    })
        .then(respuesta => respuesta.json())
        .then(datos => {
            document.getElementById('cargandoDescifrado').classList.remove('mostrar');
            if (datos.error) {
                mostrarError('errorDescifrado', datos.error);
            } else {
                document.getElementById('resultadoDescifrado').textContent = datos.resultado;
            }
        })
        .catch(error => {
            document.getElementById('cargandoDescifrado').classList.remove('mostrar');
            mostrarError('errorDescifrado', 'Error al comunicarse con el servidor: ' + error.message);
        });
}

// Función para manejar el descifrado por fuerza bruta César
function manejarFuerzaBrutaCesar() {
    const textoCifrado = document.getElementById('textoFuerzaBruta').value;

    // Validar que se haya ingresado texto
    if (!textoCifrado) {
        mostrarError('errorFuerzaBruta', 'Por favor, ingrese el texto cifrado');
        return;
    }

    // Mostrar indicador de carga
    document.getElementById('cargandoFuerzaBruta').classList.add('mostrar');
    document.getElementById('resultadoFuerzaBruta').innerHTML = '';
    document.getElementById('errorFuerzaBruta').textContent = '';

    // Realizar la petición al backend
    fetch('/api/fuerzaBrutaCesar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            texto: textoCifrado
        })
    })
        .then(respuesta => respuesta.json())
        .then(datos => {
            document.getElementById('cargandoFuerzaBruta').classList.remove('mostrar');
            if (datos.error) {
                mostrarError('errorFuerzaBruta', datos.error);
            } else {
                mostrarResultadosFuerzaBrutaCesar(datos.resultados);
            }
        })
        .catch(error => {
            document.getElementById('cargandoFuerzaBruta').classList.remove('mostrar');
            mostrarError('errorFuerzaBruta', 'Error al comunicarse con el servidor: ' + error.message);
        });
}

// Función para mostrar los resultados del descifrado por fuerza bruta César
function mostrarResultadosFuerzaBrutaCesar(resultados) {
    const contenedor = document.getElementById('resultadoFuerzaBruta');

    if (!resultados || resultados.length === 0) {
        contenedor.innerHTML = '<p>No se encontraron posibles descifraciones.</p>';
        return;
    }

    let html = '<ul class="listaResultados">';

    resultados.forEach(item => {
        // Extraer desplazamiento y texto descifrado de la tupla
        // La tupla viene como [desplazamiento, textoDescifrado]
        const desplazamiento = item[0];
        const textoDescifrado = item[1];
        
        html += `<li>
            <strong>Desplazamiento = ${desplazamiento}</strong>
            <p>${textoDescifrado}</p>
        </li>`;
    });

    html += '</ul>';
    contenedor.innerHTML = html;
}

// Función para manejar el cifrado Hill
function manejarCifradoHill() {
    const textoPlano = document.getElementById('textoPlanoHill').value;
    const matriz = document.getElementById('matrizHillCifrado').value;

    // Validar los campos
    if (!textoPlano || !matriz) {
        mostrarError('errorCifrado', 'Por favor, complete todos los campos');
        return;
    }

    // Mostrar indicador de carga
    document.getElementById('cargandoCifrado').classList.add('mostrar');
    document.getElementById('resultadoCifrado').textContent = '';
    document.getElementById('errorCifrado').textContent = '';

    // Realizar la petición al backend
    fetch('/api/cifrarHill', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            texto: textoPlano,
            clave: matriz
        })
    })
        .then(respuesta => respuesta.json())
        .then(datos => {
            document.getElementById('cargandoCifrado').classList.remove('mostrar');
            if (datos.error) {
                mostrarError('errorCifrado', datos.error);
            } else {
                document.getElementById('resultadoCifrado').textContent = datos.resultado;
            }
        })
        .catch(error => {
            document.getElementById('cargandoCifrado').classList.remove('mostrar');
            mostrarError('errorCifrado', 'Error al comunicarse con el servidor: ' + error.message);
        });
}

// Función para manejar el descifrado Hill
function manejarDescifradoHill() {
    const textoCifrado = document.getElementById('textoCifradoHill').value;
    const matriz = document.getElementById('matrizHillDescifrado').value;

    // Validar los campos
    if (!textoCifrado || !matriz) {
        mostrarError('errorDescifrado', 'Por favor, complete todos los campos');
        return;
    }

    // Mostrar indicador de carga
    document.getElementById('cargandoDescifrado').classList.add('mostrar');
    document.getElementById('resultadoDescifrado').textContent = '';
    document.getElementById('errorDescifrado').textContent = '';

    // Realizar la petición al backend
    fetch('/api/descifrarHill', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            texto: textoCifrado,
            clave: matriz
        })
    })
        .then(respuesta => respuesta.json())
        .then(datos => {
            document.getElementById('cargandoDescifrado').classList.remove('mostrar');
            if (datos.error) {
                mostrarError('errorDescifrado', datos.error);
            } else {
                document.getElementById('resultadoDescifrado').textContent = datos.resultado;
            }
        })
        .catch(error => {
            document.getElementById('cargandoDescifrado').classList.remove('mostrar');
            mostrarError('errorDescifrado', 'Error al comunicarse con el servidor: ' + error.message);
        });
}

// Función para manejar el descifrado por fuerza bruta Hill
function manejarFuerzaBrutaHill() {
    const textoCifrado = document.getElementById('textoFuerzaBruta').value;
    const textoOriginal = document.getElementById('textoOriginalFuerzaBruta').value;
    const clave = document.getElementById('claveInicialFuerzaBruta').value;

    // Validar que se hayan ingresado los textos necesarios
    if (!textoCifrado) {
        mostrarError('errorFuerzaBruta', 'Por favor, ingrese el texto cifrado');
        return;
    }
    
    if (!textoOriginal) {
        mostrarError('errorFuerzaBruta', 'Por favor, ingrese el texto original para verificación');
        return;
    }
    
    if (!clave) {
        mostrarError('errorFuerzaBruta', 'Por favor, ingrese una matriz clave inicial');
        return;
    }

    // Mostrar indicador de carga
    document.getElementById('cargandoFuerzaBruta').classList.add('mostrar');
    document.getElementById('resultadoFuerzaBruta').innerHTML = '';
    document.getElementById('errorFuerzaBruta').textContent = '';

    // Realizar la petición al backend
    fetch('/api/fuerzaBrutaHill', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            textoCifrado: textoCifrado,
            textoOriginal: textoOriginal,
            clave: clave
        })
    })
        .then(respuesta => respuesta.json())
        .then(datos => {
            document.getElementById('cargandoFuerzaBruta').classList.remove('mostrar');
            if (datos.error) {
                mostrarError('errorFuerzaBruta', datos.error);
            } else {
                mostrarResultadosFuerzaBrutaHill(datos.resultados);
            }
        })
        .catch(error => {
            document.getElementById('cargandoFuerzaBruta').classList.remove('mostrar');
            mostrarError('errorFuerzaBruta', 'Error al comunicarse con el servidor: ' + error.message);
        });
}

// Función para mostrar los resultados del descifrado por fuerza bruta Hill
function mostrarResultadosFuerzaBrutaHill(resultados) {
    const contenedor = document.getElementById('resultadoFuerzaBruta');

    if (!resultados || resultados.length === 0) {
        contenedor.innerHTML = '<p>No se encontraron posibles descifraciones.</p>';
        return;
    }

    let html = '<ul class="listaResultados">';

    resultados.forEach(item => {
        html += `<li>
            <strong>Matriz: ${item.matriz}</strong>
            <p>${item.textoDescifrado || item.texto}</p>
        </li>`;
    });

    html += '</ul>';
    contenedor.innerHTML = html;
}

// Función para manejar el cifrado Vernam
function manejarCifradoVernam() {
    const textoPlano = document.getElementById('textoPlanoVernam').value;

    // Validar los campos
    if (!textoPlano) {
        mostrarError('errorCifrado', 'Por favor, ingrese el texto a cifrar');
        return;
    }

    // Mostrar indicador de carga
    document.getElementById('cargandoCifrado').classList.add('mostrar');
    document.getElementById('resultadoCifrado').textContent = '';
    document.getElementById('errorCifrado').textContent = '';

    // Realizar la petición al backend
    fetch('/api/cifrarVernam', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            texto: textoPlano
        })
    })
        .then(respuesta => respuesta.json())
        .then(datos => {
            document.getElementById('cargandoCifrado').classList.remove('mostrar');
            if (datos.error) {
                mostrarError('errorCifrado', datos.error);
            } else {
                // Mostrar tanto el texto cifrado como la clave
                const resultadoHTML = `<p><strong>Texto cifrado:</strong> ${datos.resultado}</p>
                <p><strong>Clave:</strong> ${datos.clave}</p>`;
                document.getElementById('resultadoCifrado').innerHTML = resultadoHTML;
            }
        })
        .catch(error => {
            document.getElementById('cargandoCifrado').classList.remove('mostrar');
            mostrarError('errorCifrado', 'Error al comunicarse con el servidor: ' + error.message);
        });
}

// Función para manejar el descifrado Vernam
function manejarDescifradoVernam() {
    const textoCifrado = document.getElementById('textoCifradoVernam').value;
    const clave = document.getElementById('claveVernamDescifrado').value;

    // Validar los campos
    if (!textoCifrado || !clave) {
        mostrarError('errorDescifrado', 'Por favor, complete todos los campos');
        return;
    }

    // Mostrar indicador de carga
    document.getElementById('cargandoDescifrado').classList.add('mostrar');
    document.getElementById('resultadoDescifrado').textContent = '';
    document.getElementById('errorDescifrado').textContent = '';

    // Realizar la petición al backend
    fetch('/api/descifrarVernam', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            texto: textoCifrado,
            clave: clave
        })
    })
        .then(respuesta => respuesta.json())
        .then(datos => {
            document.getElementById('cargandoDescifrado').classList.remove('mostrar');
            if (datos.error) {
                mostrarError('errorDescifrado', datos.error);
            } else {
                document.getElementById('resultadoDescifrado').textContent = datos.resultado;
            }
        })
        .catch(error => {
            document.getElementById('cargandoDescifrado').classList.remove('mostrar');
            mostrarError('errorDescifrado', 'Error al comunicarse con el servidor: ' + error.message);
        });
}

// Función para manejar el cifrado Vigenère
function manejarCifradoVigenere() {
    const textoPlano = document.getElementById('textoPlanoVigenere').value;
    const clave = document.getElementById('claveVigenereCifrado').value;

    // Validar los campos
    if (!textoPlano || !clave) {
        mostrarError('errorCifrado', 'Por favor, complete todos los campos');
        return;
    }

    // Mostrar indicador de carga
    document.getElementById('cargandoCifrado').classList.add('mostrar');
    document.getElementById('resultadoCifrado').textContent = '';
    document.getElementById('errorCifrado').textContent = '';

    // Realizar la petición al backend
    fetch('/api/cifrarVigenere', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            texto: textoPlano,
            clave: clave
        })
    })
        .then(respuesta => respuesta.json())
        .then(datos => {
            document.getElementById('cargandoCifrado').classList.remove('mostrar');
            if (datos.error) {
                mostrarError('errorCifrado', datos.error);
            } else {
                document.getElementById('resultadoCifrado').textContent = datos.resultado;
            }
        })
        .catch(error => {
            document.getElementById('cargandoCifrado').classList.remove('mostrar');
            mostrarError('errorCifrado', 'Error al comunicarse con el servidor: ' + error.message);
        });
}

// Función para manejar el descifrado Vigenère
function manejarDescifradoVigenere() {
    const textoCifrado = document.getElementById('textoCifradoVigenere').value;
    const clave = document.getElementById('claveVigenereDescifrado').value;

    // Validar los campos
    if (!textoCifrado || !clave) {
        mostrarError('errorDescifrado', 'Por favor, complete todos los campos');
        return;
    }

    // Mostrar indicador de carga
    document.getElementById('cargandoDescifrado').classList.add('mostrar');
    document.getElementById('resultadoDescifrado').textContent = '';
    document.getElementById('errorDescifrado').textContent = '';

    // Realizar la petición al backend
    fetch('/api/descifrarVigenere', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            texto: textoCifrado,
            clave: clave
        })
    })
        .then(respuesta => respuesta.json())
        .then(datos => {
            document.getElementById('cargandoDescifrado').classList.remove('mostrar');
            if (datos.error) {
                mostrarError('errorDescifrado', datos.error);
            } else {
                document.getElementById('resultadoDescifrado').textContent = datos.resultado;
            }
        })
        .catch(error => {
            document.getElementById('cargandoDescifrado').classList.remove('mostrar');
            mostrarError('errorDescifrado', 'Error al comunicarse con el servidor: ' + error.message);
        });
}

// Función para manejar la fuerza bruta Vigenère
function manejarFuerzaBrutaVigenere() {
    const textoCifrado = document.getElementById('textoFuerzaBruta').value;
    const maxLargo = document.getElementById('maxLargoVigenere') ? document.getElementById('maxLargoVigenere').value : '4';
    const top = document.getElementById('topResultadosVigenere') ? document.getElementById('topResultadosVigenere').value : '5';

    // Validar que se haya ingresado texto
    if (!textoCifrado) {
        mostrarError('errorFuerzaBruta', 'Por favor, ingrese el texto cifrado');
        return;
    }

    // Mostrar indicador de carga
    document.getElementById('cargandoFuerzaBruta').classList.add('mostrar');
    document.getElementById('resultadoFuerzaBruta').innerHTML = '';
    document.getElementById('errorFuerzaBruta').textContent = '';

    // Realizar la petición al backend
    fetch('/api/fuerzaBrutaVigenere', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            texto: textoCifrado,
            maxLargo: maxLargo || '4',
            top: top || '5'
        })
    })
        .then(respuesta => respuesta.json())
        .then(datos => {
            document.getElementById('cargandoFuerzaBruta').classList.remove('mostrar');
            if (datos.error) {
                mostrarError('errorFuerzaBruta', datos.error);
            } else {
                mostrarResultadosFuerzaBrutaVigenere(datos.resultados);
            }
        })
        .catch(error => {
            document.getElementById('cargandoFuerzaBruta').classList.remove('mostrar');
            mostrarError('errorFuerzaBruta', 'Error al comunicarse con el servidor: ' + error.message);
        });
}

// Función para mostrar los resultados del descifrado por fuerza bruta Vigenère
function mostrarResultadosFuerzaBrutaVigenere(resultados) {
    const contenedor = document.getElementById('resultadoFuerzaBruta');
    
    if (!resultados || resultados.length === 0) {
        contenedor.innerHTML = '<p>No se encontraron posibles descifraciones.</p>';
        return;
    }
    
    // Variables para paginación
    let resultadosTotales = resultados.length;
    let resultadosPorPagina = 50;
    let paginaActual = 1;
    let filtroMinimo = 0;
    
    // Función para actualizar la tabla con los resultados filtrados y paginados
    function actualizarTabla() {
        // Filtrar resultados por puntuación mínima
        const resultadosFiltrados = resultados.filter(item => item.puntuacion >= filtroMinimo);
        const totalFiltrados = resultadosFiltrados.length;
        
        // Calcular índices para la paginación
        const inicio = (paginaActual - 1) * resultadosPorPagina;
        const fin = Math.min(paginaActual * resultadosPorPagina, totalFiltrados);
        const resultadosMostrados = resultadosFiltrados.slice(inicio, fin);
        
        // Generar tabla
        let html = '<h4>Resultados del descifrado por fuerza bruta</h4>';
        
        // Agregar controles de filtrado
        html += `<div class="controles-tabla">
            <div class="filtro-puntuacion">
                <label for="filtroPuntuacion">Puntuación mínima:</label>
                <input type="number" id="filtroPuntuacion" min="0" value="${filtroMinimo}" />
                <button id="aplicarFiltro">Filtrar</button>
            </div>
            <div class="info-resultados">
                Mostrando ${Math.min(fin, totalFiltrados)} de ${totalFiltrados} resultados (Total: ${resultadosTotales})
            </div>
        </div>`;
        
        // Generar tabla
        html += '<div class="tabla-resultados">';
        html += '<table class="tabla-fuerza-bruta">';
        html += '<thead><tr><th>Clave</th><th>Texto descifrado</th><th>Puntuación</th></tr></thead>';
        html += '<tbody>';
        
        resultadosMostrados.forEach(item => {
            html += `<tr>
                <td><strong>${item.clave}</strong></td>
                <td>${item.textoDescifrado || item.texto}</td>
                <td>${item.puntuacion || '0'} palabras</td>
            </tr>`;
        });
        
        html += '</tbody></table></div>';
        
        // Agregar botón "Mostrar más" si hay más resultados
        if (fin < totalFiltrados) {
            html += `<div class="mostrar-mas">
                <button id="mostrarMas">Mostrar más resultados</button>
            </div>`;
        }
        
        html += '<p><small>Los resultados están ordenados por número de palabras reconocidas en el diccionario.</small></p>';
        
        // Actualizar el contenedor
        contenedor.innerHTML = html;
        
        // Agregar event listeners para los botones
        if (fin < totalFiltrados) {
            document.getElementById('mostrarMas').addEventListener('click', function() {
                paginaActual++;
                actualizarTabla();
            });
        }
        
        document.getElementById('aplicarFiltro').addEventListener('click', function() {
            filtroMinimo = parseInt(document.getElementById('filtroPuntuacion').value) || 0;
            paginaActual = 1; // Reiniciar a la primera página al filtrar
            actualizarTabla();
        });
    }
    
    // Inicializar tabla
    actualizarTabla();
}

// Función para manejar el cifrado de Transposición por Columna
function manejarCifradoTransposicionColumna() {
    const textoPlano = document.getElementById('textoPlanoTransposicionColumna').value;
    const clave = document.getElementById('claveTransposicionColumnaCifrado').value;

    // Validar los campos
    if (!textoPlano || !clave) {
        mostrarError('errorCifrado', 'Por favor, complete todos los campos');
        return;
    }

    // Mostrar indicador de carga
    document.getElementById('cargandoCifrado').classList.add('mostrar');
    document.getElementById('resultadoCifrado').textContent = '';
    document.getElementById('errorCifrado').textContent = '';

    // Realizar la petición al backend
    fetch('/api/cifrarTransposicionColumna', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            texto: textoPlano,
            clave: clave
        })
    })
        .then(respuesta => respuesta.json())
        .then(datos => {
            document.getElementById('cargandoCifrado').classList.remove('mostrar');
            if (datos.error) {
                mostrarError('errorCifrado', datos.error);
            } else {
                document.getElementById('resultadoCifrado').textContent = datos.resultado;
            }
        })
        .catch(error => {
            document.getElementById('cargandoCifrado').classList.remove('mostrar');
            mostrarError('errorCifrado', 'Error al comunicarse con el servidor: ' + error.message);
        });
}

// Función para manejar el descifrado de Transposición por Columna
function manejarDescifradoTransposicionColumna() {
    const textoCifrado = document.getElementById('textoCifradoTransposicionColumna').value;
    const clave = document.getElementById('claveTransposicionColumnaDescifrado').value;

    // Validar los campos
    if (!textoCifrado || !clave) {
        mostrarError('errorDescifrado', 'Por favor, complete todos los campos');
        return;
    }

    // Mostrar indicador de carga
    document.getElementById('cargandoDescifrado').classList.add('mostrar');
    document.getElementById('resultadoDescifrado').textContent = '';
    document.getElementById('errorDescifrado').textContent = '';

    // Realizar la petición al backend
    fetch('/api/descifrarTransposicionColumna', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            texto: textoCifrado,
            clave: clave
        })
    })
        .then(respuesta => respuesta.json())
        .then(datos => {
            document.getElementById('cargandoDescifrado').classList.remove('mostrar');
            if (datos.error) {
                mostrarError('errorDescifrado', datos.error);
            } else {
                document.getElementById('resultadoDescifrado').textContent = datos.resultado;
            }
        })
        .catch(error => {
            document.getElementById('cargandoDescifrado').classList.remove('mostrar');
            mostrarError('errorDescifrado', 'Error al comunicarse con el servidor: ' + error.message);
        });
}

// Función para manejar el descifrado por fuerza bruta de Transposición por Columna
function manejarFuerzaBrutaTransposicionColumna() {
    const textoCifrado = document.getElementById('textoFuerzaBruta').value;
    const claveInicio = document.getElementById('claveInicioTransposicionColumna').value;
    const claveFin = document.getElementById('claveFinTransposicionColumna').value;

    // Validar que se haya ingresado texto
    if (!textoCifrado) {
        mostrarError('errorFuerzaBruta', 'Por favor, ingrese el texto cifrado');
        return;
    }

    // Validar que se haya especificado el rango de claves
    if (!claveInicio || !claveFin) {
        mostrarError('errorFuerzaBruta', 'Por favor, especifique el rango de longitudes de clave (inicio y fin)');
        return;
    }

    // Validar que el rango sea válido
    if (parseInt(claveInicio) > parseInt(claveFin)) {
        mostrarError('errorFuerzaBruta', 'El valor de inicio debe ser menor o igual al valor de fin');
        return;
    }

    // Mostrar indicador de carga
    document.getElementById('cargandoFuerzaBruta').classList.add('mostrar');
    document.getElementById('resultadoFuerzaBruta').innerHTML = '';
    document.getElementById('errorFuerzaBruta').textContent = '';

    // Realizar la petición al backend
    fetch('/api/fuerzaBrutaTransposicionColumna', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            texto: textoCifrado,
            claveInicio: claveInicio,
            claveFin: claveFin
        })
    })
        .then(respuesta => respuesta.json())
        .then(datos => {
            document.getElementById('cargandoFuerzaBruta').classList.remove('mostrar');
            if (datos.error) {
                mostrarError('errorFuerzaBruta', datos.error);
            } else {
                mostrarResultadosFuerzaBrutaTransposicionColumna(datos.resultados);
            }
        })
        .catch(error => {
            document.getElementById('cargandoFuerzaBruta').classList.remove('mostrar');
            mostrarError('errorFuerzaBruta', 'Error al comunicarse con el servidor: ' + error.message);
        });
}

// Función para mostrar los resultados del descifrado por fuerza bruta de Transposición por Columna
function mostrarResultadosFuerzaBrutaTransposicionColumna(resultados) {
    const contenedor = document.getElementById('resultadoFuerzaBruta');

    if (!resultados || resultados.length === 0) {
        contenedor.innerHTML = '<p>No se encontraron posibles descifraciones.</p>';
        return;
    }

    let html = '<ul class="listaResultados">';

    resultados.forEach(item => {
        html += `<li>
            <strong>Permutación: ${item.permutacion}</strong>
            <p>${item.textoDescifrado || item.texto}</p>
        </li>`;
    });

    html += '</ul>';
    contenedor.innerHTML = html;
}