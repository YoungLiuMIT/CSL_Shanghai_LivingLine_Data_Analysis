# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 06:29:09 2018

@author: BentoScope_3
"""

##Here are the scripts for identifying the accurate xy coordinates for each indivudual with every single record
###Interval Tree and Hyperbola equation are two main methods applied here
###Take data of 20180728 for example

##packages used
import pandas as pd
import numpy as np
from pandas import DataFrame
import json 
import os
import statistics
from statistics import mean
from functools import reduce
from intervaltree import IntervalTree
import matplotlib
import matplotlib.pyplot as plt
from sympy import *
from sympy.solvers import solve
import csv

        
## set the working directory
Folder_Path = r'C:\Shanghai_Livingline\0728_json' #your own filepath
os.chdir(Folder_Path)
data_list = os.listdir(Folder_Path)

##read the individual_jsons for 20180728 and update them into one
IndividualJson={}
for i in range(len(data_list)):
    try:
        with open(data_list[i],'r',encoding='utf-8',errors='replace') as myfilei:
            datai=myfilei.readlines()
            for record in range(len(datai)):
                IndividualJson.update(json.loads(datai[record]))
    except IOError as e:
        print('Operation failed:%s') % e.strerror
key = list(IndividualJson.keys())            
## use IntervalTree for detecting all the interval records for each individual
## note that the singnal was sent every 1 minute on this condition

#generate all the intervals of all individuals for one day
allTrees={}
for ind in range(0,len(IndividualJson)):
    tree = IntervalTree()
    for o in IndividualJson[key[ind]]['observations']:
        tree[o['ts']-60000:o['ts']]={'AP':o['probe'],'rssi':o['rssi']}
    tree.split_overlaps()
    tree.merge_equals(data_reducer=lambda x,y:{'AP': x['AP']+','+y['AP'] ,'rssi': x['rssi']+','+y['rssi']})
    allTrees[key[ind]]=tree
    for node in sorted(tree):
        objall=node[2]['rssi'].split(',')
        first_item = True
        for item in objall:
            value_list = item.split(';')
            try:
                rssi_mean = np.mean([float(obj) for obj in value_list])
            except:
                print('error')
            if first_item:
                node[2]['rssi']=str(rssi_mean)
                first_item = False
            else:
                node[2]['rssi'] += ',' + str(rssi_mean)
                print(node)

#here is the information for apmac xy coordinates    
ap_xy_filepath=r'C:\Shanghai_Livingline'
apmac_info = pd.read_csv(ap_xy_filepath+'.\\apmac_xy_meter.csv')
apmac_info.columns = ['apmac_number','AP','r_coordinate X','r_coordinate Y']

#for ind_1 in range(0,len(IndividualJson)):
#    print(ind_1)
#    node_1 = sorted(allTrees[key[ind_1]])
#    for ind_ind_1 in node_1:
#        id_list = ind_ind_1[2]['AP'].split(',')
#        ind_ind_1[2]['AP_XY'] = []
#        for id_index in range(len(id_list)):
#              xy = apmac_info.loc[apmac_info['AP']==id_list[id_index], \
#                                       ['r_coordinate X', 'r_coordinate Y']].values.tolist()
#              if(len(xy) == 0):
#                  ind_ind_1[2]['AP_XY'].append(xy)
#              else:
#                  ind_ind_1[2]['AP_XY'].append(xy[0])    
#    print(node_1)

ap2Xy={ap: apmac_info.loc[apmac_info['AP']==ap][['r_coordinate X', 'r_coordinate Y']].values[0] for ap in apmac_info['AP'].values}
#agentList=[list(allTrees.items())[a][0] for a in range(1000)]
agentList=list(allTrees.keys())
for agent in agentList[:1000]:
    for interval in allTrees[agent]:
        apList=interval[2]['AP'].split(',')
        for ap in apList:
            try:
                apXY=ap2Xy[ap]
            except:
                apXY=[float('nan'), float('nan')]
            # TODO: save apXY wherever you want
            
    
## we divide all the records into three categories: 
    ### connection_once is the record connected to one device at the certain interval in which situation we define the location of the individual to be the foot point from the device to the road center axis
    ### connection_twice is the record connected to two devices at the certain interval in which situation we use hyperbola method and define the location of the individual to be the intersection point from the stronger point to the road center axis
    ### connection_morethan_twice is the record connected to more than two devices at the certain interval in which situation we use hyperbola method and draw the hyperbola of devices whose rssi ranked last 1,2,3 and define the intersection of these two hyperbolas to be the individual location
for ind_2 in range(0,len(node_first)):
    connection = node_1[ind_2]
    if len(connection[2]['AP'].split(',')) == 1:
        print(connection)
            ind_xy=[str(connection[2]['AP_XY'][0][0]),-107.1032655]
            connection[2]['ind_xy'] = []
            connection[2]['ind_xy'].append(ind_xy)
    #    else:
    #        connection[2]['ind_xy'] = []
        print(connection)
#            print (test(connection_once[2]))
#    for ind_3 in range(0,len(connection)):
#        connection_1 = node_1[ind_3]
    elif len(connection[2]['AP'].split(',')) == 2:
        AP1_xy=connection[2]['AP_XY'][0]
        AP2_xy=connection[2]['AP_XY'][1]
        AP1_rssi=connection[2]['rssi'].split(',')[0]
        AP2_rssi=connection[2]['rssi'].split(',')[1]
        h =mean([float(AP1_xy[0]),float(AP2_xy[0])]) 
        k =mean([float(AP1_xy[1]),float(AP2_xy[1])])
        a = np.exp(float(AP1_rssi)/float(AP2_rssi))/2
        c = np.sqrt((float(AP1_xy[0])-float(AP2_xy[0]))**2 - (float(AP1_xy[1])-float(AP2_xy[1]))**2)/2
        b = np.sqrt(c**2-a**2)
        x,y = symbols('x y')
        connection_twice = solve([((x-h)**2/a**2)-((y-k)**2/b**2)-1,y+107.1032655])
        x_list = []
        for i in range(len(connection_twice)):
            x_list.append(float(connection_twice[i][x]))
        if len(x_list) != 0:
            ind_xy = [mean(x_list),-107103.2655]
            connection[2]['ind_xy'] = ind_xy
#        print(connection)
#            if float(AP1_rssi) < float(AP2_rssi):
#                ind_xy=[str(min(connection_twice[i][x])),str(connection_twice[i][y])]
#            else:
#                ind_xy=[str(max(connection_twice[i][x])),str(connection_twice[i][y])] 
#            connection[2]['ind_xy'].append(ind_xy)
    elif len(connection[2]['AP'].split(',')) > 2:
        AP1_xy=connection[2]['AP_XY'][np.argsort(connection[2]['rssi'].split(','))[0]]
        AP2_xy=connection[2]['AP_XY'][np.argsort(connection[2]['rssi'].split(','))[1]]
        AP3_xy=connection[2]['AP_XY'][np.argsort(connection[2]['rssi'].split(','))[2]]
        AP1_rssi=sorted(connection[2]['rssi'])[0]
        AP2_rssi=sorted(connection[2]['rssi'])[1]
        AP3_rssi=sorted(connection[2]['rssi'])[2]
        
        h1 =mean([float(AP1_xy[0]),float(AP2_xy[0])]) 
        k1 =mean([float(AP1_xy[1]),float(AP2_xy[1])])
        a1 = np.exp(float(AP1_rssi)/float(AP2_rssi))/2
        c1 = np.sqrt((float(AP1_xy[0])-float(AP2_xy[0]))**2 - (float(AP1_xy[1])-float(AP2_xy[1]))**2)/2
        b1 = np.sqrt(c**2-a**2)
        
        h2 =mean([float(AP2_xy[0]),float(AP3_xy[0])]) 
        k2 =mean([float(AP2_xy[1]),float(AP3_xy[1])])
        a2 = np.exp(float(AP2_rssi)/float(AP3_rssi))/2
        c2 = np.sqrt((float(AP2_xy[0])-float(AP3_xy[0]))**2 - (float(AP2_xy[1])-float(AP3_xy[1]))**2)/2
        b2 = np.sqrt(c**2-a**2)
        ind_xy=[]
        x,y = symbols('x y')
        connection_morethan_twice=solve([((x-h)**2/a1**2)-((y-k)**2/b1**2)-1,((x-h)**2/a2**2)-((y-k)**2/b2**2)-1])
        x_list = []
        y_list = []
        for i in range(len(connection_morethan_twice)):
            x_list.append(float(connection_morethan_twice[i][x]))
            y_list.append(float(connection_morethan_twice[i][y]))
        if len(x_list) != 0 & len(y_list) != 0:
            ind_xy = [mean(x_list),mean(y_list)]
            connection[2]['ind_xy'] = ind_xy
    else:
        connection[2]['ind_xy'] = []
print(node_1)

