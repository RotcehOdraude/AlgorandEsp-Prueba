import algosdk

# Haciendo una estructura para la cuenta
class Cuenta:
    def __init__(self, llave_privada, direccion ):
        self.llave_privada = llave_privada
        self.direccion = direccion

def generar_cuenta():
    """
    Genera una nueva llave privada y la dirección de cuenta asociada.

    Returns:
        Tuple: Una tupla que contiene la llave privada generada, la dirección de cuenta y el mnemónico de la llave privada.
    
    Raises:
        None.

    Example:
        private_key, account_address = generar_cuenta()
    """
    # Generate a fresh private key and associated account address
    private_key, account_address = algosdk.account.generate_account()

    # Convert the private key into a mnemonic which is easier to use
    mnemonic = algosdk.mnemonic.from_private_key(private_key)

    # Wrapping the private key and address into a class
    account = Cuenta(private_key, account_address)

    return account, mnemonic

def leer_cuentas_deArchivo(archivo):
    """
    Lee un archivo y procesa cada línea para obtener un diccionario de cuentas numeradas.

    Parámetros:
    - archivo (str): El nombre del archivo a leer.

    Retorna:
    - dict: Un diccionario donde sus elementos son las cuentas generadas y almacenadas en el archivo [archivo].txt,
             y los valores son tuplas que contienen la clave y la dirección leídas de cada cuenta.

    """
    cuentas = []
    with open(archivo, "r") as file:
        for linea in file:
            linea = linea.strip()  # Eliminar espacios en blanco al inicio y final de la línea
            if linea:
                clave, direccion = linea.split(",")  # Dividir la línea en clave y dirección
                cuentas.append(Cuenta(clave, direccion))  
    return cuentas