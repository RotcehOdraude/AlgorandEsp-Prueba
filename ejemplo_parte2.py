import algorandEjemploAldeco.primero_crearCuenta as PRIMERO
import algorandEjemploAldeco.segundo_first_transaction_example as SEGUNDO
import algorandEjemploAldeco.tercero_admin_asset as TERCERO
from algorandEjemploAldeco.tercero_admin_asset import LLAVE_PRIVADA_DE_X, DIRECCION_DE_CUENTA_X

# Borrar el contenido del archivo
with open("cuentas_activos.txt", "w") as archivo:
    archivo.write("")

# Haciendo una estructura para el creador o Sender del activo
class Creador_del_activo:
    def __init__(self, llave_privada, direccion ):
        self.llave_privada = llave_privada
        self.direccion = direccion

### 3.0 CREAR Y ADMINISTRAR MI PROPIO ACTIVO ###
'''
El protocolo Algorand permite la creación de activos on-chain o tokens (criptomonedas personalizadas) que tendran la misma seguridad, compatibilidad, velocidad y facilidad de uso que el Algo. El nombre oficial de los activos en Algorand es Activos Estándar de Algorand (ASA). Los ASA se usan para representar monedas estables (stablecoins), recompensas por lealtad, créditos del sistema, puntos para un juego u objetos coleccionables, por nombrar sólo algunos. También pueden representar activos únicos, como la escritura de una casa, objetos coleccionables, piezas únicas en una cadena de suministro, etc. Además, existen funciones opcionales para imponer restricciones de transferencia a un activo, lo que ayuda a respaldar casos de uso de valores, cumplimiento y certificación.
'''

### 3.1 CREAR UN ACTIVO ###
''' 
Requisitos: 
 - Tener una cuenta de Algorand con fondos (10 Algos)
 - Lista de cuentas que pueden realizar operaciones con el activo

 Operaciones:
 1. Gestionar
 2. Reservar
 3. Congelar
 4. Recuperar
'''

# Generando 3 cuentas
for i in range(3):
    llave_privada_X, direccion_cuenta_X, _ = PRIMERO.generar_cuenta_llavePrivada()
    with open("cuentas_activos.txt", "a") as archivo:
        archivo.write(f"{llave_privada_X},{direccion_cuenta_X}\n")

cuentas_creadas = PRIMERO.leer_cuentas_deArchivo("cuentas_activos.txt") 
# cuentas_creadas = {0: (llave_privada_A,direccion_cuenta_A), 1: (llave_privada_B,direccion_cuenta_B), ...}

creador_del_activo = Creador_del_activo(cuentas_creadas[0][LLAVE_PRIVADA_DE_X],cuentas_creadas[0][DIRECCION_DE_CUENTA_X])

# Añadiendo fondos a la cuenta
# URL: https://testnet.algoexplorer.io/dispenser
input(f"Presiona enter hasta haber añadido fondos a la cuenta del creado del activo:{creador_del_activo.direccion}\n")

# Conexión con el cliente
algod_client = SEGUNDO.conexion_con_cliente_algod(red="algonode")

# Revisando saldo de la cuenta
saldo, account_info_A = SEGUNDO.verficar_balance_cuenta(algod_client, creador_del_activo.direccion)
print(f"Saldo de la cuenta {creador_del_activo.direccion} es: {saldo} microAlgos")

if(saldo > 10000):
    # Creamos un activo
    unsigned_txn = TERCERO.crear_activo(algod_client, cuentas_creadas)

    # Firmamos la transacción
    signed_txn = SEGUNDO.firmar_transaccion(unsigned_txn, creador_del_activo.llave_privada)

    # Enviamos la transacción
    confirmed_txn, tx_id = SEGUNDO.enviar_transaccion(algod_client,signed_txn)

    # Impriendo la transacción del activo
    TERCERO.imprimir_transaccion_activo(algod_client, confirmed_txn, tx_id, creador_del_activo.direccion)

    print("Account 1 address: {}".format(creador_del_activo.direccion))
    print("Account 2 address: {}".format(cuentas_creadas[1][DIRECCION_DE_CUENTA_X]))
    print("Account 3 address: {}".format(cuentas_creadas[2][DIRECCION_DE_CUENTA_X]))
else:
    print("La cuenta no tiene suficientes fondos para crear un activo")

