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

import config as cf
from App import model
import os
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________

def init():
    init = model.newInit()
    return init

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def Load_Data(init,decision):
    for filename in os.listdir(cf.data_dir):
        if filename.endswith(decision + ".csv"):
            print("Cargando archivo: " + filename)
            load(init, filename)
    return init


def load(init, direction):
    fileU = cf.data_dir + direction
    input_file = csv.DictReader(open(fileU, encoding="utf-8"), delimiter=",")
    for data in input_file:
        model.addRoute(init,data)
    return init

def totalConnections(Inite):
    return model.totalConnections(Inite)


def totalCommunities(Inite):
    return model.totalCommunities(Inite)

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def MejorHorario(Inite,h1,h2,c1,c2):
    return model.MejorHorario(Inite,h1,h2,c1,c2)