#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import numpy as np

def generate_forest(n):
    return np.zeros(n, dtype = "int16")

def random_event(p):
    return random.random() <= p

def sprouts(forest, p):
    for i in range(len(forest)):
        if random_event(p):
            forest[i] = 1
        
def lightning(forest, f):
    for i in range(len(forest)):
        if random_event(f) and forest[i] == 1:
            forest[i] = -1

def neighbors(forest, pos):
    if (pos == 0):
        list = [1]
    elif (pos == len(forest)-1):
        list = [len(forest)-2]
    else:
        list = [pos-1, pos+1]
    
    return list

def propagate_neighbors(forest):
    propagated = False
    for i in range(len(forest)):
        if forest[i] == -1:
            for j in neighbors(forest, i):
                if forest[j] == 1:
                    forest[j] = -1
                    propagated = True
            
    return propagated

def propagate(forest):
    done = True
    while done == True:
        done = propagate_neighbors(forest)
        
def cleaning(forest):
    for i in range(len(forest)):
        if forest[i] == -1:
            forest[i] = 0
            
def dinamic(n, a, p, f):
    survivors = []
    forest = generate_forest(n)
    for i in range(a):
        count = 0
        sprouts(forest, p)
        lightning(forest, f)
        propagate(forest)
        cleaning(forest)
        for i in range(n):
            if forest[i] == 1:
                count += 1
        survivors.append(count)
        
    return sum(survivors)/a
    
def trees_survivors(f, a, n):
    average = []
    for p in np.arange(0, 1.01, 0.01):
        average.append(dinamic(n, a, p, f))
    #print(len(average))
    
    return average

def optimal_p(f, a, n):
    biggest = average[0]
    place = 0
    average = trees_survivors(f, a, n)
    for i in range(len(average)):
        if average[i] > biggest:
            biggest = average[i]
            place = i
    
    return f"{place}%"
        
    
