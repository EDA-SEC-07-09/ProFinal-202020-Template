"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import orderedmap as om
from DISClib.ADT import list as lt
from DISClib.ADT import stack
from DISClib.Algorithms.Sorting import mergesort
from DISClib.DataStructures import listiterator as it
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
import datetime

assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------
# Funciones para agregar informacion al grafo
def newInit():
    Inite = {
        "mapa_companies": None,
        "Taxis sin repetir": None,
        "mapa_fecha": None,
    }
    Inite["mapa_fecha"] = om.newMap("BST", comparefunction=compareStations)
    Inite["mapa_companies"] = m.newMap(
        maptype="PROBING", comparefunction=compareStationsv2
    )
    Inite["Taxis sin repetir"] = []

    return Inite


def req1(Inite, data):
    if data["company"] == "":
        data["company"] = "Independent Owner"
    if data["taxi_id"] not in Inite["Taxis sin repetir"]:
        Inite["Taxis sin repetir"].append(data["taxi_id"])

    existe_compañia = m.get(Inite["mapa_companies"], data["company"])
    if existe_compañia == None:
        nodo_companies = crea_nodo_company(data)
        m.put(Inite["mapa_companies"], data["company"], nodo_companies)
    else:
        existe_compañia = me.getValue(existe_compañia)
        if data["taxi_id"] not in existe_compañia["value"]:
            existe_compañia["value"].append(data["taxi_id"])
        existe_compañia["servicios"] += 1


# ==============================
# Funciones de consulta
# ==============================


def req1_return(Inite, ranking1, ranking2):
    companies_orden = m.valueSet(Inite["mapa_companies"])
    services_orden = m.valueSet(Inite["mapa_companies"])

    mergesort.mergesort(services_orden, comparador_ascendente_services)  # SHELLSORT
    mergesort.mergesort(companies_orden, comparador_ascendente_taxis)  # SHELLSORT
    cantidad_compañias_taxi = m.size(Inite["mapa_companies"])
    top1 = lt.newList("ARRAY_LIST")
    top2 = lt.newList("ARRAY_LIST")
    for i in range(1, lt.size(companies_orden) + 1):
        elemento = lt.getElement(companies_orden, i)
        lt.addLast(top1, elemento)
        if i == ranking1:
            break
    for i in range(1, lt.size(services_orden) + 1):
        elemento = lt.getElement(services_orden, i)
        lt.addLast(top2, elemento)
        if i == ranking2:
            break
    return {
        "ranking1": top1,
        "ranking2": top2,
        "compañias taxi": cantidad_compañias_taxi,
        "total taxis": len(Inite["Taxis sin repetir"]),
    }


def nodo_taxi(data, total):
    taxi = {
        "taxi": data["taxi_id"],
        "puntos": float(data["trip_miles"]) / (total),
        "servicios": 1,
    }
    return taxi


def add_to_map(Inite, data):
    fechax = data["trip_start_timestamp"]
    fechax = fechax[:10]
    fechax = transformador_fecha(fechax)
    fecha = om.get(Inite["mapa_fecha"], fechax)
    if data["trip_total"] == "":
        data["trip_total"] = 0
    if data["trip_miles"] == "":
        data["trip_miles"] = 0
    millas = float(data["trip_miles"])
    total = float(data["trip_total"])

    if millas > 0 and total > 0:
        if fecha is None:
            new_map = m.newMap(maptype="PROBING", comparefunction=compareStationsv2)
            nodo = nodo_taxi(data, total)
            m.put(new_map, data["taxi_id"], nodo)
            om.put(Inite["mapa_fecha"], fechax, new_map)
        else:
            existe = m.get(me.getValue(fecha), data["taxi_id"])
            if existe is None:
                nodo = nodo_taxi(data, total)
                m.put(me.getValue(fecha), data["taxi_id"], nodo)
            else:
                existe = me.getValue(m.get(me.getValue(fecha), data["taxi_id"]))
                puntos = existe["puntos"]
                servicios = existe["servicios"]
                puntos_new = incrementalV2(puntos, servicios, total / millas)
                existe["puntos"] = puntos_new
                existe["servicios"] += 1


def consulta_puntos_PROV(Inite, fecha, top):

    fecha = transformador_fecha(fecha)
    mapa = me.getValue(om.get(Inite["mapa_fecha"], fecha))
    top_final = lt.newList("ARRAY_LIST")
    lista_ordenada = m.valueSet(mapa)
    mergesort.mergesort(lista_ordenada, comparador_ascendente)  # SHELLSORT
    for i in range(1, lt.size(lista_ordenada) + 1):
        a_ver = lt.getElement(lista_ordenada, i)
        lt.addLast(top_final, a_ver)
        if i == top:
            break
    return top_final


def consulta2(Inite, fecha_ini, fecha_fin, top2):
    fecha_fin = transformador_fecha(fecha_fin)
    fecha_ini = transformador_fecha(fecha_ini)
    datos_entre_medio = om.values(Inite["mapa_fecha"], fecha_ini, fecha_fin)

    mapa_intermedio = m.newMap(maptype="PROBING", comparefunction=compareStationsv2)
    for i in range(1, lt.size(datos_entre_medio) + 1):
        lista = lt.getElement(datos_entre_medio, i)
        lista = m.valueSet(lista)

        for e in range(1, lt.size(lista) + 1):
            elemento = lt.getElement(lista, e)
            existe = m.get(mapa_intermedio, elemento["taxi"])
            if existe is None:
                m.put(mapa_intermedio, elemento["taxi"], elemento)
            else:
                nodo_new = incrementalV3(me.getValue(existe), elemento)
                m.put(mapa_intermedio, nodo_new["taxi"], nodo_new)

    top_2 = lt.newList("ARRAY_LIST")
    mapa_intermedio_ordenado = m.valueSet(mapa_intermedio)
    mergesort.mergesort(mapa_intermedio_ordenado, comparador_ascendente)  # SHELLSORT

    for i in range(1, lt.size(mapa_intermedio_ordenado) + 1):
        elemento = lt.getElement(mapa_intermedio_ordenado, i)
        lt.addLast(top_2, elemento)
        if i == top2:
            break

    return top_2


# ==============================
# Funciones Helper
# ==============================
def transformador_fecha(fecha):
    fecha = datetime.datetime.strptime(fecha, "%Y-%m-%d")
    xd = fecha.date()
    return xd


def crea_nodo_service(data):
    nodo_service = {"company": data["company"], "value": 1}
    return nodo_service


def incrementalV2(sumado, servicios, a_sumar):
    puntos = ((sumado / servicios) + a_sumar) * (servicios + 1)
    return puntos


def incrementalV3(nodo_estaba, nodo_llega):
    puntos_estaba_sin_servicio = nodo_estaba["puntos"] / nodo_estaba["servicios"]

    puntos_llega_sin_servicio = nodo_llega["puntos"] / nodo_llega["servicios"]
    puntos_total = (puntos_estaba_sin_servicio + puntos_llega_sin_servicio) * (
        nodo_estaba["servicios"] + nodo_llega["servicios"]
    )
    taxi_new = {
        "taxi": nodo_estaba["taxi"],
        "puntos": puntos_total,
        "servicios": nodo_estaba["servicios"] + nodo_llega["servicios"],
    }
    return taxi_new


def transformador_hora(hora):
    hora = datetime.datetime.strptime(hora, "%H:%M:%S.%f")
    hora = hora.time()
    return hora


def posicion_123(lista, elemento):
    for i in range(1, lt.size(lista) + 1):
        encontrado = lt.getElement(lista, i)
        if elemento == encontrado:
            return i
    return 0


def crea_nodo_company(data):
    nodo_companies = {"company": data["company"], "value": [], "servicios": 1}
    nodo_companies["value"].append(data["taxi_id"])
    return nodo_companies


# ==============================
# Funciones de Comparacion
# ==============================


def compara_lista(dato1, dato2):
    if dato1 == dato2:
        return 0
    elif dato1 > dato2:
        return 1
    else:
        return -1


def comparador_ascendente(pos1, pos2):
    if pos1["puntos"] > pos2["puntos"]:
        return True
    return False


def comparador_ascendente_services(pos1, pos2):
    if pos1["servicios"] > pos2["servicios"]:
        return True
    return False


def comparador_ascendente_taxis(pos1, pos2):
    if len(pos1["value"]) > len(pos2["value"]):
        return True
    return False


def compareStations(estacion1, estacion2):
    if estacion1 == estacion2:
        return 0
    elif estacion1 > estacion2:
        return 1
    else:
        return -1


def compareStationsv2(estacion1, estacion2):
    estacion2 = me.getKey(estacion2)
    if estacion1 == estacion2:
        return 0
    elif estacion1 > estacion2:
        return 1
    else:
        return -1
