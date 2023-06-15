import json
from algosdk.transaction import *
import algorandEjemploAldeco.segundo_first_transaction_example as SEGUNDO

# Definicion de constantes
DIRECCION_DE_CUENTA_X = 1 # Usado para la tupla (llave_privada_X,direccion_cuenta_X); Donde 1 representa el segundo elemento en la tupla
LLAVE_PRIVADA_DE_X = 0 # Usado para la tupla (llave_privada_X,direccion_cuenta_X); Donde 0 representa el primer elemento en la tupla

#  Función de utilidad para imprimir el activo creado para la cuenta y el assetid
def print_created_asset(algodclient, address, assetid):
    account_info = algodclient.account_info(address)
    idx = 0;
    for my_account_info in account_info['created-assets']:
        scrutinized_asset = account_info['created-assets'][idx]
        idx = idx + 1
        if (scrutinized_asset['index'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['index']))
            print(json.dumps(my_account_info['params'], indent=4))
            break


#Función de utilidad para imprimir la tenencia de activos para la cuenta y assetid
def print_asset_holding(algodclient, address, assetid):
    account_info = algodclient.account_info(address)
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1
        if (scrutinized_asset['asset-id'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['asset-id']))
            print(json.dumps(scrutinized_asset, indent=4))
            break


# Crear un activo
def crear_activo(algod_client, sender_private_key ,sender, manager, reserve, freeze, clawback, asset_name = "Jeringas", unit_name = "Jeringa",url = "https://path/to/my/asset/details", decimals = 0):
    
    # Obtener parámetros de red para transacciones antes de cada transacción.
    params = algod_client.suggested_params()
    params.fee = 1000
    params.flat_fee = True

    unsigned_txn = AssetConfigTxn(
        sender = sender,
        sp = params,
        total = 1000,
        default_frozen = False,
        unit_name = unit_name,
        asset_name = asset_name,
        manager =  manager, 
        reserve =  reserve, 
        freeze =  freeze,
        clawback =  clawback,
        url = url,
        decimals = decimals
    )
    # Firmamos la transacción
    signed_txn = SEGUNDO.firmar_transaccion(unsigned_txn, sender_private_key)

    # Enviamos la transacción
    confirmed_txn, tx_id = SEGUNDO.enviar_transaccion(algod_client,signed_txn)

    return confirmed_txn, tx_id
    

'''
# Se envía la transacción a la red de la misma manera que se describió previamente
try:
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(txid))
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))

except Exception as err:
    print(err)
'''
def obtener_asset_id(algod_client, tx_id):
    pendig_tx = algod_client.pending_transaction_info(tx_id)
    asset_id = pendig_tx["asset-index"]
    return asset_id


def imprimir_transaccion_activo(algod_client, confirmed_txn, tx_id, sender):
    """
    Imprime información sobre una transacción de activo y muestra detalles adicionales del activo y las tenencias asociadas.

    Parámetros:
    - algod_client (algod.AlgodClient): El cliente Algod utilizado para interactuar con la cadena de bloques.
    - confirmed_txn (dict): La transacción confirmada de activo.
    - tx_id (str): El ID de transacción de la transacción de activo.
    - accounts (list): Una lista de cuentas involucradas en la transacción de activo.

    """
    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    try:
        asset_id = obtener_asset_id(algod_client, tx_id)

        print_created_asset(algod_client, sender, asset_id)
        print_asset_holding(algod_client, sender, asset_id)
    except Exception as e:
        print(e)


# Modificando un activo
def modificando_activo(algod_client, asset_id, sender,sender_private_key, manager, reserve, freeze, clawback):
    params = algod_client.suggested_params()

    txn = AssetConfigTxn(
        sender= sender,
        sp=params,
        index=asset_id,
        manager=manager,
        reserve=reserve,
        freeze=freeze,
        clawback=clawback
    )

    s_txn = SEGUNDO.firmar_transaccion(txn, sender_private_key)
    SEGUNDO.enviar_transaccion(algod_client,s_txn)

# OPT-IN
def opt_in(algod_client, asset_id, opt_adress,opt_private_key):
    # Verificar si asset_id esta en la cuenta "opt_adress" antes del opt-in
    params = algod_client.suggested_params()

    account_info = algod_client.account_info(opt_adress)
    holding = None
    idx = 0

    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1
        if (scrutinized_asset['asset-id'] == asset_id):
            holding = True
            break

    if not holding:
        # Usamos la clase AssetTransferTxn para transferir y realizar opt-in
        txn = AssetTransferTxn(
            sender=opt_adress,
            sp=params,
            receiver=opt_adress,
            amt=0,
            index=asset_id)
        
        # Se firma la transacción
        stxn = SEGUNDO.firmar_transaccion(txn,opt_private_key)

        # Se envia la transacción a la red
        confirmed_txn, txid = SEGUNDO.enviar_transaccion(algod_client,stxn)
        return confirmed_txn, txid

# Transferir un activo

def transferir_activo(algod_client,sender_address,sender_private_key,receiver_adderss,amount,asset_id):
    params = algod_client.suggested_params()

    txn = AssetTransferTxn(
        sender = sender_address,
        sp = params,
        receiver = receiver_adderss,
        amt = amount,
        index = asset_id)
    
    # Se firma la transacción
    stxn = SEGUNDO.firmar_transaccion(txn,sender_private_key)

    # Se envia la transacción a la red
    confirmed_txn, txid = SEGUNDO.enviar_transaccion(algod_client,stxn)

    return confirmed_txn, txid

# Congelar un activo
def congelar_activo(algod_client,congelador,congelador_llave_privada,asset_id,target):
    params = algod_client.suggested_params()

    txn = AssetFreezeTxn(
        sender=congelador,
        sp=params,
        index=asset_id,
        target=target,
        new_freeze_state=True
    )
    stxn = SEGUNDO.firmar_transaccion(txn,congelador_llave_privada)

    confirmed_txn, tx_id = SEGUNDO.enviar_transaccion(algod_client,stxn)
    return confirmed_txn, tx_id


# Revocar un activo
def revocar_activo(algod_client,asset_id,operador,operador_llave_privada,devolvedor,receiver):
    params = algod_client.suggested_params()

    txn = AssetTransferTxn(
        sender=operador,
        sp=params,
        receiver=receiver,
        amt=10,
        index=asset_id,
        revocation_target=devolvedor
    )
    stxn = SEGUNDO.firmar_transaccion(txn,operador_llave_privada)

    confirmed_txn, tx_id = SEGUNDO.enviar_transaccion(algod_client,stxn)
    return confirmed_txn, tx_id


# Destruir un activo
def destruir_activo(algod_client,asset_id,destructor, destructor_llave_privada):
    params = algod_client.suggested_params()

    txn = AssetConfigTxn(
        sender=destructor,
        sp=params,
        index=asset_id,
        strict_empty_address_check=False
        )

    stxn = SEGUNDO.firmar_transaccion(txn,destructor_llave_privada)

    confirmed_txn, tx_id = SEGUNDO.enviar_transaccion(algod_client,stxn)
    return confirmed_txn, tx_id