class Rotor:
    def __init__(self, cableadoInterno, muesca):
        self.cableadoInterno = cableadoInterno
        self.muesca = muesca
        self.posicion = 0

    def Adelante(self, letra):
        indice = (ord(letra) - ord('A') + self.posicion) % 26
        return chr((ord(self.cableadoInterno[indice]) - ord('A') - self.posicion) % 26 + ord('A'))

    def Atras(self, letra):
        indice = (ord(letra) - ord('A') + self.posicion) % 26
        letraTransformada = chr(indice + ord('A'))
        return chr((self.cableadoInterno.index(letraTransformada) - self.posicion) % 26 + ord('A'))

    def Girar(self):
        self.posicion = (self.posicion + 1) % 26
        return self.posicion == self.muesca


class Reflector:
    def __init__(self, cableadoInterno):
        self.cableadoInterno = cableadoInterno

    def Reflejar(self, letra):
        indice = ord(letra) - ord('A')
        return self.cableadoInterno[indice]


class TableroConexion:
    def __init__(self, pares):
        self.mapeo = {}
        for a, b in pares:
            self.mapeo[a], self.mapeo[b] = b, a

    def Intercambiar(self, letra):
        return self.mapeo.get(letra, letra)


class MaquinaEnigma:
    def __init__(self, rotores, reflector, tableroConexion):
        self.rotores = rotores
        self.reflector = reflector
        self.tableroConexion = tableroConexion
        self.posicionesIniciales = [rotor.posicion for rotor in self.rotores]

    def CodificarLetra(self, letra):
        letra = self.tableroConexion.Intercambiar(letra)
        for rotor in self.rotores:
            letra = rotor.Adelante(letra)
        letra = self.reflector.Reflejar(letra)
        for rotor in reversed(self.rotores):
            letra = rotor.Atras(letra)
        letra = self.tableroConexion.Intercambiar(letra)
        self.GirarRotores()
        return letra

    def GirarRotores(self):
        girarSiguiente = True
        for rotor in self.rotores:
            if girarSiguiente:
                girarSiguiente = rotor.Girar()

    def CodificarMensaje(self, mensaje):
        mensajeCodificado = ""
        for letra in mensaje.upper():
            if letra.isalpha():
                mensajeCodificado += self.CodificarLetra(letra)
            else:
                mensajeCodificado += letra
        return mensajeCodificado

    def ReiniciarRotores(self):
        for i, rotor in enumerate(self.rotores):
            rotor.posicion = self.posicionesIniciales[i]


# Configuración de la máquina Enigma
def ObtenerMaquinaEnigma(posicion_rotor1=16, posicion_rotor2=4, posicion_rotor3=21, tablero_conexiones=None):
    # Crear rotores con las posiciones especificadas
    rotor1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", posicion_rotor1)
    rotor2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", posicion_rotor2)
    rotor3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", posicion_rotor3)
    reflector = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")

    # Procesar el tablero de conexiones
    pares_conexiones = []

    # Si se proporciona como string en formato "A-Z,B-Y,C-X"
    if isinstance(tablero_conexiones, str) and tablero_conexiones:
        try:
            conexiones = tablero_conexiones.split(',')
            for conexion in conexiones:
                if '-' in conexion:
                    par = conexion.split('-')
                    if len(par) == 2 and len(par[0]) == 1 and len(par[1]) == 1:
                        pares_conexiones.append((par[0].upper(), par[1].upper()))
        except Exception as e:
            # Si hay un error en el formato, usar conexiones por defecto
            pares_conexiones = [("A", "Z"), ("B", "Y"), ("C", "X")]
    # Si no se proporciona nada o es None, usar conexiones por defecto
    elif tablero_conexiones is None:
        pares_conexiones = [("A", "Z"), ("B", "Y"), ("C", "X")]
    # Si se proporciona como lista de tuplas, usarla directamente
    else:
        pares_conexiones = tablero_conexiones

    tableroConexion = TableroConexion(pares_conexiones)
    return MaquinaEnigma([rotor1, rotor2, rotor3], reflector, tableroConexion)


# Mantener compatibilidad con el código existente
def ObtenerMaquinaEnigmaPorDefecto():
    """Función de compatibilidad que devuelve la configuración por defecto de la máquina Enigma"""
    return ObtenerMaquinaEnigma()

def Cifrar(texto, rotor1=16, rotor2=4, rotor3=21, tableroConexiones=None, reflector=None):
    # Detectar el formato de llamada (antiguo o nuevo)
    pos_rotor1, pos_rotor2, pos_rotor3 = 16, 4, 21  # valores por defecto
    conexiones = None

    # Formato antiguo: Cifrar(texto, [rotor1, rotor2, rotor3], reflector, conexiones)
    if isinstance(rotor2, type(None)) and isinstance(rotor1, list) and len(rotor1) >= 3:
        # Detectamos el formato antiguo: primer parámetro es una lista de rotores
        try:
            pos_rotor1 = int(rotor1[0]) if rotor1[0] is not None else 16
            pos_rotor2 = int(rotor1[1]) if rotor1[1] is not None else 4
            pos_rotor3 = int(rotor1[2]) if rotor1[2] is not None else 21
            # En este caso, rotor3 contiene las conexiones
            conexiones = rotor3
        except (ValueError, IndexError):
            # Si hay error en la conversión, usar valores por defecto
            pos_rotor1, pos_rotor2, pos_rotor3 = 16, 4, 21
    # Segundo formato antiguo: Cifrar(texto, rotores_list, reflector, conexiones)
    elif isinstance(rotor1, list) and len(rotor1) >= 3:
        try:
            pos_rotor1 = int(rotor1[0]) if rotor1[0] is not None else 16
            pos_rotor2 = int(rotor1[1]) if rotor1[1] is not None else 4
            pos_rotor3 = int(rotor1[2]) if rotor1[2] is not None else 21
            # En este formato, las conexiones vienen en rotor3
            conexiones = rotor3
        except (ValueError, IndexError):
            pos_rotor1, pos_rotor2, pos_rotor3 = 16, 4, 21
    # Formato nuevo: Cifrar(texto, rotor1, rotor2, rotor3, tableroConexiones)
    else:
        try:
            pos_rotor1 = int(rotor1) if rotor1 is not None else 16
            pos_rotor2 = int(rotor2) if rotor2 is not None else 4
            pos_rotor3 = int(rotor3) if rotor3 is not None else 21
            conexiones = tableroConexiones
        except ValueError:
            # Si hay error en la conversión, usar valores por defecto
            pos_rotor1, pos_rotor2, pos_rotor3 = 16, 4, 21

    # Asegurar que las posiciones estén en el rango válido (0-25)
    pos_rotor1 = max(0, min(25, pos_rotor1))
    pos_rotor2 = max(0, min(25, pos_rotor2))
    pos_rotor3 = max(0, min(25, pos_rotor3))
    maquina = ObtenerMaquinaEnigma(pos_rotor1, pos_rotor2, pos_rotor3, conexiones)
    return maquina.CodificarMensaje(texto)

def Descifrar(textoCifrado, rotor1=16, rotor2=4, rotor3=21, tableroConexiones=None, reflector=None):
    return Cifrar(textoCifrado, rotor1, rotor2, rotor3, tableroConexiones, reflector)
