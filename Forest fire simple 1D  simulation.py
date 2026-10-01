#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import numpy as np

def generar_bosque(n):
    return np.zeros(n, dtype = "int16")

def suceso_aleatorio(p):
    return random.random() <= p

def brotes(bosque, p):
    for i in range(len(bosque)):
        if suceso_aleatorio(p):
            bosque[i] = 1
        
def rayos(bosque, f):
    for i in range(len(bosque)):
        if suceso_aleatorio(f) and bosque[i] == 1:
            bosque[i] = -1

def vecinos(bosque, pos):
    if (pos == 0):
        lista = [1]
    elif (pos == len(bosque)-1):
        lista = [len(bosque)-2]
    else:
        lista = [pos-1, pos+1]
    
    return lista

def propagar_vecinos(bosque):
    propague = False
    for i in range(len(bosque)):
        if bosque[i] == -1:
            for j in vecinos(bosque, i):
                if bosque[j] == 1:
                    bosque[j] = -1
                    propague = True
            
    return propague

def propagar(bosque):
    ya_ta = True
    while ya_ta == True:
        ya_ta = propagar_vecinos(bosque)
        
def limpieza(bosque):
    for i in range(len(bosque)):
        if bosque[i] == -1:
            bosque[i] = 0
            
def dinamica(n, a, p, f):
    sobrevivientes = []
    bosque = generar_bosque(n)
    for i in range(a):
        cuenta = 0
        brotes(bosque, p)
        rayos(bosque, f)
        propagar(bosque)
        limpieza(bosque)
        for i in range(n):
            if bosque[i] == 1:
                cuenta += 1
        sobrevivientes.append(cuenta)
        
    return sum(sobrevivientes)/a
    
def arboles_sobrevivientes(f, a, n):
    promedio = []
    for p in np.arange(0, 1.01, 0.01):
        promedio.append(dinamica(n, a, p, f))
    #print(len(promedio))
    
    return promedio

def p_optimo(f, a, n):
    mayor = 0
    promedio = arboles_sobrevivientes(f, a, n)
    for i in range(len(promedio)):
        if promedio[i] > mayor:
            mayor = i/100
    
    return mayor
        
    