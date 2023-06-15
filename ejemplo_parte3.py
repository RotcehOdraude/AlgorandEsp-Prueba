import algorandEjemploAldeco.cuarto_atomic_transfer as CUARTO
### ADMINISTRA ACTIVOS CON TRANSFERECIAS ATÓMICAS ###
'''
Para crear este tipo de transacciones hay que seguir los siguientes pasos:

Crear las transacciones y/o transferencias de activos. Crear una transacción como se explicó en el Tema 2 sin firmar. Si como consecuencia de esta transacción se transferirá un activo también se de crear esta transferencia como se explicó en el Tema 3 sin firmar.
Agrupar las transacciones. Estas dos (o más) transacciones se agrupan creando un identificador para este grupo de transacciones.
Firmar las transacciones agrupadas. Se firman las transacciones agrupadas con sus respectivas llaves privadas.
Enviar las transacciones unidas a la red. Combinar las transacciones y enviarlas a la red.
Comprobar en el explorador que el grupo de transacciones se confirmo correctamente.
'''

### CREAR TRANSACCIONES ###
'''
Crear dos o más (hasta 16) transacciones sin firmar de cualquier tipo. Esto se hace siguiendo los pasos del Tema 2 o del Tema 3.
El ejemplo siguiente ilustra la Cuenta A enviando una transacción a la Cuenta C y la Cuenta B enviando una transacción a la Cuenta A.
'''

CUARTO.group_transactions()