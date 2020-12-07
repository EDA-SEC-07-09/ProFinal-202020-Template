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
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error

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
        "Ranking Companies": None,
        "Ranking Servicios": None,
        "Taxis sin repetir": None,
    }
    Inite["Ranking Companies"] = lt.newList("ARRAY_LIST")
    Inite["Ranking Servicios"] = lt.newList("ARRAY_LIST")
    Inite["Taxis sin repetir"] = []
    return Inite


def req1(Inite, data):
    if data["taxi_id"] not in Inite["Taxis sin repetir"]:
        Inite["Taxis sin repetir"].append(data["taxi_id"])

    if lt.size(Inite["Ranking Companies"]) == 0:
        nodo_companies = crea_nodo_company(data)
        exist_in_rank = lt.newList("SINGLE_LINKED", compara_lista)  # SINGLE_LINKED
        lt.addLast(exist_in_rank, data["company"])
        lt.addLast(Inite["Ranking Companies"], exist_in_rank)
        lt.addLast(Inite["Ranking Companies"], nodo_companies)
    else:
        exist_in_rank = lt.getElement(Inite["Ranking Companies"], 1)
        presente = lt.isPresent(exist_in_rank, data["company"])
        if presente == 0:
            nodo_companies = crea_nodo_company(data)
            for i in range(2, lt.size(Inite["Ranking Companies"]) + 1):
                actual = lt.getElement(Inite["Ranking Companies"], i)
                if lt.size(nodo_companies["value"]) >= lt.size(actual["value"]):
                    lt.insertElement(Inite["Ranking Companies"], nodo_companies, i)
                    lt.insertElement(exist_in_rank, data["company"], i - 1)
                    break
                elif i == lt.size(Inite["Ranking Companies"]):
                    lt.addLast(Inite["Ranking Companies"], nodo_companies)
                    lt.addLast(exist_in_rank, data["company"])
                    break

        else:
            posicion = presente + 1
            elemento = lt.getElement(Inite["Ranking Companies"], posicion)

            if lt.isPresent(elemento["value"], data["taxi_id"]) == 0:
                lt.addLast(elemento["value"], data["taxi_id"])
                if posicion != 2:
                    Termina = True
                    while (posicion > 2) and Termina:
                        posicion -= 1
                        compara = lt.getElement(Inite["Ranking Companies"], posicion)
                        if lt.size(elemento["value"]) < lt.size(compara["value"]):
                            Termina = False

                            posicion += 1
                            lt.deleteElement(Inite["Ranking Companies"], presente + 1)
                            lt.insertElement(
                                Inite["Ranking Companies"], elemento, posicion
                            )
                            lt.deleteElement(exist_in_rank, presente)
                            lt.insertElement(
                                exist_in_rank, elemento["company"], posicion - 1
                            )

                        elif lt.size(elemento["value"]) > lt.size(compara["value"]):
                            lt.deleteElement(exist_in_rank, presente)
                            lt.insertElement(
                                exist_in_rank, elemento["company"], posicion - 1
                            )

                            lt.deleteElement(Inite["Ranking Companies"], presente + 1)
                            lt.insertElement(
                                Inite["Ranking Companies"], elemento, posicion
                            )
                            presente = posicion - 1

    if lt.isEmpty(Inite["Ranking Servicios"]):
        nodo_service = crea_nodo_service(data)
        exist_in_rank = lt.newList("ARRAY_LIST", compara_lista)  # SINGLE_LINKED
        lt.addLast(exist_in_rank, data["company"])
        lt.addLast(Inite["Ranking Servicios"], exist_in_rank)
        lt.addLast(Inite["Ranking Servicios"], nodo_service)
    else:
        exist_in_rank = lt.getElement(Inite["Ranking Servicios"], 1)
        presente = lt.isPresent(exist_in_rank, data["company"])
        if presente == 0:
            nodo_service = crea_nodo_service(data)
            for i in range(2, lt.size(Inite["Ranking Servicios"]) + 1):
                actual = lt.getElement(Inite["Ranking Servicios"], i)
                if nodo_service["value"] >= actual["value"]:
                    lt.insertElement(Inite["Ranking Servicios"], nodo_service, i)
                    lt.insertElement(exist_in_rank, data["company"], i - 1)
                    break
                elif i == lt.size(Inite["Ranking Servicios"]):
                    lt.addLast(Inite["Ranking Servicios"], nodo_service)
                    lt.addLast(exist_in_rank, data["company"])
                    break
        else:
            posicion = presente + 1
            elemento = lt.getElement(Inite["Ranking Servicios"], posicion)
            elemento["value"] += 1
            if posicion != 2:
                Termina = True
                while (posicion > 2) and Termina:
                    posicion -= 1
                    compara = lt.getElement(Inite["Ranking Servicios"], posicion)
                    if elemento["value"] < compara["value"]:
                        Termina = False
                        posicion += 1
                        lt.deleteElement(Inite["Ranking Servicios"], presente + 1)
                        lt.insertElement(Inite["Ranking Servicios"], elemento, posicion)
                        lt.deleteElement(exist_in_rank, presente)
                        lt.insertElement(
                            exist_in_rank, elemento["company"], posicion - 1
                        )
                    elif elemento["value"] > compara["value"]:
                        lt.deleteElement(exist_in_rank, presente)
                        lt.insertElement(
                            exist_in_rank, elemento["company"], posicion - 1
                        )
                        lt.deleteElement(Inite["Ranking Servicios"], presente + 1)
                        lt.insertElement(Inite["Ranking Servicios"], elemento, posicion)
                        presente = posicion - 1


# ==============================
# Funciones de consulta
# ==============================
def req1_return(Inite, ranking1, ranking2):
    para1 = 0
    para2 = 0
    ranking_servicios = lt.newList("ARRAY_LIST")
    ranking_taxis = lt.newList("ARRAY_LIST")
    cantidad_compañias_taxi = lt.size(Inite["Ranking Companies"]) - 1

    for i in range(2, lt.size(Inite["Ranking Companies"]) + 1):
        elemento = lt.getElement(Inite["Ranking Companies"], i)
        lt.addLast(ranking_taxis, elemento)
        para1 += 1
        if para1 == ranking1:
            break

    for i in range(2, lt.size(Inite["Ranking Servicios"]) + 1):
        elemento = lt.getElement(Inite["Ranking Servicios"], i)
        lt.addLast(ranking_servicios, elemento)
        para2 += 1
        if para2 == ranking2:
            break
    return {
        "ranking1": ranking_taxis,
        "ranking2": ranking_servicios,
        "compañias taxi": cantidad_compañias_taxi,
        "total taxis": len(Inite["Taxis sin repetir"]),
    }


# ==============================
# Funciones Helper
# ==============================
def crea_nodo_company(data):
    nodo_companies = {
        "company": data["company"],
        "value": lt.newList("SINGLE_LINKED", compara_lista),  # SINGLE_LINKED
    }
    lt.addLast(nodo_companies["value"], data["taxi_id"])
    return nodo_companies


def crea_nodo_service(data):
    nodo_service = {"company": data["company"], "value": 1}
    return nodo_service


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
