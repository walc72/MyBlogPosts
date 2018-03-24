#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Koldo Pina
Date created: 18/03/2018
Python Version: 3.5
"""

import pandas as pd
import matplotlib.pyplot as plt

# Modelo "cincel y martillo"
import csv

with open('data_LR.csv', 'r') as f:
    reader = csv.reader(f, delimiter='|')
    OUTDOOR_TEMP = []
    ELECTRIC_POWER = []
    for index, row in enumerate(reader):
        if index == 0:
            header = row
        else:
            try:
                outNum = float(row[0].replace(",", "."))
            except:
                outNum = None
            OUTDOOR_TEMP.append(outNum)
            try:
                elecNum = float(row[1].replace(",", "."))
            except:
                elecNum = None
            ELECTRIC_POWER.append(elecNum)


def info(header, data_list):
    """
    :param header: lista con los encabezados de las columnas
    :param data_list: lista con las listas de datos de las columnas: [lista1, lista2, etc...]

    :return: diccionario de diccionarios de valores con tipo de dato, número de na, media, std, min, max de cada columna
    """
    from collections import defaultdict

    header = header
    columns = data_list
    values = defaultdict()
    for index, head in enumerate(header):
        aux = defaultdict()
        aux['clases'] = set([type(ele) for ele in columns[index]])
        aux['na'] = sum(1 for ele in columns[index] if ele == None)
        # media
        media = sum(ele for ele in columns[index] if ele != None) / len(columns[index])
        aux['media'] = media
        # std
        n = sum(1 for ele in columns[index] if ele != None)
        std = ((1 / (n - 1)) * sum((ele - media) ** 2 for ele in columns[index] if ele != None)) ** 0.5
        aux['std'] = std
        # minimo
        aux['min'] = min(ele for ele in columns[index] if ele != None)
        # maximo
        aux['max'] = max(ele for ele in columns[index] if ele != None)
        values[head] = aux
    return values

def visual(header, X, y):
    """

    :param header: Lista con los nombres de los encabezados
    :param X: Lista con los valores de la columna a colocar en el eje X
    :param y: Lista con los valores de la columna a colocar en el eje y
    :return: matplotlib figure plot
    """

    fs = 10  # fontsize
    fig, axs = plt.subplots(3, 2, figsize=(6, 6))
    plt.subplots_adjust(top=0.9, bottom=0.1, hspace=0.5, wspace=0.2, left=0.125, right=0.9)
    axs[0, 0].scatter(X, y, c='r', edgecolors=(0, 0, 0), alpha=0.2)
    axs[0, 0].set_title('Scatter %s vs %s' %(header[1], header[0]), fontsize=fs)
    axs[1, 0].hist(X, color='red')
    axs[1, 0].set_title('Hist %s' %header[0], fontsize=fs)
    axs[0, 1].hist2d(X, y)
    axs[0, 1].set_title('Hist 2D', fontsize=fs)
    axs[1, 1].hist(y, color='blue')
    axs[1, 1].set_title('Hist %s' %header[1], fontsize=fs)
    axs[2, 0].boxplot(X)
    axs[2, 0].set_title('Box %s' %header[0], fontsize=fs)
    axs[2, 1].boxplot(y)
    axs[2, 1].set_title('Box %s' %header[1], fontsize=fs)
    plt.show()



print ('_'*60 + 'INFO')
print (info(header, [OUTDOOR_TEMP, ELECTRIC_POWER]))

#Quitamos los nas
index_to_drop = [index for index, val in enumerate(ELECTRIC_POWER) if val is None]
ELECTRIC_POWER = [val for index, val in enumerate(ELECTRIC_POWER) if index not in index_to_drop]
OUTDOOR_TEMP = [val for index, val in enumerate(OUTDOOR_TEMP) if index not in index_to_drop]

print (info(header, [OUTDOOR_TEMP, ELECTRIC_POWER]))

