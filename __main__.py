import ToolsSST as TS
import ToolsClorofila as TC
import Graficar as Gr

def __init__():
    print('1. Trabajar con datos de clorofila.')
    print('2. Trabajar con datos de SST.')
    print('3. Graficar.')

    try:
        opcion = int(input('Ingrese una de las opciones anteriores.'))
    except ValueError:
        print('ERROR: Ah ingresado un valor no numerico')
        return -1

    if opcion<1 and opcion>3:
        print('Error: Ah ingresado un numero no valido')
        return -1

    if opcion==1:
        return TC()

    if opcion==2:
        return TS()

    if opcion==3:
        return Gr()