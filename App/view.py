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
from DISClib.ADT import list as lt
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
    print("3- REQUERIMENTO 1")
    print("4- REQUERIMENTO 2")
    print("0- Salir")


while True:
    printMenu()
    inputs = input("Seleccione una opcion para continuar:\n")
    if inputs == "1":
        analyzer = controller.init()
    elif inputs == "2":
        controller.Load_Data(analyzer)
    elif inputs == "3":
        ranking1 = int(
            input(
                "Digite el top que desea saber de compañías por cantidad de taxis afiliados:\n"
            )
        )
        ranking2 = int(
            input(
                "Digite el top que desea saber de compañías por servicios prestados:\n"
            )
        )
        req1 = controller.req1(analyzer, ranking1, ranking2)

        print("------------------------------")
        print("Cantidad de taxis de los servicios reportados:", req1["total taxis"])
        print("------------------------------")
        print("Cantidad de compañias con al menos 1 taxi:", req1["compañias taxi"])
        print("------------------------------")
        print(
            "El top:", ranking1, "de compañias con mayor cantidad de taxis registrados."
        )
        print("------------------------------")
        cont = 0
        ranking1_ = req1["ranking1"]
        for i in range(1, lt.size(ranking1_) + 1):
            cont += 1
            elemento = lt.getElement(ranking1_, i)
            print(cont, elemento["company"], ":", lt.size(elemento["value"]))
        print("------------------------------")
        print("El top:", ranking2, "de compañias que más servicios prestaron.")
        print("------------------------------")
        cont = 0
        ranking2_ = req1["ranking2"]
        for i in range(1, lt.size(ranking2_) + 1):
            cont += 1
            elemento = lt.getElement(ranking2_, i)
            print(cont, elemento["company"], ":", elemento["value"])
        print("------------------------------")

    elif inputs == "4":
        pass
    else:
        sys.exit(0)
sys.exit(0)
