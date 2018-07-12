from ToolsSST import AnioMedio

print('2. Trabajar con SST')

class Opciones():
    def __init__(self):
        print('1. Calcular Anio Medio')
        opcion = int(input('Ingrese una opcion: '))
        if opcion == 1:
            AnioMedio.CalcularAnioMedio()


