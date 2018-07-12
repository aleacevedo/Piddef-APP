import os
from pyhdf.SD import *
from matplotlib import path
import csv
import numpy as np
from datetime import datetime
from scipy.stats import iqr as iq

NaN = -32767

NOT_INFO = ["Processing Control", "Input Parameters", "Input Files"]
VIP_INFO = ["Start Day", "End Day", "Start Year", "End Year"]


def organize_files(hdf_ruta, transpuesto=False):
    """ Organizo todos los archivos .hdf que se encuentren en la carpeta hdf_path
    si transpose igual a false devuelvo un dicc del tipo dicc[anio][mes]:[files_names]
    si transpose igual a true devuelvo un dicc del tipo dicc[mes][anio]:[files_names]"""
    hdf_archivos = os.listdir(hdf_ruta)
    hdf_archivos.sort()
    dic = {}
    for archivo in hdf_archivos:
        if not archivo.endswith(".hdf"):
            continue

        indice = archivo.find('.')-6
        anio = int(archivo[indice:indice+4])
        mes = int(archivo[indice+4:indice+6])

        if transpuesto == True:
            if not mes in dic: dic[mes] = {}
            if not anio in dic[mes]: dic[mes][anio] = []
            dic[mes][anio].append(archivo)

        else:
            if not anio in dic: dic[anio] = {}
            if not mes in dic[anio]: dic[anio][mes] = []
            dic[anio][mes].append(archivo)

    return dic


def apply_fun_to_data(data, fun):
    index = np.logical_not(fun(data))
    data[index] = np.nan
    return data

def calculate_period(attribute):
    """ Recibo un diccionario con un array en sus VIP_INFO y lo devuelvo con
     su periodo """
    time = attribute[VIP_INFO[0]]
    attribute[VIP_INFO[0]] = 999
    for x in time :
        attribute[VIP_INFO[0]] = min(attribute[VIP_INFO[0]], x)
    time = attribute[VIP_INFO[1]]
    attribute[VIP_INFO[1]] = 0
    for x in time :
        attribute[VIP_INFO[1]] = max(attribute[VIP_INFO[1]], x)
    time = attribute[VIP_INFO[2]]
    attribute[VIP_INFO[2]] = 9999
    for x in time :
        attribute[VIP_INFO[2]] = min(attribute[VIP_INFO[2]], x)
    time = attribute[VIP_INFO[3]]
    attribute[VIP_INFO[3]] = 3
    for x in time :
        attribute[VIP_INFO[3]] = max(attribute[VIP_INFO[3]], x)
    return attribute

def organize_info(attributes):
    """ Recibo un array con los atributos de los archivos hdf y devulevo un solo
    dic de atributos con periodo total """
    res_attribute = {}
    for attribute in attributes:
        for key in attribute:
            if key in NOT_INFO:
                continue
            elif key in VIP_INFO:
                if not key in res_attribute: res_attribute[key] = []
                res_attribute[key].append(attribute[key])
            else:
                if not key in res_attribute:
                    res_attribute[key] = attribute[key]
    return calculate_period(res_attribute)


def search_max_or_min(arrays, fun):
    """Busco el maximo o el minimo segun la funcion pasada en el parametro fun
    de un array que posee las matrices de igual tamaño entre NaN y otro numero
    siempre prevalece el otro numero. Devulevo una matris con el maximo o minimo
    de cada pixel"""
    result = fun(list(arrays), 0)
    return result

def descomponer(numero):
        c = int(numero/100)
        d = int((numero-(c*100))/10)
        u = int(numero-(d*10)-(c*100))

        return str(c)+str(d)+str(u)

def name_generator(attribute, add):
    name  = attribute["Product Name"]
    nwname = str(attribute["Start Year"]) + descomponer(attribute["Start Day"]) + str(attribute["End Year"]) + descomponer(attribute["End Day"]) + "_"
    name = name[0] + nwname + name[16:43] + add + ".hdf"
    return name

def write_data_to_HDF(array, attribute = {}, name = "", folder = "ResAmp/", bands = 'l3m_data'):
    """ Crea un nuevo HDF en la carpeta ResAmp, con el nombre pasado por parametro
    o un nombre generado con sus attributos en caso contrario y con el array
     pasado por parametro como dataset y con los atributos pasados por parametro"""
    if "" == name:
        name = name_generator(attribute, name)
        attribute["Product Name"] = name
        file = SD(folder+name+"", SDC.WRITE|SDC.CREATE)
    else:
        if os.path.isfile(folder+name):
            file = SD(folder+name+"", SDC.WRITE)
        else:
            file = SD(folder+name+"", SDC.WRITE|SDC.CREATE)
    file.create(bands, SDC.FLOAT64, array.shape)
    data = file.select(bands)
    for x in range(len(array)):
        data[x] = array[x]
    for x in attribute:
        at = attribute[x]
        try:
            if(at.dtype == np.dtype('int16')  or at.dtype == np.dtype('int32') or at.dtype == np.dtype('uint8') or at.dtype == np.dtype('uint16') or type(at)==int):
                new_attr = file.attr(x)
                new_attr.set(SDC.INT32, int(at))
            elif(at.dtype == np.dtype('float32') or at.dtype == np.dtype('float64') or type(at) == float):
                new_attr = file.attr(x)
                new_attr.set(SDC.FLOAT64, at)
            else:
                at = np.str(at)
                file.__setattr__(x, at)
        except AttributeError:
            #at = np.str(at)
            file.__setattr__(x, at)
        except TypeError:
            print(type(at))
            print(x)
            print(at)
    print("Guardando: ",name)

def get_data_from_HDF(files, hdf_path):
    """ Ingreso un array con los nombres de los archivos y devulevo un array
    con la dataset de esos archivos y uno con los atributos de esos archivos"""
    arrays = []
    attributes = []
    for file_name in files:
        if not '.hdf' in file_name: continue
        print("Abriendo: ",file_name)
        path = hdf_path + "/" + file_name
        file = SD(path, SDC.READ)
        for data_set in file.datasets().keys():
            array = file.select(data_set).get()
            array = array.astype(float)
            array[array==NaN] = np.nan
            arrays.append(array)
            attributes.append(file.attributes())
    return arrays, attributes

def leap_year(year):
    """ Funcion auxiliar de julian_to_gregor que decide si el anio es biciesto"""
    return  ( year % 4 == 0 and year % 100 !=0 ) or year % 400 == 0

def julian_to_gregor(year, day):
    """ Pasa del anio juliano al gregoriano """
    leap = leap_year(year)
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if leap == True:
        days[1] = 29
    sum = 0
    for k, item in enumerate(days):
        sum += item
        if sum >= day:
            dd = item - (sum - day)
            mm = (k+1)
            dd = dd
            break
    return mm, year


def calculate_prom(arrays):
    """ Calcula el promedio de cada pixel de dos arrays"""
    for x in arrays:
        if(NaN in x[0]): x[x==NaN] = np.nan
    prom = np.nanmean(arrays, 0)
    return prom

def calculate_amp(arrayMin, arrayMax):
    """ Calcula la amplitud de cada pixel de dos arrays"""
    amp = []
    if NaN in arrayMin[0]: arrayMin[arrayMin == NaN] = np.nan
    if NaN in arrayMax[0]: arrayMax[arrayMax == NaN] = np.nan
    amp = [arrayMax, np.negative(arrayMin)]
    amp = np.nansum(amp,0)
    return amp

def recortar(data, attr, minLatNw, maxLatNw, minLonNw, maxLonNw, out='Recortes/'):
    """Recibe una array, data, a recortar y un diccionario con los atributos de dichos datos"""
    lonStep = attr['Longitude Step']
    latStep = attr['Latitude Step']
    maxLat = attr['Northernmost Latitude']
    minLat = attr['Southernmost Latitude']
    maxLon = attr['Easternmost Longitude']
    minLon = attr['Westernmost Longitude']
    minX = int(abs(minLon - minLonNw)/lonStep)
    maxX = int(abs(minLon - maxLonNw)/lonStep)
    #print("X: ", (minX,maxX))
    minY = int(abs(maxLat - maxLatNw)/latStep)
    maxY = int(abs(maxLat - minLatNw)/latStep)
    #print("Y: ", (minY, maxY))
    data = data[minY:maxY , minX:maxX]
    attr['Northernmost Latitude'] = maxLatNw
    attr['Southernmost Latitude'] = minLatNw
    attr['Easternmost Longitude'] = maxLonNw
    attr['Westernmost Longitude'] = minLonNw
    attr['Number of Lines'] = data.shape[0]
    attr['Number of Columns'] = data.shape[1]
    #print("Shape: ", data.shape )
    print(attr['Product Name'][:-1])
    write_data_to_HDF(data, attr, folder=out, name=attr['Product Name'][:-1])

def inpolygon(data, attr, polig):
    """ Recibe el poligono como una lista de tuplas con cada vertice, devuelve una lista con todos los puntos dentro del poligono """
    if polig == None: return True
    polig = np.array(polig)
    lonStep = attr['Longitude Step']
    latStep = attr['Latitude Step']
    noLat = attr['Northernmost Latitude']
    suLat = attr['Southernmost Latitude']
    esLon = attr['Easternmost Longitude']
    wsLon = attr['Westernmost Longitude']
    cord = []
    test = np.empty(data.shape, dtype = object)
    ny = data.shape[0]; nx = data.shape[1]
    i = 0
    for y in range(ny):
        for x in range(nx):
            i = i + 1
            lons = wsLon + (lonStep * x)
            lats = noLat - (latStep * y)
            test[y][x] = (lons,lats)
            cord.append((lons, lats))
    p = path.Path(polig)
    in_p = p.contains_points(cord)
    in_p = in_p.reshape(ny,nx)
    return in_p


def rename_MO(path):
    files = organize_files(path)
    for anio in files:
        for mes in files[anio]:
            for file in files[anio][mes]:
                old_name = path+file
                if len(str(mes))<2: new_name = path+file[0]+str(anio)+'0'+str(mes)+file[15:]
                else: new_name = path+file[0]+str(anio)+str(mes)+file[15:]
                os.rename(old_name,new_name)

def calc_anomalia(data, media):
    anomalia = []
    for x in data:
        anomalia.append(x-media)
    return anomalia

def read_poly(contorno):
    vertices = []
    with open(contorno) as csvfile:
        reader = csv.reader(csvfile)
        for linea in reader:
            vertices.append((float(linea[0]), float(linea[1])))
    return vertices

def calc_serie(archivos, path, vertices=None):
    l = len(archivos)
    x = 0
    while l > x:
        if not archivos[x].endswith('.hdf'):
            print('Borrando: ', archivos[x] )
            archivos.pop(x)
            x = x-1
        l = len(archivos)
        x = x + 1
    print(archivos[-1])
    index = archivos[0].find('.')-6
    desde = (int(archivos[0][index:index+4]),int(archivos[0][index+4:index+6]))
    hasta = (int(archivos[-1][index:index+4]),int(archivos[-1][index+4:index+6]))
    promedios = []
    mediana = []
    varianza = []
    iqr_l = []
    data, attr = get_data_from_HDF(archivos, path)
    poligono = inpolygon(data[0], attr[0], vertices)

    for x,y in zip(data,attr):
        x = x*y['Slope']
        promedios.append(np.nanmean(x[poligono]))
        mediana.append(np.nanmedian(x[poligono]))
        varianza.append(np.nanstd(x[poligono]))
        iqr_l.append(iq(x[poligono]))

    x = np.array([datetime(x, i, 1, 0, 0) for x in range(desde[0], hasta[0]+1) for i in range(1, 13)])
    dif_a = np.empty(desde[1]-1)
    dif_a[:] = np.nan
    dif_b = np.empty(12-hasta[1])
    dif_b[:] = np.nan
    promedios = np.concatenate([dif_a,promedios,dif_b])
    mediana = np.concatenate([dif_a, mediana, dif_b])
    varianza = np.concatenate([dif_a, varianza, dif_b])
    iqr_l = np.concatenate([dif_a, iqr_l, dif_b])

    return x, promedios, mediana, varianza, iqr_l