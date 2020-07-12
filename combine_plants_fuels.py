# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 19:58:54 2020

@author: .3
"""

import pandas as pd


plants = pd.read_csv(r"C:\Users\.3\Desktop\national_energy\allPlants_allFuels.csv")

plantCodes = list(set(plants['Plant Code']))


allResults = []
for pc in plantCodes:
    
    dfPlant = plants[plants['Plant Code'] == pc]
    
    plantState = dfPlant['State'].values[0]
    
    allFuels = []
    for i in range(1,7):
        
        dfPlantE = dfPlant[dfPlant['Energy Source '+str(i)].isna() == False]
        
        if len(dfPlantE) < 1:
            continue
        
        fuelsList = list(set(dfPlant['Energy Source '+str(i)]))
        allFuels = allFuels + fuelsList
         
    finalFuels = list(set(allFuels))
    
    allResults.append([pc,plantState,  finalFuels])
     
dfResults = pd.DataFrame(allResults, columns = ['plant_code', 'state', 'fuels'])
    
dfResults.to_csv('plants_fuels_together.csv', index = False)
     