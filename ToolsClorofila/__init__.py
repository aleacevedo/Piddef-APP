from ToolsClorofila import AnioMedio, AmplitudAnual

print("1. Trabajar con Clorofila")

class Opciones:

    opciones = ['1. Calcular Año Medio', '2. Calcular Amplitud del Año Medio', '3. Calcular Anomalias con respecto al Año Medio']

    def __init__(self):
        for x in self.opciones:
            print(x)

        try:
            elegida = int(input('Eliga una de las opciones anteriores: '))
        except ValueError:
            print('ERROR: La opcion elegida no es numerica')


        if elegida<1 and elegida>len(self.opciones):
            print('ERROR: La opcion elegida esta fuera de rango')

        if elegida == 1:
            AnioMedio.CalcularAnioMedio()

        if elegida == 2:
            AmplitudAnual.CalcularAmplitudAnual()


