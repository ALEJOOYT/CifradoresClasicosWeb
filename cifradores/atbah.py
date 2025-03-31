def atbash_cipher(text):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    reversed_alphabet = alphabet[::-1]

    translation_table = str.maketrans(alphabet + alphabet.lower(), reversed_alphabet + reversed_alphabet.lower())

    return text.translate(translation_table)

# Menú interactivo
while True:
    print("\n===== Cifrado Atbash =====")
    print("1. Cifrar un mensaje")
    print("2. Descifrar un mensaje")
    print("3. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        mensaje = input("Ingrese el texto a cifrar: ")
        print("Mensaje cifrado:", atbash_cipher(mensaje))

    elif opcion == "2":
        mensaje = input("Ingrese el texto a descifrar: ")
        print("Mensaje descifrado:", atbash_cipher(mensaje))

    elif opcion == "3":
        print("Saliendo del programa...")
        break

    else:
        print("Opción no válida, por favor intente de nuevo.")
