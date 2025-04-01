import unittest
from cifradores.adfgvx import (
    COORDENADAS_ADFGVX,
    GenerarCuadroAdfgvx,
    CifrarAdfgvx,
    DescifrarAdfgvx,
    GenerarMatrizAleatoria,
    ValidarMatrizAdfgvx
)

class TestAdfgvx(unittest.TestCase):
    def setUp(self):
        # Generar una matriz válida para las pruebas
        self.matriz_valida = GenerarMatrizAleatoria()
        self.clave_valida = "CLAVE"
        self.texto_valido = "HELLO123"
        
    def test_generar_matriz_aleatoria(self):
        # Verificar que genera una matriz válida
        matriz = GenerarMatrizAleatoria()
        self.assertEqual(len(matriz), 36)
        # Verificar que no hay duplicados
        valores = list(matriz.values())
        self.assertEqual(len(valores), len(set(valores)))
        # Verificar coordenadas válidas
        for coord in matriz.keys():
            self.assertEqual(len(coord), 2)
            self.assertIn(coord[0], COORDENADAS_ADFGVX)
            self.assertIn(coord[1], COORDENADAS_ADFGVX)

    def test_ciclo_cifrado_descifrado(self):
        # Verificar que el texto se puede cifrar y descifrar correctamente
        texto_original = "HELLO123"
        texto_cifrado = CifrarAdfgvx(texto_original, self.matriz_valida, self.clave_valida)
        texto_descifrado = DescifrarAdfgvx(texto_cifrado, self.matriz_valida, self.clave_valida)
        self.assertEqual(texto_original, texto_descifrado)

    def test_validaciones_entrada_cifrado(self):
        # Probar texto vacío
        with self.assertRaises(ValueError) as cm:
            CifrarAdfgvx("", self.matriz_valida, self.clave_valida)
        self.assertIn("no puede estar vacío", str(cm.exception))

        # Probar clave vacía
        with self.assertRaises(ValueError) as cm:
            CifrarAdfgvx(self.texto_valido, self.matriz_valida, "")
        self.assertIn("no puede estar vacía", str(cm.exception))

        # Probar caracteres inválidos en el texto
        with self.assertRaises(ValueError) as cm:
            CifrarAdfgvx("HELLO!@#", self.matriz_valida, self.clave_valida)
        self.assertIn("caracteres no permitidos", str(cm.exception))

    def test_validaciones_entrada_descifrado(self):
        texto_cifrado = CifrarAdfgvx(self.texto_valido, self.matriz_valida, self.clave_valida)

        # Probar texto vacío
        with self.assertRaises(ValueError) as cm:
            DescifrarAdfgvx("", self.matriz_valida, self.clave_valida)
        self.assertIn("no puede estar vacío", str(cm.exception))

        # Probar clave vacía
        with self.assertRaises(ValueError) as cm:
            DescifrarAdfgvx(texto_cifrado, self.matriz_valida, "")
        self.assertIn("no puede estar vacía", str(cm.exception))

        # Probar caracteres inválidos en el texto cifrado
        with self.assertRaises(ValueError) as cm:
            DescifrarAdfgvx("HELLO123", self.matriz_valida, self.clave_valida)
        self.assertIn("caracteres inválidos", str(cm.exception))

        # Probar longitud impar del texto cifrado
        with self.assertRaises(ValueError) as cm:
            DescifrarAdfgvx("ADF", self.matriz_valida, self.clave_valida)
        self.assertIn("longitud par", str(cm.exception))

    def test_validaciones_matriz(self):
        matriz_invalida = self.matriz_valida.copy()
        # Eliminar una coordenada para hacerla inválida
        del matriz_invalida['AA']
        
        with self.assertRaises(ValueError) as cm:
            ValidarMatrizAdfgvx(matriz_invalida)
        self.assertIn("36 caracteres", str(cm.exception))

        # Matriz con duplicados
        matriz_duplicada = self.matriz_valida.copy()
        primera_clave = list(matriz_duplicada.keys())[0]
        segunda_clave = list(matriz_duplicada.keys())[1]
        matriz_duplicada[segunda_clave] = matriz_duplicada[primera_clave]

        with self.assertRaises(ValueError) as cm:
            ValidarMatrizAdfgvx(matriz_duplicada)
        self.assertIn("caracteres repetidos", str(cm.exception))

if __name__ == '__main__':
    unittest.main()

