import ToolsHDF as TH
import os
print('4. Recortar')

class Recortar:

    def __init__(self):
        try:
            self.noLat = float(input('Ingrese la latitud mas al norte: '))
            self.suLat = float(input('Ingrese la latitud mas al sur: '))
            self.esLon = float(input('Ingrese la longitud mas al este: '))
            self.oeLon = float(input('Ingrese la longitud mas al oeste: '))
        except ValueError:
            print('ERROR: Se han ingresado valores no numericos.')

        if self.noLat<self.suLat or self.esLon<self.oeLon:
            print('ERROR: Error de limites')
        self.Recortar()

    def Recortar(self):
        entrada = 'Recortar/ARecortar/'
        salida = 'Recortar/Recortado/'+'Lon='+str(self.esLon)+'-'+str(self.oeLon)+'Lat='+str(self.noLat)+'-'+str(self.suLat)+'/'
        os.mkdir(salida)
        files = os.listdir(entrada)
        for x in files:
            if '.hdf' in x:
                datas, attrs = TH.get_data_from_HDF([x], entrada)
                TH.recortar(datas[0], attrs[0], self.suLat, self.noLat, self.oeLon, self.esLon, out=salida)