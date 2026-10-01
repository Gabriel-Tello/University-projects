# -*- coding: utf-8 -*-
import random

def tirar_cubilete():
    dados = []
    i = 0
    while i<5:
        dados.append(random.randint(1,6))
        i += 1
    return (dados)

#print(tirar_cubilete())

def contar_elemento(lista, elemento):
    conteo = 0
    i = 0
    while i<len(lista):
        if lista[i] == elemento:
            conteo += 1
        i += 1
    return conteo

#print (contar_elemento([1,1,3,5,1], 1))
#print (contar_elemento([6,5,5,1,5], 6))

def puntos_por_unos(lista_dados):
    nr_de_unos = contar_elemento(lista_dados, 1)
    puntos = nr_de_unos * 100
    if nr_de_unos == 5:
        puntos += 10000
    elif nr_de_unos >= 3:
        puntos += 1000
    return puntos

#print(puntos_por_unos([1, 1, 3, 5, 1]))
#print(puntos_por_unos([6, 5, 5, 1, 5]))

def puntos_por_cincos(lista_dados):
    nr_de_cincos = contar_elemento(lista_dados, 5)
    puntos = nr_de_cincos * 50
    if nr_de_cincos == 5:
        puntos += 5000
    elif nr_de_cincos >= 3:
        puntos += 500
    return puntos

#print(puntos_por_cincos([1, 1, 3, 5, 1]))
#print(puntos_por_cincos([6, 5, 5, 1, 5]))

def total_puntos(lista_dados):
    #puntos = puntos_por_unos(lista_dados) + puntos_por_cincos(lista_dados)
    #return puntos
    return puntos_por_unos(lista_dados) + puntos_por_cincos(lista_dados)

#print(total_puntos([1, 1, 3, 5, 1]))
#print(total_puntos([6, 5, 5, 1, 5]))

def jugar_ronda(puntajes):
    i = 0
    while i<len(puntajes):
        puntajes[i] += total_puntos(tirar_cubilete())
        i += 1
    return puntajes 


"""
puntajes = [0, 0, 0]
i = 0
while i < 10:
    puntajes = jugar_ronda(puntajes)
    i += 1     
print(puntajes)
"""

#Lo de las tres " comillas lo aprendí por ahí

def hay_10mil(puntajes):
    i = 0
    gane_signo_de_pregunta = False
    while i < len(puntajes):
       if puntajes[i] >= 10000:
           gane_signo_de_pregunta = True
       i += 1
    return gane_signo_de_pregunta

#print(hay_10mil([100, 10000, 50, 0]))
#print(hay_10mil([11000, 9000, 550, 1200, 3450]))
#print(hay_10mil([50, 50, 100]))

def partida_completa(cant_jugadores):
    puntos = [0] * cant_jugadores
    cant_rondas = 0
    while hay_10mil(puntos) == False:
        jugar_ronda(puntos)
        cant_rondas += 1
    #print(puntos)
    return cant_rondas

#print(partida_completa(4))