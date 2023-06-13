import algorandEjemploAldeco.primero_crearCuenta as PRIMERO
import algorandEjemploAldeco.segundo_first_transaction_example as SEGUNDO

### 1.1 CREANDO CUENTAS EN ALGORAND ###
'''
# Generando llave privada de cuenta A y su dirección
cuenta_A, _ = PRIMERO.generar_cuenta()

# Almacenando en un archivo de texto la llave privada y la dirección de la cuenta A
with open("cuentas.txt", "w") as archivo:
    archivo.write(f"{cuenta_A.llave_privada},{cuenta_A.direccion}\n")

# Generando llave privada de cuenta A y su dirección
cuenta_B, _ = PRIMERO.generar_cuenta()

# Almacenando en un archivo de texto la llave privada y la dirección de la cuenta A
with open("cuentas.txt", "a") as archivo:
    archivo.write(f"{cuenta_B.llave_privada},{cuenta_B.direccion}\n")
'''
l_cuentas_creadas = PRIMERO.leer_cuentas_deArchivo("cuentas.txt")

cuenta_A = l_cuentas_creadas[0]  
cuenta_B = l_cuentas_creadas[1] 

### 1.2 AÑADIENDO FONDOS A LAS CUENTAS ###
# URL: https://testnet.algoexplorer.io/dispenser

### 1.3 VERIFICANDO EL BALANCE DE NUESTRAS CUENTAS ###
# URL: https://testnet.algoexplorer.io/

### 2. TU PRIMERA TRANSACCIÓN ###
# Cualquier transacción puede incluir una "nota" arbitraria de hasta 1kb. En otras palabras, las notas permiten almacenar una pequeña cantidad de datos en la cadena de bloques que nos permitirá identificar una transacción de otra de manera local.

### 2.1 CONECTA CON EL CLIENTE ###
algod_client = SEGUNDO.conexion_con_cliente_algod(red="algonode")

### 2.2 REVISAR EL SALDO DE LA CUENTA A ###
saldo, account_info_A = SEGUNDO.verficar_balance_cuenta(algod_client, cuenta_A.direccion)

### 2.3 CREAR UNA TRANSACCIÓN ###
amount = 500000
note = "Esta es la n-esima transaccion de A"
unsigned_txn,params = SEGUNDO.crear_transaccion(algod_client, cuenta_A.direccion, cuenta_B.direccion, amount, note)

### 2.4 FIRMAR LA TRANSACCIÓN ###
signed_txn = SEGUNDO.firmar_transaccion(unsigned_txn, cuenta_A.llave_privada)

### 2.5 ENVIAR UNA TRANSACCIÓN ###
confirmed_txn,tx_id = SEGUNDO.enviar_transaccion(algod_client, signed_txn)

# Imprimiendo información de la transacción
SEGUNDO.imprimir_transaccion(algod_client,cuenta_A.direccion,account_info_A,confirmed_txn,amount,params)

# Confirmando transaccion en el explorador
# URL: https://testnet.algoexplorer.io/
# Puedes usar el tx_id o la dirección de la cuenta origen o la dirección de la cuenta destino


