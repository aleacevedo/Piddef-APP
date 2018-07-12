import ToolsHDF as TH
import numpy as np
import os

entrada = 'Clorofila/AnioMedio/'
salida = 'Clorofila/AmplitudAnual/'

def get_min_and_max(arrays):
    """Busco el maximo y el minimo de cada pixel de las matrices que se encuentran
    dentro del array pasado por parametro"""
    return TH.search_max_or_min(arrays, np.nanmin), TH.search_max_or_min(arrays, np.nanmax)

def CalcularAmplitudAnual():
    data_anio, attr_anio = TH.get_data_from_HDF(os.listdir(entrada),entrada)
    min_anio, max_anio = get_min_and_max(data_anio)
    amp_anio = TH.calculate_amp(min_anio, max_anio)
    attr_anio = TH.organize_info(attr_anio)
    TH.write_data_to_HDF(array=amp_anio, attribute=attr_anio, folder=salida, name='AmplitudAnual.hdf')