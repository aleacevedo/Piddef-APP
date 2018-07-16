import ToolsHDF as TH
import numpy as np
from scipy import stats
import os

entrada = 'Clorofila/DataCalibrar/'
salida = 'Clorofila/DataCalibrada/'

def calc_intercept_slopes(x, y):
    var1 = x
    var2 = y
    x = None
    y = None
    slope = []
    intercept = []
    allvar1 = []
    print("Genero matrices var1")
    for x in var1:
        allvar1.append(x.flatten())
    var1 = None
    allvar2 = []
    print("Genero matrices var2")
    for x in var2:
        allvar2.append(x.flatten())
    var2 = None
    allvar1 = np.matrix(allvar1).transpose()
    allvar2 = np.matrix(allvar2).transpose()
    print("Termino de generar matrices")
    print("Calculando intercepts y slopes")
    for x in range(len(allvar1)):
        if x%1000000 == 0: print(x)
        good = ~(np.isnan(allvar1[x]) | np.isnan(allvar2[x]))
        if allvar1[x][good].size > 0:
            sl_inter = stats.linregress(allvar1[x][good], allvar2[x][good])
            slope.append(sl_inter[0])
            intercept.append(sl_inter[1])
        else:
            slope.append(np.nan)
            intercept.append(np.nan)
    print("Final de la funcion")
    return slope, intercept

def Calibrar():
    files = TH.organize_files(entrada)
    AQ = []
    SW = []
    for anio in files:
        for mes in files[anio]:
            if len(files[anio][mes])>1:
                for x in files[anio][mes]:
                    if(x[0]=='A'): AQ.append(x)
                    if(x[0]=='S'): SW.append(x)
    print("Cargando archivos Aqua")
    datosAQ , attr = TH.get_data_from_HDF(AQ,entrada)
    print("Cargando archivos SeaWiss")
    datosSW, attr = TH.get_data_from_HDF(SW, entrada)
    slope, intercept = calc_intercept_slopes(np.log10(datosSW), np.log10(datosAQ))
    print(len(slope))
    print(len(intercept))
    hdf_files = os.listdir(entrada)
    for file in hdf_files:
        if file[0]=='A':
            data , attr = TH.get_data_from_HDF([file],entrada)
            data = np.log10(data[0].flatten())
            data = (data -intercept)/slope
            data = np.power(10,data)
            data = data.reshape(4080,4320)
            data[data>100] = np.nan
            TH.write_data_to_HDF(data, attr[0], name=file, folder=salida)