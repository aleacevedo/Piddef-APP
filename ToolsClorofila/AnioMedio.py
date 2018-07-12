import ToolsHDF as TH

entrada = 'Clorofila/Data/'
salida = 'Clorofila/AnioMedio/'

def CalcularAnioMedio():
    files = TH.organize_files(entrada,True)
    for mes in files:
        file_mes = []
        for file in files[mes].values():
            if not '.hdf' in file: pass
            file_mes.append(file[0])
            name = file_mes[0]
        data_mes, attr_mes = TH.get_data_from_HDF(file_mes,entrada)
        prom_mes = TH.calculate_prom(data_mes)
        attr_mes = TH.organize_info(attr_mes)
        TH.write_data_to_HDF(prom_mes,attr_mes,folder=salida,name=name)
    return 0