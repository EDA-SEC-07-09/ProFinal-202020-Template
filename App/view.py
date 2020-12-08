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


import sys
import config
from App import controller
from DISClib.ADT.graph import gr
from DISClib.ADT import stack
import timeit
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________

recursionLimit = 1000000

# ___________________________________________________
#  Menu principal
# ___________________________________________________

"""
Menu principal
"""

def printMenu():
    print("Bienvenido")
    print("1- Inicializar Analyzer")
    print("2- Cargar información en el Analyzer")
    print("3- Requerimiento A")
    print("4- Requerimiento C")
    print("0- Salir")

while True:
    printMenu()
    inputs = input("Seleccione una opcion para continuar:\n")
    if inputs == "1":
        analyzer = controller.init()
    elif inputs == "2":
        decision = input("Qué archivo desea cargar (small,medium,large) :\n")
        controller.Load_Data(analyzer,decision)
        numver=controller.totalCommunities(analyzer)
        numarc=controller.totalConnections(analyzer)
        print("Numero de vertices: " + str(numver))
        print("Numero de arcos: " + str(numarc))
        sys.setrecursionlimit(recursionLimit)
        print(gr.vertices(analyzer["Graph"]))
    else:
        sys.exit(0)
sys.exit(0)