#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import numpy as np

def generar_bosque(n, m):
    return np.zeros((n, m), dtype="int16")

def suceso_aleatorio(p):
    return random.random() <= p

def  vecinos(bosque, pos):
    n, m = bosque.shape
    y, x = pos
    vecinos = [0]*8
    cont = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not(i == 0 and j == 0):
                vecinos[cont] = ((y + i) % n, (x + j) % m)
                cont += 1
    return vecinos
            
def brotes(bosque, p):
    for i in range(bosque.shape[0]):
        for j in range(bosque.shape[1]):
            if suceso_aleatorio(p):
                bosque[(i, j)] = 1