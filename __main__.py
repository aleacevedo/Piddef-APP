import ToolsClorofila as TC
import ToolsSST as TS
import Graficar as Gr
import Recortar as Rc


def __init__():

    try:
        opcion = int(input('Ingrese una de las opciones anteriores: '))
    except ValueError:
        print('ERROR: Ah ingresado un valor no numerico')
        return -1

    if opcion<1 and opcion>4:
        print('Error: Ah ingresado un numero no valido')
        return -1

    if opcion==1:
        return TC.Opciones()

    if opcion==2:
        return TS.Opciones()

    if opcion==3:
        return Gr()

    if opcion==4:
        return Rc.Recortar()

__init__()