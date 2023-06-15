from algosdk.v2client import algod
from algosdk import transaction
from algosdk import constants
import json
import base64

def conexion_con_cliente_algod(red = "algonode", algod_token = None, api_key = None):
    """
    Conexión con el cliente.

    Parámetros:
    - red (str): La red a la que se desea conectar. Opciones válidas: "algonode" (por defecto), "purestake".
    - algod_token (str): El token de autenticación para el cliente Algod para el cliente PureStake.
    - api_key (str): La clave de la API para el cliente PureStake.

    Retorna:
    - (AlgodClient) Regresa el cliente AlgodClient de la red especificada.

    Descripción:
    Esta función establece una conexión con un cliente de Algorand. Puede conectarse a la red AlgoNode o a PureStake,
    según la opción especificada en el parámetro 'red'. Si se elige PureStake, se deben proporcionar el token de autenticación
    'algod_token' y la clave de la API 'api_key'.

    Ejemplo:
    - conexion_con_cliente(red="purestake", algod_token="mi_token", api_key="mi_clave")

    """
    if (red == "purestake"):
        #Si usas PureStake

        #algod_client = algod.AlgodClient(
        #    algod_token="",
        #    algod_address="https://testnet-algorand.api.purestake.io/ps2",
        #    headers={"X-API-Key": "API KEY"}
        #)
        pass
    elif (red == "algonode"):
        print("Conectando con AlgoNode")
        #Si usas AlgoNode
        algod_client = algod.AlgodClient(
            algod_token = "",
            algod_address="https://testnet-api.algonode.cloud",
            headers={"X-API-Key": ""}
        )
        return algod_client
    else:
        print("Error en la red")


#Incluye la información de una de tus cuentas.
#Recuerda que los datos de la llave privada nunca deben estar en código
#Aquí lo hacemos para facilitar la explicación

####my_address = "TU DIRECCION"
####private_key = mnemonic.to_private_key("Tu mnemónico de 25 palabras")

#Verificando el balance de la cuenta
def verficar_balance_cuenta(algod_client, my_address):
    """
    Verifica el balance de una cuenta en la cadena de bloques utilizando el cliente de Algod.

    Parámetros:
    - algod_client (algod.AlgodClient): El cliente Algod utilizado para interactuar con la cadena de bloques.
    - my_address (str): La dirección de la cuenta cuyo balance se desea verificar.

    Retorna:
    (tuple)
    - saldo: El balance de la cuenta en microAlgos.
    - algo_client.account_info(my_address): La información de la cuenta.

    """
    try:
        account_info = algod_client.account_info(my_address)
        print("Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")
        return account_info.get('amount'), account_info
    except Exception as e:
        print(e)
        return -1
    

# build transaction
def crear_transaccion(algod_client, my_address, receiver_address, amount=1000000, note=""):
    """
    Crea una transacción de pago utilizando el cliente Algod.

    Parámetros:
    - algod_client (algod.AlgodClient): El cliente Algod utilizado para interactuar con la cadena de bloques.
    - my_address (str): La dirección de la cuenta emisora desde donde se realizará el pago.
    - receiver_address (str): La dirección de la cuenta receptora que recibirá el pago.
    - amount (int, opcional): La cantidad de microAlgos a enviar en la transacción (por defecto es 1,000,000).
    - note (str, opcional): Una nota asociada a la transacción (por defecto es una cadena vacía).

    Retorna:
    - transaction.PaymentTxn: La transacción de pago creada.
    - params: 

    """
    params = algod_client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = True
    params.fee = constants.MIN_TXN_FEE

    note = note.encode()
    unsigned_txn = transaction.PaymentTxn(my_address, params, receiver_address, amount, None, note)
    return unsigned_txn, params

# sign transaction
def firmar_transaccion(unsigned_txn, my_private_key):
    """
    Firma una transacción utilizando my clave privada.

    Parámetros:
    - unsigned_txn (transaction.Transaction): La transacción no firmada que se desea firmar.
    - my_private_key (str): La clave privada utilizada para firmar la transacción.

    Retorna:
    - transaction.SignedTransaction: La transacción firmada.

    """
    signed_txn = unsigned_txn.sign(my_private_key)
    return signed_txn

#submit transaction
def enviar_transaccion(algod_client,signed_txn):
    """
    Envía una transacción firmada a la red utilizando el cliente Algod.

    Parámetros:
    - algod_client (algod.AlgodClient): El cliente Algod utilizado para interactuar con la cadena de bloques.
    - signed_txn (transaction.SignedTransaction): La transacción firmada que se desea enviar.

    Retorna:
    - transaction.ConfirmedTransaction: La transacción confirmada por la red.

    """
    try:
        tx_id = algod_client.send_transaction(signed_txn)
        print("Successfully sent transaction with txID: {}".format(tx_id))

        # wait for confirmation
        confirmed_txn = transaction.wait_for_confirmation(algod_client, tx_id, 4)
        return confirmed_txn, tx_id
    except Exception as err:
        print("ERROR: ENTRE AL ERROR DEL TRY EXCEPT DE ENVIAR TRANSACCION")
        print(err)
        return None, None

def imprimir_transaccion(algod_client, my_address, account_info, confirmed_txn, amount, params):
    """
    Imprime información detallada sobre una transacción confirmada.

    Parámetros:
    - algod_client (algod.AlgodClient): El cliente Algod utilizado para interactuar con la cadena de bloques.
    - my_address (str): La dirección de la cuenta emisora de la transacción.
    - confirmed_txn (dict): Un diccionario que contiene la información de la transacción confirmada.
    - amount (int): La cantidad de microAlgos transferidos en la transacción.
    - params (algod.model.TransactionParams): Los parámetros de la transacción.

    No retorna ningún valor.

    """
    print("Transaction information: {}".format(json.dumps(confirmed_txn, indent=4)))
    print("Decoded note: {}".format(base64.b64decode(confirmed_txn["txn"]["txn"]["note"]).decode()))
    print("Starting Account balance: {} microAlgos".format(account_info.get('amount')))
    print("Amount transfered: {} microAlgos".format(amount))
    print("Fee: {} microAlgos".format(params.fee))
    account_info = algod_client.account_info(my_address)
    print("Final Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")
