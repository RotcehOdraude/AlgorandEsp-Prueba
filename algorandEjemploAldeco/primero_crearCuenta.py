import algosdk

def generar_cuenta_llavePrivada():
    """
    Genera una nueva llave privada y la dirección de cuenta asociada.

    Returns:
        Tuple: Una tupla que contiene la llave privada generada y la dirección de cuenta.
    
    Raises:
        None.

    Example:
        private_key, account_address = generar_cuenta_llavePrivada()
    """
    # Generate a fresh private key and associated account address
    private_key, account_address = algosdk.account.generate_account()

    # Convert the private key into a mnemonic which is easier to use
    mnemonic = algosdk.mnemonic.from_private_key(private_key)

    print("Private key mnemonic: " + mnemonic)
    print("Account address: " + account_address)
    
    return private_key, account_address