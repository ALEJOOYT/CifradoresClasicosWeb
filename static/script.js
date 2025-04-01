document.addEventListener('DOMContentLoaded', function () {
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
                { id: 'clave', label: 'Clave', type: 'text' },
                { id: 'palabrasClave', label: 'Palabras clave para fuerza bruta (separadas por comas)', type: 'text' }
            ],
            tieneFuerzaBruta: true
        },
        'hill': {
            params: [
                { id: 'matrizSize', label: 'Tamaño de la matriz', type: 'number', min: 2, max: 10, value: 2 }
            ],
            botonesExtra: [
                { id: 'btnGenerarMatrizAleatoria', label: 'Generar Matriz Aleatoria', operacion: 'generarMatrizAleatoria' }
            ],
            tieneFuerzaBruta: true,
            customRender: function (parametrosCifrador) {
                // Tamaño de matriz
                const div = document.createElement('div');
                div.className = 'parametroEntrada';

                const label = document.createElement('label');
                label.htmlFor = 'matrizSize';
                label.textContent = 'Tamaño de la matriz';

                const input = document.createElement('input');
                input.type = 'number';
                input.id = 'matrizSize';
                input.name = 'matrizSize';
                input.min = 2;
                input.max = 10;
                input.value = 2;

                div.appendChild(label);
                div.appendChild(input);
                parametrosCifrador.appendChild(div);

                // Contenedor para la matriz
                const matrizContainer = document.createElement('div');
                matrizContainer.id = 'matrizContainer';
                matrizContainer.className = 'matriz-container';
                parametrosCifrador.appendChild(matrizContainer);

                // Botón para generar matriz aleatoria
                const btnDiv = document.createElement('div');
                btnDiv.className = 'botonesExtra';

                const btnGenerarMatriz = document.createElement('button');
                btnGenerarMatriz.textContent = 'Generar Matriz Aleatoria';
                btnGenerarMatriz.className = 'boton botonExtra';
                btnGenerarMatriz.onclick = generarMatrizAleatoria;

                btnDiv.appendChild(btnGenerarMatriz);
                parametrosCifrador.appendChild(btnDiv);

                // Campo oculto para almacenar la matriz como string
                // Campo oculto para almacenar la matriz como string
                const hiddenInput = document.createElement('input');
                hiddenInput.type = 'hidden';
                hiddenInput.id = 'matriz';
                hiddenInput.name = 'matriz';
                parametrosCifrador.appendChild(hiddenInput);
                // Crear matriz inicial
                crearMatriz(2);

                // Event listener para cambiar tamaño de matriz
                input.addEventListener('change', function () {
                    const size = parseInt(this.value);
                    if (size >= 2 && size <= 10) {
                        crearMatriz(size);
                    }
                });
            }
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

        // Usar renderizado personalizado si existe
        if (parametrosCifradores[cifrador].customRender) {
            parametrosCifradores[cifrador].customRender(parametrosCifrador);
            return;
        }

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
            if (param.value !== undefined) input.value = param.value;

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
    // Función para obtener los valores de los parámetros
    function obtenerParametros() {
        const cifrador = tipoCifrador.value;
        const params = {};

        if (cifrador && parametrosCifradores[cifrador]) {
            parametrosCifradores[cifrador].params.forEach(param => {
                const input = document.getElementById(param.id);
                if (input) params[param.id] = input.value;
            });

            // Caso especial para Hill, obtener la matriz del input oculto
            if (cifrador === 'hill') {
                const hiddenInput = document.getElementById('matriz');
                if (hiddenInput && hiddenInput.value) {
                    // Asegurar que se use el nombre correcto para el parámetro
                    params['matriz'] = hiddenInput.value;
                    console.log('Enviando matriz:', params['matriz']);
                } else {
                    console.error('Error: El input oculto de la matriz no existe o está vacío');
                }
            }

            console.log('Parámetros enviados:', params);
            return params;
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

        // Validar parámetros especiales por cifrador
        if (cifrador === 'hill' && !validarMatriz()) {
            return;
        }

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

        // Procesar palabrasClave para Playfair
        if (cifrador === 'playfair' && params.palabrasClave) {
            params.palabrasClave = params.palabrasClave.split(',').map(p => p.trim()).filter(p => p);
        }

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

                        // Check if the result is already formatted (like from PlayFair)
                        if (typeof resultado === 'string' && resultado.includes('|')) {
                            return resultado;
                        } else if (resultado.key && resultado.text) {
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
    // Funciones para manejar la matriz de Hill
    function crearMatriz(size) {
        const container = document.getElementById('matrizContainer');
        if (!container) return;

        container.innerHTML = '';
        container.style.gridTemplateColumns = `repeat(${size}, 1fr)`;

        for (let i = 0; i < size; i++) {
            for (let j = 0; j < size; j++) {
                const cell = document.createElement('input');
                cell.type = 'number';
                cell.className = 'matriz-cell';
                cell.dataset.row = i;
                cell.dataset.col = j;
                cell.value = 0;
                cell.min = 0;
                cell.max = 25;

                // Actualizar matriz cuando cambie un valor
                cell.addEventListener('change', actualizarValorMatriz);

                container.appendChild(cell);
            }
        }

        // Inicializar la matriz con valores por defecto
        actualizarMatriz();
    }

    function actualizarValorMatriz() {
        actualizarMatriz();
    }

    function actualizarMatriz() {
        const container = document.getElementById('matrizContainer');
        const hiddenInput = document.getElementById('matriz');
        if (!container || !hiddenInput) return;

        const cells = container.querySelectorAll('.matriz-cell');
        const size = Math.sqrt(cells.length);

        // Crear matriz
        const matriz = [];
        for (let i = 0; i < size; i++) {
            matriz.push([]);
            for (let j = 0; j < size; j++) {
                const cell = container.querySelector(`.matriz-cell[data-row="${i}"][data-col="${j}"]`);
                matriz[i].push(parseInt(cell.value) || 0);
            }
        }

        // Convertir matriz a string (formato plano)
        // Convertir matriz a string con formato de matriz cuadrada para el backend
        // Formato: "valor1,valor2,valor3;valor4,valor5,valor6;..." donde cada fila está separada por punto y coma
        const matrizString = matriz.map(row => row.join(',')).join(';');
        hiddenInput.value = matrizString;
        console.log('Matriz actualizada:', hiddenInput.value);
    }

    // Función para generar una matriz aleatoria
    function generarMatrizAleatoria() {
        const sizeInput = document.getElementById('matrizSize');
        if (!sizeInput) return;

        const size = parseInt(sizeInput.value) || 2;
        const container = document.getElementById('matrizContainer');
        if (!container) return;

        // Generar valores aleatorios para cada celda
        const cells = container.querySelectorAll('.matriz-cell');
        cells.forEach(cell => {
            cell.value = Math.floor(Math.random() * 26); // Valores entre 0 y 25
        });

        // Actualizar matriz
        actualizarMatriz();
    }

    // Validar matriz antes de enviar
    function validarMatriz() {
        const hiddenInput = document.getElementById('matriz');
        if (!hiddenInput || !hiddenInput.value) {
            alert('Error: No se ha definido la matriz');
            return false;
        }

        // Verificar que todos los valores sean números válidos
        const matrixValues = hiddenInput.value.split(';').map(row => row.split(',').map(Number));
        for (let i = 0; i < matrixValues.length; i++) {
            for (let j = 0; j < matrixValues[i].length; j++) {
                if (isNaN(matrixValues[i][j]) || matrixValues[i][j] < 0 || matrixValues[i][j] > 25) {
                    alert('Error: La matriz contiene valores inválidos. Todos deben ser números entre 0 y 25.');
                    return false;
                }
            }
        }

        return true;
    }
});
