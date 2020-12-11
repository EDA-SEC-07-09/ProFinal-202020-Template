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
    Inite={"Graph":None,"vu1":None,"vu2":None}
    Inite["Graph"] = gr.newGraph(
        datastructure="ADJ_LIST",
        directed=True,
        size=1000,
        comparefunction=compareStations,
    )
    Inite["Inicio"]=m.newMap(maptype="PROBING",comparefunction=compareStations)
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
    if time2!="" and time1!="" and origin!="" and destination!="" and origin!=destination and d!="" and d!="0.0":
        init=origin+"-"+time1
        dest=destination+"-"+time2
        addCommunity(Inite,init)
        addCommunity(Inite,dest)
        addConnection(Inite,init,dest,duration)
        completeMap(Inite,origin,time1)
    return Inite

def completeMap(Inite,inicio,time):
    if not(m.contains(Inite["Inicio"],inicio)):
        lista=lt.newList("ARRAY_LIST",cmpfunction=compareRoutes)
        lt.addLast(lista,time)
        m.put(Inite["Inicio"],inicio,lista)
    else:
        l=m.get(Inite["Inicio"],inicio)
        lista=l["value"]
        if not lt.isPresent(lista,time):
            lt.addLast(lista,time)
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



def MejorHorario(Inite,h1,h2,c1,c2):
    ho1=datetime.datetime.strptime(h1,"%H:%M")
    ho2=datetime.datetime.strptime(h2,"%H:%M")
    a=m.get(Inite["Inicio"],c1)
    horas=a["value"]
    iterator=it.newIterator(horas)
    costo_menor=None
    hora1=None
    hora2=None
    alerta=False
    i_max=0
    while it.hasNext(iterator):
        i=0
        element=it.next(iterator)
        conversor=datetime.datetime.strptime(element,"%H:%M")
        alarm=False
        if ho1<=conversor<=ho2 and ho1<=ho2:
            buscar=c1+"-"+element 
            dijk=djk.Dijkstra(Inite["Graph"],buscar)
            element2=element
            llegada=c2+"-"+element
            if djk.hasPathTo(dijk,llegada):
                path=djk.pathTo(dijk,llegada)
                costo=djk.distTo(dijk,llegada)
                if costo_menor==None or costo<costo_menor:
                    hora1=element
                    hora2=element
                    costo_menor=costo
                    ruta=path
                if costo<=900:
                    alerta=True    
            while alarm==False and alerta==False and (i_max==0 or i<=i_max):
                i+=1
                hc=datetime.datetime.strptime(element2,"%H:%M")
                convertidor=datetime.timedelta(hours=hc.hour,minutes=hc.minute)
                suma=convertidor+datetime.timedelta(minutes=15)
                alm=str(suma)
                tam=len(alm)
                re=tam-3
                cor=alm[:re]
                ele2=datetime.datetime.strptime(cor,"%H:%M")
                e=str(ele2)
                el=e[11:]
                elem=el[:5]
                element2=str(elem)
                llegada=c2+"-"+element2
                if djk.hasPathTo(dijk,llegada):
                    path=djk.pathTo(dijk,llegada)
                    costo=djk.distTo(dijk,llegada)
                    if costo_menor==None or costo<costo_menor:
                        hora1=element
                        hora2=element2
                        costo_menor=costo
                        ruta=path
                        i_max=i
                    alarm=True
                if element2=="23:45":
                    i_max=i
                    alarm=True
        elif ho1>ho2:
            if (conversor>=ho1 and conversor>=ho2) or (conversor<=ho1 and conversor<=ho2):
                buscar=c1+"-"+element 
                dijk=djk.Dijkstra(Inite["Graph"],buscar)
                element2=element
                llegada=c2+"-"+element
                if djk.hasPathTo(dijk,llegada):
                    path=djk.pathTo(dijk,llegada)
                    costo=djk.distTo(dijk,llegada)
                    if costo_menor==None or costo<costo_menor:
                        hora1=element
                        hora2=element
                        costo_menor=costo
                        ruta=path
                    if costo<=900:
                        alerta=True
                while alarm==False and alerta==False and (i_max==0 or i<=i_max):
                    i+=1
                    hc=datetime.datetime.strptime(element2,"%H:%M")
                    convertidor=datetime.timedelta(hours=hc.hour,minutes=hc.minute)
                    suma=convertidor+datetime.timedelta(minutes=15)
                    if suma>=datetime.timedelta(days=1,hours=0,minutes=0):
                        alm=str(suma)
                        cor2=alm[7:]
                        tam=len(cor2)
                        re=tam-3
                        cor=cor2[:re]
                        ele2=datetime.datetime.strptime(cor,"%H:%M")
                        e=str(ele2)
                        el=e[11:]
                        elem=el[:5]
                        element2=str(elem)
                    else:
                        alm=str(suma)
                        tam=len(alm)
                        re=tam-3
                        cor=alm[:re]
                        ele2=datetime.datetime.strptime(cor,"%H:%M")
                        e=str(ele2)
                        el=e[11:]
                        elem=el[:5]
                        element2=str(elem)
                    llegada=c2+"-"+element2
                    if djk.hasPathTo(dijk,llegada):
                        path=djk.pathTo(dijk,llegada)
                        costo=djk.distTo(dijk,llegada)
                        if costo_menor==None or costo<costo_menor:
                            hora1=element
                            hora2=element2
                            costo_menor=costo
                            ruta=path
                        i_max=i
                        alarm=True
                    if element2==h1:
                        i_max=i
                        alarm=True
    if hora1!=None and hora2!=None and costo_menor!=None and ruta!=None:
        tupla=(hora1,hora2,costo_menor,ruta)
        return tupla
    else:
        return None
        

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

def compareRoutes(route1, route2):
    if route1 == route2:
        return 0
    elif route1 > route2:
        return 1
    else:
        return -1

