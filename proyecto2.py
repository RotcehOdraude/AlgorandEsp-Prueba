import algorandEjemploAldeco.primero_crearCuenta as PRIMERO
### CREACION DE CUENTAS INVOLUCRADAS EN EL PROYECTO ####
'''
1. (BM) Banco de Mexico: Este es el ente que creara la moneda digital a ser utilizada como dinero fiat.
2. (C) Cuenta ciudadanos: Este ente representara a un conjunto de ciudadanos que pagana sus impuestos a hacienda.
3. (S) SAT: Este ente representará al Servicio de Administración Tributaria, el cual es el encargado de recaudar los impuestos de los ciudadanos. Y redigirigir parte de lo recaudado a Hospitales Publicos.
4. (H) Hospital: Este ente representará a un Hospital Publico, el cual recibirá parte de los impuestos recaudados por el SAT. Además se encargara de la creacion de nuevos activos que reprentaran isumos medicos.
5. (P) Proveedores: Este ente se encargará de suministrar insumos medicos al Hospital. Recibiendo activos de una moneda y entregando activos de otro tipo, en este caso insumos médicos solicitaos por el Hospital.
6. (D) Doctor[a]: Este ente representará a un doctor o doctora que trabaja en el Hospital. El doctor recibirá activos de insumos medicos y los entregará a los pacientes.
7. (E) Enfermer[o|a]: Este ente representará a un enfermero o enfermera que trabaja en el Hospital. El enfermero recibirá activos de insumos medicos y los entregará a los pacientes.
'''

# Generando llave privada de cuenta A y su dirección
cuenta_A, _ = PRIMERO.generar_cuenta()

# Almacenando en un archivo de texto la llave privada y la dirección de la cuenta A
with open("cuentas.txt", "w") as archivo:
    archivo.write(f"{cuenta_A.llave_privada},{cuenta_A.direccion}\n")

    