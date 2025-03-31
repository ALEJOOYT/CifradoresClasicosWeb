// Funciones para el CifradorClassicosWeb
document.addEventListener('DOMContentLoaded', function () {
    // Asignar eventos a los botones
    document.getElementById('botonCifrar').addEventListener('click', manejarCifrado);
    document.getElementById('botonDescifrar').addEventListener('click', manejarDescifrado);
    document.getElementById('botonFuerzaBruta').addEventListener('click', manejarFuerzaBruta);
    
    // Asignar evento al selector de cifrado
    document.getElementById('tipoCifrado').addEventListener('change', function() {
        mostrarFormulariosCifrado();
    });
    
    // Asignar eventos a los botones de generar matriz aleatoria
    document.getElementById('generarMatrizAdfgvx').addEventListener('click', function() {
        generarMatrizAleatoria('matrizAdfgvxCifrado');
    });
    
    document.getElementById('generarMatrizAdfgvxDescifrado').addEventListener('click', function() {
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
    const elementosPlayFair = document.querySelectorAll('.solo-playfair');
    
    if (tipoCifrado === 'afin') {
        elementosAfin.forEach(elem => elem.style.display = 'block');
        elementosAdfgvx.forEach(elem => elem.style.display = 'none');
        elementosPlayFair.forEach(elem => elem.style.display = 'none');
    } else if (tipoCifrado === 'adfgvx') {
        elementosAfin.forEach(elem => elem.style.display = 'none');
        elementosAdfgvx.forEach(elem => elem.style.display = 'block');
        elementosPlayFair.forEach(elem => elem.style.display = 'none');
    } else if (tipoCifrado === 'playFair') {
        elementosAfin.forEach(elem => elem.style.display = 'none');
        elementosAdfgvx.forEach(elem => elem.style.display = 'none');
        elementosPlayFair.forEach(elem => elem.style.display = 'block');
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
