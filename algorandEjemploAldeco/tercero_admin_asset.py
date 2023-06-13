import json
import base64
from algosdk.v2client import algod
from algosdk import account, mnemonic, encoding
from algosdk.transaction import *

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
def crear_activo(algod_client, accounts, sender = None, manager = None, reserve = None, freeze = None, clawback = None, unit_name = "Puma", asset_name = "Jeringas",url = "https://path/to/my/asset/details", decimals = 0):
    """
    Esta funcion crea una transacción y configura un activo.

    Args:
        algod_client: Cliente Algod de Algorand utilizado para realizar transacciones.
        accounts: Lista de cuentas involucradas en la transacción.
        sender: Dirección del remitente de la transacción (opcional). Si no se proporciona, se utilizará accounts[1][DIRECCION_DE_CUENTA_X].
        manager: Dirección del administrador del activo (opcional). Si no se proporciona, se utilizará accounts[0][DIRECCION_DE_CUENTA_X].
        reserve: Dirección de la reserva del activo (opcional). Si no se proporciona, se utilizará accounts[1][DIRECCION_DE_CUENTA_X].
        freeze: Dirección para congelar el activo (opcional). Si no se proporciona, se utilizará accounts[1][DIRECCION_DE_CUENTA_X].
        clawback: Dirección para revocar el activo (opcional). Si no se proporciona, se utilizará accounts[1][DIRECCION_DE_CUENTA_X].
        unit_name: Nombre de la unidad del activo (opcional). Valor por defecto: "MIMONEDA".
        asset_name: Nombre del activo (opcional). Valor por defecto: "MiMoneda".
        url: URL de detalles del activo (opcional). Valor por defecto: "https://path/to/my/asset/details".
        decimals: Número de decimales del activo (opcional). Valor por defecto: 0.

    Returns:
        Una transacción sin firmar (unsigned_txn) para configurar el activo.
    """
    # Obtener parámetros de red para transacciones antes de cada transacción.
    params = algod_client.suggested_params()
    params.fee = 1000
    params.flat_fee = True

    unsigned_txn = AssetConfigTxn(
        sender = accounts[0][DIRECCION_DE_CUENTA_X] if sender is None else sender,
        sp = params,
        total = 1000,
        default_frozen = False,
        unit_name = unit_name,
        asset_name = asset_name,
        manager = accounts[1][DIRECCION_DE_CUENTA_X] if manager is None else manager,
        reserve = accounts[1][DIRECCION_DE_CUENTA_X] if reserve is None else reserve,
        freeze = accounts[1][DIRECCION_DE_CUENTA_X] if freeze is None else freeze,
        clawback = accounts[1][DIRECCION_DE_CUENTA_X] if clawback is None else clawback,
        url = url,
        decimals = decimals
    )
    
    return unsigned_txn

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
        pendig_tx = algod_client.pending_transaction_info(tx_id)
        asset_id = pendig_tx["asset-index"]

        print_created_asset(algod_client, sender, asset_id)
        print_asset_holding(algod_client, sender, asset_id)
    except Exception as e:
        print(e)

'''
# Modificando un activo

params = algod_client.suggested_params()

txn = AssetConfigTxn(
    sender=accounts[1],
    sp=params,
    index=asset_id,
    manager=accounts[0],
    reserve=accounts[1],
    freeze=accounts[1],
    clawback=accounts[1])
stxn = txn.sign(SKs[1])

try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))

except Exception as err:
    print(err)
print_created_asset(algod_client, accounts[0], asset_id)

# OPT-IN

params = algod_client.suggested_params()

account_info = algod_client.account_info(accounts[2])
holding = None
idx = 0
for my_account_info in account_info['assets']:
    scrutinized_asset = account_info['assets'][idx]
    idx = idx + 1
    if (scrutinized_asset['asset-id'] == asset_id):
        holding = True
        break

if not holding:

    txn = AssetTransferTxn(
        sender=accounts[2],
        sp=params,
        receiver=accounts[2],
        amt=0,
        index=asset_id)
    stxn = txn.sign(SKs[2])

    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))

    except Exception as err:
        print(err)
    print_asset_holding(algod_client, accounts[2], asset_id)

# Transferir un activo

params = algod_client.suggested_params()

txn = AssetTransferTxn(
    sender=accounts[0],
    sp=params,
    receiver=accounts[2],
    amt=10,
    index=asset_id)
stxn = txn.sign(SKs[0])

try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))

except Exception as err:
    print(err)

print_asset_holding(algod_client, accounts[2], asset_id)

# Congelar un activo

params = algod_client.suggested_params()

txn = AssetFreezeTxn(
    sender=accounts[1],
    sp=params,
    index=asset_id,
    target=accounts[2],
    new_freeze_state=True
)
stxn = txn.sign(SKs[1])

try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
except Exception as err:
    print(err)

print_asset_holding(algod_client, accounts[2], asset_id)

# Revocar un activo

params = algod_client.suggested_params()

txn = AssetTransferTxn(
    sender=accounts[1],
    sp=params,
    receiver=accounts[0],
    amt=10,
    index=asset_id,
    revocation_target=accounts[2]
)
stxn = txn.sign(SKs[1])

try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
except Exception as err:
    print(err)

print("Account 3")
print_asset_holding(algod_client, accounts[2], asset_id)

print("Account 1")
print_asset_holding(algod_client, accounts[0], asset_id)

# Destruir un activo

params = algod_client.suggested_params()

txn = AssetConfigTxn(
    sender=accounts[0],
    sp=params,
    index=asset_id,
    strict_empty_address_check=False
    )

stxn = txn.sign(SKs[0])

try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
except Exception as err:
    print(err)
try:
    print("Account 3 must do a transaction for an amount of 0, ")
    print("with a close_assets_to to the creator account, to clear it from its accountholdings")
    print("For Account 1, nothing should print after this as the asset is destroyed on the creator account")
    print_asset_holding(algod_client, accounts[0], asset_id)
    print_created_asset(algod_client, accounts[0], asset_id)

except Exception as e:
    print(e)

'''