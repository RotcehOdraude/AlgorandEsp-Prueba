import algorandEjemploAldeco.primero_crearCuenta as PRIMERO
import algorandEjemploAldeco.segundo_first_transaction_example as SEGUNDO
import algorandEjemploAldeco.tercero_admin_asset as TERCERO


# #Borra el contenido del archivo
# with open("cuentas_activos.txt", "w") as archivo:
#     archivo.write("")



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

cuentas_creadas = PRIMERO.leer_cuentas_deArchivo("cuentas_activos.txt")
# cuentas_creadas = []
# # Generando 3 cuentas
# for i in range(3):
#     cuenta, _ = PRIMERO.generar_cuenta()
#     cuentas_creadas.append(cuenta)
#     with open("cuentas_activos.txt", "a") as archivo:
#         archivo.write(f"{cuenta.llave_privada},{cuenta.direccion}\n")

creador_del_activo = cuentas_creadas[0]

cuenta_0 = cuentas_creadas[0]
cuenta_1 = cuentas_creadas[1]
cuenta_2 = cuentas_creadas[2]

# Añadiendo fondos a la cuenta
# URL: https://testnet.algoexplorer.io/dispenser
input(f"Presiona enter hasta haber añadido fondos a la cuenta del creador del activo:{creador_del_activo.direccion}\n")

# Conexión con el cliente
algod_client = SEGUNDO.conexion_con_cliente_algod(red="algonode")

# Revisando saldo de la cuenta
saldo, account_info_A = SEGUNDO.verficar_balance_cuenta(algod_client, creador_del_activo.direccion)
print(f"Saldo de la cuenta {creador_del_activo.direccion} es: {saldo} microAlgos")

if(saldo > 10000):
    # Creamos un activo
    print("\n####### Creando activo...")
    sender = cuenta_0.direccion
    manager = cuenta_1.direccion
    reserve = cuenta_1.direccion
    freeze = cuenta_1.direccion
    clawback = cuenta_1.direccion

    confirmed_txn, tx_id = TERCERO.crear_activo(
        algod_client,
        creador_del_activo.llave_privada, 
        sender, 
        manager, 
        reserve, 
        freeze, 
        clawback,
        asset_name="caja_jer", # Max 8 caracteres
        unit_name="jeringa" # Max 8 caracteres
    )

    # Impriendo la transacción del activo
    TERCERO.imprimir_transaccion_activo(algod_client, confirmed_txn, tx_id, creador_del_activo.direccion)

    # print("Account 1 address: {}".format(creador_del_activo.direccion))
    # print("Account 2 address: {}".format(cuenta_1.direccion))
    # print("Account 3 address: {}".format(cuenta_2.direccion))

    ### 3.2 MODIFICANDO UN ACTIVO ###
    print("\n####### Modificando activo...")
    # Cambiando administrador
    # El administrador actual (la cuenta 1) emite una transacción de configuración de activos que asigna la cuenta 0 como nuevo administrador. 
    # El resto de las operaciones quedan igual.

    sender = cuenta_1.direccion
    sender_private_key = cuenta_1.llave_privada
    manager = cuenta_0.direccion
    reserve = cuenta_1.direccion
    freeze = cuenta_1.direccion
    clawback = cuenta_1.direccion
    asset_id = TERCERO.obtener_asset_id(algod_client, tx_id)

    TERCERO.modificando_activo(algod_client, asset_id, sender, sender_private_key, manager, reserve, freeze, clawback)

    # Imprimiendo el activo creado
    TERCERO.print_created_asset(algod_client, sender, asset_id)


    ### 3.3 RECIVIR UN ACTIVO (Opt.in)###
    print("\n####### Recibiendo activo...")
    '''
    Antes de que una cuenta pueda recibir un activo específico, debe "optar" por recibirlo, es decir debe de realizar la operación de opt-in.
    La operación de opt-in es simplemente una transferencia de activos con una cantidad de 0, tanto hacia como desde la cuenta realizando dicha operación.
    El siguiente código muestra esta operación para la cuenta 2.
    '''

    confirmed_txn, txid = TERCERO.opt_in(algod_client, asset_id, cuenta_2.direccion,cuenta_2.llave_privada)

    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))

    # Verificamos que el activo pertenece a esta cuenta
    # Este debe mostrar balance de 0
    TERCERO.print_asset_holding(algod_client, cuenta_2.direccion, asset_id)

    ### 3.4 TRANSFERIR UN ACTIVO ###
    print("\n####### Transferir activo...")
    '''
    Los activos pueden transferirse entre cuentas que hayan optado por recibirlos (operación anterior). Son análogas a las transacciones de pago estándar, pero para los ASAs.
    El siguiente código muestra un ejemplo que transfiere 10 activos de la cuenta 0 a la cuenta 2.
    '''
    confirmed_txn, txid = TERCERO.transferir_activo(algod_client ,cuenta_0.direccion, cuenta_0.llave_privada, cuenta_2.direccion, 10, asset_id)

    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
    TERCERO.print_asset_holding(algod_client, cuenta_2.direccion, asset_id)

    ### 3.5 CONGELAR UN ACTIVO ###
    print("\n####### Congelar activo...")
    '''
    Congelar o descongelar un activo para una cuenta requiere de una transacción firmada por la cuenta que realizará esta operación.
    El código siguiente muestra como la cuenta 1 congela los activos de la cuenta 2.
    '''
    confirmed_txn, txid = TERCERO.congelar_activo(algod_client, cuenta_1.direccion, cuenta_1.llave_privada, asset_id, cuenta_2.direccion)

    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
    TERCERO.print_asset_holding(algod_client, cuenta_2.direccion, asset_id)

    ### 3.6 REVOCAR UN ACTIVO ###
    print("\n####### Revocar activo...")
    '''
    La revocación de un activo elimina un número específico de activos de una cuenta desde la cuenta de recuperación de dicho activo.
    Para realizar esta operación es necesario especificar un emisor de activos (la cuenta de destino a revocar) y un receptor de activos (la cuenta a la que se transferiran los fondos de regreso).
    El siguiente código muestra la revocación de la cuenta 2 para regresar los activos a la cuenta 0, esto realizado por la cuenta 1.
    '''
    confirmed_txn, txid = TERCERO.revocar_activo(algod_client, asset_id, cuenta_1.direccion, cuenta_1.llave_privada, cuenta_2.direccion, cuenta_0.direccion)

    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))

    print("Account 3")
    TERCERO.print_asset_holding(algod_client, cuenta_2.direccion, asset_id)

    print("Account 1")
    TERCERO.print_asset_holding(algod_client, cuenta_0.direccion, asset_id)
    
    ### 3.7 DESTRUIR UN ACTIVO ###
    print("\n####### Destruir activo...")
    '''
    Los activos pueden ser destruidos por la cuenta administradora. Todos los activos deben ser propiedad del creador del activo antes de que el activo pueda ser eliminado.
    El siguiente código muestra un ejemplo donde la cuenta 0 destruye un activo de la cuenta 2.
    '''
    confirmed_txn, txid = TERCERO.destruir_activo(algod_client,asset_id,cuenta_0.direccion,cuenta_0.llave_privada)

    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))

    try:
        print("Account 3 must do a transaction for an amount of 0, ")
        print("with a close_assets_to to the creator account, to clear it from its accountholdings")
        print("For Account 1, nothing should print after this as the asset is destroyed on the creator account")
        TERCERO.print_asset_holding(algod_client, cuenta_0.direccion, asset_id)
        TERCERO.print_created_asset(algod_client, cuenta_0.direccion, asset_id)

    except Exception as e:
        print(e)



else:
    print("La cuenta no tiene suficientes fondos para crear un activo")
