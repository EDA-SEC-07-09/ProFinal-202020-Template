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
    Inite={"Graph":None}
    Inite["Graph"] = gr.newGraph(
        datastructure="ADJ_LIST",
        directed=True,
        size=1000,
        comparefunction=compareStations,
    )
    return Inite

def addRoute(Inite,Route):
    origin=Route["pickup_community_area"]
    destination=Route["dropoff_community_area"]
    initdate=Route["trip_start_timestamp"]
    enddate=Route["trip_end_timestamp"]
    d=Route["trip_seconds"]
    if d!="":
        tam=len(d)
        r=tam-2
        df=d[:r]
        duration=int(df)
    t1=initdate[11:]
    t2=enddate[11:]
    time1=t1[:5]
    time2=t2[:5]
    if time2!="" and time1!="" and origin!="" and destination!="" and origin!=destination and d!="":
        init=origin+"-"+time1
        dest=destination+"-"+time2
        addCommunity(Inite,init)
        addCommunity(Inite,dest)
        addConnection(Inite,init,dest,duration)
    return Inite

def addCommunity(Inite,community):
    if not gr.containsVertex(Inite["Graph"],community):
        gr.insertVertex(Inite["Graph"],community)
    return Inite

def addConnection(Inite,community1,community2,duration):
    edge=gr.getEdge(Inite["Graph"],community1,community2)
    if edge is None:
        gr.addEdge(Inite["Graph"],community1,community2,duration)
        edge=gr.getEdge(Inite["Graph"],community1,community2)
        edge["division"]=1
    else:
        duracion=incremental(edge["weight"],edge["division"],duration)
        edge["division"]+=1
        edge["weight"]=duracion
    return Inite
    
# ==============================
# Funciones de consulta
# ==============================
def totalConnections(Inite):
    return gr.numEdges(Inite["Graph"])


def totalCommunities(Inite):
    return gr.numVertices(Inite["Graph"])
        
        
        


# ==============================
# Funciones Helper
# ==============================
def incremental(promediada, division, suma):
    promedio_nuevo = ((promediada * division) + suma) / (division + 1)
    return promedio_nuevo
# ==============================
# Funciones de Comparacion
# ==============================
def compareStations(estacion1, estacion2):
    estacion2 = me.getKey(estacion2)
    if estacion1 == estacion2:
        return 0
    elif estacion1 > estacion2:
        return 1
    else:
        return -1