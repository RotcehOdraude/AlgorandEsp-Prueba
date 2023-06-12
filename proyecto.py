from algorandEjemploAldeco.primero_crearCuenta import * 
from algorandEjemploAldeco.segundo_first_transaction_example import *

### 1.1 CREANDO CUENTAS EN ALGORAND ###
'''
# Generando llave privada de cuenta A y su dirección
llave_privada_A, direccion_cuenta_A, _ = generar_cuenta_llavePrivada()

# Almacenando en un archivo de texto la llave privada y la dirección de la cuenta A
with open("cuentas.txt", "w") as archivo:
    archivo.write(f"A: {llave_privada_A},{direccion_cuenta_A}\n")

# Generando llave privada de cuenta A y su dirección
llave_privada_B, direccion_cuenta_B, _ = generar_cuenta_llavePrivada()

# Almacenando en un archivo de texto la llave privada y la dirección de la cuenta A
with open("cuentas.txt", "a") as archivo:
    archivo.write(f"B: {llave_privada_B},{direccion_cuenta_B}\n")
'''
cuentas_creadas = leer_cuentas_deArchivo("cuentas.txt")
llave_privada_A,direccion_cuenta_A = cuentas_creadas[0]
llave_privada_B,direccion_cuenta_B = cuentas_creadas[1]

### 1.2 AÑADIENDO FONDOS A LAS CUENTAS ###
# URL: https://testnet.algoexplorer.io/dispenser

### 1.3 VERIFICANDO EL BALANCE DE NUESTRAS CUENTAS ###
# URL: https://testnet.algoexplorer.io/

### 2. TU PRIMERA TRANSACCIÓN ###
# Cualquier transacción puede incluir una "nota" arbitraria de hasta 1kb. En otras palabras, las notas permiten almacenar una pequeña cantidad de datos en la cadena de bloques que nos permitirá identificar una transacción de otra de manera local.

### 2.1 CONECTA CON EL CLIENTE ###
algod_client = conexion_con_cliente_algod(red="algonode")

### 2.2 REVISAR EL SALDO DE LA CUENTA A ###
saldo, account_info_A = verficar_balance_cuenta(algod_client, direccion_cuenta_A)

### 2.3 CREAR UNA TRANSACCIÓN ###
amount = 500000
unsigned_txn,params = crear_transaccion(algod_client, direccion_cuenta_A, direccion_cuenta_B, amount, note="Esta es la primera transaccion de A")

### 2.4 FIRMAR LA TRANSACCIÓN ###
signed_txn = firmar_transaccion(unsigned_txn, llave_privada_A)

### 2.5 ENVIAR UNA TRANSACCIÓN ###
confirmed_txn,tx_id = enviar_transaccion(algod_client, signed_txn)

# Imprimiendo información de la transacción
imprimir_transaccion(algod_client,direccion_cuenta_A,account_info_A,confirmed_txn,amount,params)

# Confirmando transaccion en el explorador
# URL: https://testnet.algoexplorer.io/
# Puedes usar el 
