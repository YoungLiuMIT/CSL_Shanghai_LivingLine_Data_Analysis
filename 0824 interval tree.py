# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 18:01:56 2018

@author: Weiting Xiong
"""
from intervaltree import IntervalTree
import json
import os 
import pandas as pd
from pandas import DataFrame
from functools import reduce
import statistics
from statistics import mean
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

Folder_Path = r'E:\jupyter3\raw data\0728_json' #your own filepath
os.chdir(Folder_Path)
with open ('indi072800.json','r', encoding='utf-8',errors='replace') as myfile0:
    data0 = myfile0.readlines()
    IndividualJson0=[json.loads(data0[i]) for i in range(len(data0))]
with open ('indi072801.json','r', encoding='utf-8',errors='replace') as myfile1:
    data1 = myfile1.readlines()
    IndividualJson1=[json.loads(data1[i]) for i in range(len(data1))]   
with open ('indi072802.json','r', encoding='utf-8',errors='replace') as myfile2:
    data2 = myfile2.readlines()
    IndividualJson2=[json.loads(data2[i]) for i in range(len(data2))]
with open ('indi072803.json','r', encoding='utf-8',errors='replace') as myfile3:
    data3 = myfile3.readlines()
    IndividualJson3=[json.loads(data3[i]) for i in range(len(data3))]   
with open ('indi072804.json','r', encoding='utf-8',errors='replace') as myfile4:
    data4 = myfile4.readlines()
    IndividualJson4=[json.loads(data4[i]) for i in range(len(data4))]
with open ('indi072805.json','r', encoding='utf-8',errors='replace') as myfile5:
    data5 = myfile5.readlines()
    IndividualJson5=[json.loads(data5[i]) for i in range(len(data5))] 
    
IndividualJson = {}
for d in [IndividualJson0[0], IndividualJson1[0], IndividualJson2[0], IndividualJson3[0], IndividualJson4[0], IndividualJson5[0]]:
  IndividualJson.update(d)
key = list(IndividualJson.keys())
#key
#len(key)
#for ind in range(0, len(key)):
allTrees={}
for ind in range(0, 100):
    tree = IntervalTree()
    for o in IndividualJson[key[ind]]['observations']:
        tree[o['ts']-60000:o['ts']]={'AP':o['probe'], 'rssi':o['rssi']}
    tree.split_overlaps()
    tree.merge_equals(data_reducer=lambda x, y : {'AP': x['AP']+','+y['AP'] ,'rssi': x['rssi']+','+y['rssi']})
#    print(tree)
#    type(tree)
#    print(sorted(tree)[0]['rssi'])
    allTrees[key[ind]]=tree
    for node in sorted(tree):
        objall=node[2]['rssi'].split(',')
        first_item = True
        for item in objall:
            value_list = item.split(';')
            try:
                rssi_mean = np.mean([float(obj) for obj in value_list])
            except:
                print("error")
            if first_item:
                node[2]['rssi'] = str(rssi_mean)
                first_item = False
            else:
                node[2]['rssi'] += ',' + str(rssi_mean)
        print(node) 
#key=list(allTrees.keys())
#for each interval, 
#if the number of AP connection is one, so the individual location is the pedal from the connected probe to the street center line;
#if the number of AP connection is twice, so the individual location is defined by one of the hyperbola lines which is near the stronger-rssi connceted probe;
#if the number of AP connection is more than twice, so the individual location if defined by the probes which ranks top 3 rin rssi, we can generate two hyperbolas with the 1-2 and 2-3 probe connection respectively;

## generate the street center axis in autocad
from pyautocad import Autocad, APoint
acad = Autocad(create_if_not_exists=True)
acad.prompt("Hello, Autocad from Python\n")
print(acad.doc.Name)
p1 = APoint(459904.7957,-107103.2655)
p2 = APoint(747599.6862,-107103.2655)
street_center_axis=acad.model.AddLine(p1,p2)



def hyper(AP1_xy, AP2_xy, AP1_rssi, AP2_rssi):
#    parameter=[]
#    for a in range(len(key)):
#       AP1_xy=allTrees[key[a]]['AP']
#       AP1_rssi==allTrees[a]['rssi']
    h =mean([float(AP1_xy[0]),float(AP2_xy[0])]) 
    k =mean([float(AP1_xy[1]),float(AP2_xy[1])])
    a = np.exp(AP1_rssi/AP2_rssi)/2
    c = np.sqrt((float(AP1_xy[0])-float(AP2_xy[0]))**2 - (float(AP1_xy[1])-float(AP2_xy[1]))**2)/2
    b = np.sqrt(c**2-a**2)


x_list = range(0,200,2)
y_list = []
for x in x_list:
    y_list.append(b*(1-2*((x-h)**2/a**2)+((x-h)**4/a**4)) + k)
axes()
plt.contour(x_list, y_list)
plt.show()
plt.figure()
plt.plot(x_list, y_list)