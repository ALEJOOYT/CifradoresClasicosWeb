document.addEventListener('DOMContentLoaded', function() {
    // Elementos DOM
    const tipoCifrador = document.getElementById('tipoCifrador');
    const parametrosCifrador = document.getElementById('parametrosCifrador');
    const btnCifrar = document.getElementById('btnCifrar');
    const btnDescifrar = document.getElementById('btnDescifrar');
    const btnFuerzaBruta = document.getElementById('btnFuerzaBruta');
    const btnLimpiar = document.getElementById('btnLimpiar');
    const textoEntrada = document.getElementById('textoEntrada');
    const textoSalida = document.getElementById('textoSalida');

    // Configuración de parámetros por cifrador
    const parametrosCifradores = {
        'cesar': {
            params: [
                { id: 'desplazamiento', label: 'Desplazamiento', type: 'number', min: 1, max: 25 }
            ],
            tieneFuerzaBruta: true
        },
        'afin': {
            params: [
                { id: 'a', label: 'Valor de a', type: 'number', min: 1 },
                { id: 'b', label: 'Valor de b', type: 'number', min: 0 }
            ],
            tieneFuerzaBruta: true
        },
        'adfgvx': {
            params: [
                { id: 'clave', label: 'Clave', type: 'text' }
            ],
            botonesExtra: [
                { id: 'btnGenerarClave', label: 'Generar Clave Aleatoria', operacion: 'generarClave' }
            ],
            tieneFuerzaBruta: false
        },
        'playfair': {
            params: [
                { id: 'clave', label: 'Clave', type: 'text' }
            ],
            tieneFuerzaBruta: true
        },
        'hill': {
            params: [
                { id: 'clave', label: 'Matriz Clave (separada por comas)', type: 'text', placeholder: 'Ej: 2,3,1,4' }
            ],
            tieneFuerzaBruta: true
        },
        'vernam': {
            params: [
                { id: 'clave', label: 'Clave (para descifrar)', type: 'text' }
            ],
            tieneFuerzaBruta: false
        },
        'vigenere': {
            params: [
                { id: 'clave', label: 'Clave', type: 'text' }
            ],
            tieneFuerzaBruta: true
        },
        'atbash': {
            params: [],
            tieneFuerzaBruta: false
        },
        'transposicionColumna': {
            params: [
                { id: 'clave', label: 'Clave', type: 'text' }
            ],
            tieneFuerzaBruta: true
        },
        'transposicionFilas': {
            params: [
                { id: 'filas', label: 'Número de Filas', type: 'number', min: 2 }
            ],
            tieneFuerzaBruta: false
        },
        'transposicionRail': {
            params: [
                { id: 'rieles', label: 'Número de Rieles', type: 'number', min: 2 }
            ],
            tieneFuerzaBruta: true
        }
    };

    // Función para actualizar los campos de parámetros y botones
    function actualizarInterfaz() {
        const cifrador = tipoCifrador.value;
        parametrosCifrador.innerHTML = '';
        
        // Ocultar/mostrar botón de fuerza bruta solo para los cifradores que lo soportan
        btnFuerzaBruta.style.display = 
            cifrador && parametrosCifradores[cifrador]?.tieneFuerzaBruta === true ? 'block' : 'none';

        if (!cifrador || !parametrosCifradores[cifrador]) return;

        // Agregar campos de parámetros
        parametrosCifradores[cifrador].params.forEach(param => {
            const div = document.createElement('div');
            div.className = 'parametroEntrada';

            const label = document.createElement('label');
            label.htmlFor = param.id;
            label.textContent = param.label;

            const input = document.createElement('input');
            input.type = param.type;
            input.id = param.id;
            input.name = param.id;

            if (param.min !== undefined) input.min = param.min;
            if (param.max !== undefined) input.max = param.max;
            if (param.placeholder) input.placeholder = param.placeholder;

            div.appendChild(label);
            div.appendChild(input);
            parametrosCifrador.appendChild(div);
        });

        // Agregar botones extra si existen
        if (parametrosCifradores[cifrador].botonesExtra) {
            const botonesDiv = document.createElement('div');
            botonesDiv.className = 'botonesExtra';

            parametrosCifradores[cifrador].botonesExtra.forEach(boton => {
                const btn = document.createElement('button');
                btn.textContent = boton.label;
                btn.className = 'boton botonExtra';
                btn.onclick = () => ejecutarOperacionEspecial(cifrador, boton.operacion);
                botonesDiv.appendChild(btn);
            });

            parametrosCifrador.appendChild(botonesDiv);
        }
    }

    // Función para obtener los valores de los parámetros
    function obtenerParametros() {
        const cifrador = tipoCifrador.value;
        const params = {};

        if (cifrador && parametrosCifradores[cifrador]) {
            parametrosCifradores[cifrador].params.forEach(param => {
                const input = document.getElementById(param.id);
                if (input) params[param.id] = input.value;
            });
        }

        return params;
    }

    // Función para procesar el texto
    async function procesarTexto(operacion) {
        const cifrador = tipoCifrador.value;
        if (!cifrador) {
            alert('Por favor seleccione un método de cifrado');
            return;
        }

        const texto = textoEntrada.value;
        if (!texto) {
            alert('Por favor ingrese un texto');
            return;
        }

        const params = obtenerParametros();

        try {
            const response = await fetch('/procesar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    cifrador: cifrador,
                    operacion: operacion,
                    texto: texto,
                    parametros: params
                })
            });

            const data = await response.json();
            if (data.error) {
                alert(data.error);
            } else {
                textoSalida.value = 
                    Array.isArray(data.resultado) ? 
                    data.resultado.map(r => `Intento ${r[0]}: ${r[1]}`).join('\n') :
                    data.resultado;
            }
        } catch (error) {
            alert('Error al procesar el texto: ' + error.message);
        }
    }

    // Función para ejecutar fuerza bruta
    async function procesarFuerzaBruta() {
        const cifrador = tipoCifrador.value;
        if (!cifrador) {
            alert('Por favor seleccione un método de cifrado');
            return;
        }

        const texto = textoEntrada.value;
        if (!texto) {
            alert('Por favor ingrese un texto');
            return;
        }

        const params = obtenerParametros();

        try {
            const response = await fetch('/fuerza_bruta', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    cifrador: cifrador,
                    texto: texto,
                    parametros: params
                })
            });

            const data = await response.json();
            if (data.error) {
                alert(data.error);
            } else {
                // Display results in a list format
                if (Array.isArray(data.resultados)) {
                    textoSalida.value = data.resultados.map((resultado, index) => {
                        let displayText = `Posible solución ${index + 1}: `;
                        
                        if (resultado.key && resultado.text) {
                            displayText += `Key: ${resultado.key}, Text: ${resultado.text}`;
                        } else if (resultado.clave && resultado.textoDescifrado) {
                            displayText += `Clave: ${resultado.clave}, Texto: ${resultado.textoDescifrado}`;
                        } else if (resultado.desplazamiento && resultado.texto) {
                            displayText += `Desplazamiento: ${resultado.desplazamiento}, Texto: ${resultado.texto}`;
                        } else if (resultado.a && resultado.b && resultado.texto) {
                            displayText += `a: ${resultado.a}, b: ${resultado.b}, Texto: ${resultado.texto}`;
                        } else if (resultado.rieles && resultado.texto) {
                            displayText += `Rieles: ${resultado.rieles}, Texto: ${resultado.texto}`;
                        } else {
                            // Try to intelligently extract key-value pairs from the object
                            const pairs = Object.entries(resultado).map(([key, value]) => `${key}: ${value}`);
                            displayText += pairs.join(', ');
                        }
                        
                        return displayText;
                    }).join('\n');
                } else {
                    textoSalida.value = data.resultados || 'No se encontraron resultados';
                }
            }
        } catch (error) {
            alert('Error al procesar fuerza bruta: ' + error.message);
        }
    }

    // Función para ejecutar operaciones especiales
    async function ejecutarOperacionEspecial(cifrador, operacion) {
        try {
            const response = await fetch('/operaciones-especiales', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    cifrador: cifrador,
                    operacion: operacion
                })
            });

            const data = await response.json();
            if (data.error) {
                alert(data.error);
            } else {
                if (operacion === 'generarClave') {
                    const inputClave = document.getElementById('clave');
                    if (inputClave) inputClave.value = data.resultado;
                } else {
                    textoSalida.value = data.resultado;
                }
            }
        } catch (error) {
            alert('Error en operación especial: ' + error.message);
        }
    }

    // Event Listeners
    tipoCifrador.addEventListener('change', actualizarInterfaz);
    btnCifrar.addEventListener('click', () => procesarTexto('cifrar'));
    btnDescifrar.addEventListener('click', () => procesarTexto('descifrar'));
    btnFuerzaBruta.addEventListener('click', procesarFuerzaBruta);
    btnLimpiar.addEventListener('click', () => {
        textoEntrada.value = '';
        textoSalida.value = '';
        const inputs = parametrosCifrador.querySelectorAll('input');
        inputs.forEach(input => input.value = '');
    });

    // Inicializar interfaz
    actualizarInterfaz();
});

