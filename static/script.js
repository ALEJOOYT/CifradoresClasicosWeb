// Funciones para el CifradorAfinWeb
document.addEventListener('DOMContentLoaded', function () {
    // Asignar eventos a los botones
    document.getElementById('botonCifrar').addEventListener('click', manejarCifrado);
    document.getElementById('botonDescifrar').addEventListener('click', manejarDescifrado);
    document.getElementById('botonFuerzaBruta').addEventListener('click', manejarFuerzaBruta);
});

// Función para manejar el cifrado
function manejarCifrado(evento) {
    // Ya no necesitamos preventDefault ya que estamos usando botones, no envío de formularios

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

// Función para manejar el descifrado
function manejarDescifrado(evento) {
    // Ya no necesitamos preventDefault ya que estamos usando botones, no envío de formularios

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

// Función para manejar el descifrado por fuerza bruta
function manejarFuerzaBruta(evento) {
    // Ya no necesitamos preventDefault ya que estamos usando botones, no envío de formularios

    const textoCifrado = document.getElementById('textoFuerzaBruta').value;

    // Validar los campos
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

