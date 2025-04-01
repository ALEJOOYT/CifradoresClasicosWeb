class Rotor:
    def __init__(self, cableadoInterno, muesca):
        self.cableadoInterno = cableadoInterno  # Cableado interno del rotor
        self.muesca = muesca  # Posición de giro (notch)
        self.posicion = 0  # Posición inicial del rotor

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


# Configuración por defecto de la máquina Enigma
def ObtenerMaquinaEnigmaPorDefecto():
    rotor1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 16)
    rotor2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", 4)
    rotor3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 21)
    reflector = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
    tableroConexion = TableroConexion([("A", "Z"), ("B", "Y"), ("C", "X")])
    return MaquinaEnigma([rotor1, rotor2, rotor3], reflector, tableroConexion)


def Cifrar(texto, rotores=None, reflector=None, conexiones=None):
    """
    Cifra un texto utilizando la máquina Enigma.
    
    Args:
        texto: El texto a cifrar
        rotores: Configuración personalizada de rotores (opcional)
        reflector: Configuración personalizada del reflector (opcional)
        conexiones: Configuración personalizada de conexiones (opcional)
        
    Returns:
        El texto cifrado
    """
    maquina = ObtenerMaquinaEnigmaPorDefecto()
    
    # Aquí se podrían agregar opciones para configurar la máquina
    # según los parámetros adicionales
    
    return maquina.CodificarMensaje(texto)


def Descifrar(textoCifrado, rotores=None, reflector=None, conexiones=None):
    """
    Descifra un texto utilizando la máquina Enigma.
    
    Args:
        textoCifrado: El texto cifrado a descifrar
        rotores: Configuración personalizada de rotores (opcional)
        reflector: Configuración personalizada del reflector (opcional)
        conexiones: Configuración personalizada de conexiones (opcional)
        
    Returns:
        El texto descifrado
    """
    maquina = ObtenerMaquinaEnigmaPorDefecto()
    
    # Aquí se podrían agregar opciones para configurar la máquina
    # según los parámetros adicionales
    
    return maquina.CodificarMensaje(textoCifrado)
