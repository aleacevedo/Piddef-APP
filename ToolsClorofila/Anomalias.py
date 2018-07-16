import ToolsHDF as TH
import os
import numpy as np

entrada='Clorofila/Data/'
anioMedio = 'Clorofila/AnioMedio/'
salida = 'Clorofila/Anomalias/'


def CalcularAnomalias():
    files_s = TH.organize_files(entrada, True)
    files_m = TH.organize_files(anioMedio, True)
    for mes in files_s:
        data_s = []
        for anio in files_s[mes]:
            for x in files_s[mes][anio]:
                data_s.append(x)
        data, attr = TH.get_data_from_HDF(data_s, entrada)
        data_media, attr_b = TH.get_data_from_HDF(list(files_m[mes].values())[0], anioMedio)
        anomalias = TH.calc_anomalia(data, data_media[0])
        for x in range(len(anomalias)):
            name = data_s[x][:8]+'Anomalias_'+data_s[x][8:]
            TH.write_data_to_HDF(anomalias[x], attr[x], name=name, folder=salida)
