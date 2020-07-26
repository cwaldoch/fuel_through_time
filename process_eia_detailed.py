# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 10:13:13 2020

@author: .3
"""

import eia
import pandas as pd
import pdb 
import numpy as np


def retrieve_time_series(api, series_ID):
    """
    Return the time series dataframe, based on API and unique Series ID
    """
    #Retrieve Data By Series ID 
    series_search = api.data_by_series(series=series_ID)
    ##Create a pandas dataframe from the retrieved time series
    df = pd.DataFrame(series_search)
    return df


localPath = r"C:\Users\.3\Desktop\fuel_through_time\\"

eia860 = pd.read_csv(localPath+"eia860.csv")
plantRef = pd.read_csv(localPath+"plants_fuels_together.csv")
vaPlants = plantRef[plantRef['state'] == 'VA']
plants = pd.read_csv(r"C:\Users\.3\Desktop\national_energy\allPlants_allFuels.csv")

va860 = plants[plants['State'] == 'VA']

refDict = {}
for col in va860.columns:
    refDict[col] = np.array(va860[col])

#codeArray = np.array
#nameArray


plantCodes = list(set(vaPlants['plant_code']))
with open(localPath+"apiKey.txt", 'r') as txt:
    apiKey = txt.read()

api = eia.API(apiKey)

"""
distillate fuel oil : combined-cycle combustion turbine part : annual
ELEC.PLANT.CONS_EG_BTU.3797-DFO-CT.A

Maybe eventually try to identify odd disparities between cons for E and gen,
never really question those values.

distillate fuel oil : combined-cycle combustion turbine part : annual
ELEC.PLANT.GEN.3797-DFO-CT.A
"""

allPlants = []
for i in range (0,len(refDict[va860.columns[0]])):

    plantCode = refDict['Plant Code'][i]
    plantName = refDict['Plant Name'][i]
    plantState = refDict['State'][i] 
    plantCounty = refDict['County'][i]
    plantLat = refDict['lat'][i]
    plantLon = refDict['lon'][i]
    opYear = refDict['Operating Year'][i]
    retYear = refDict['Retirement Year'][i]
    pMover = refDict['Prime Mover'][i]
    tech = refDict['Technology'][i]
    
    
    for n in range(1,7):
        
        fuel = refDict['Energy Source '+str(n)][i]
        
        if fuel != 'nan' and type(fuel) == str:
            
           # Example series id
            #ELEC.PLANT.GEN.3772-WAT-ALL.A
            
            serGen1 = 'ELEC.PLANT.GEN.'
            try:
                serGen2 = serGen1+str(plantCode)+'-'+fuel+'-'+pMover+'.A'
            except TypeError:
                pdb.set_trace()
            
            serCons1 = 'ELEC.PLANT.CONS_EG_BTU.'
            serCons2 = serCons1+str(plantCode)+'-'+fuel+'-'+pMover+'.A'
            
            for seriesID in [[serGen2, 'MWh'], [serCons2, 'MMBtu']]:
                try:
                    df = retrieve_time_series(api, seriesID[0])
                except KeyError:
                    # these errors should only occur for plants that haven't been
                    # built yet or doesn't have some characteristic.
                    print('Plant not in yet or characteristic wrong.')
                    continue
                    
                dfCol = df.columns[0]
                #plantName = dfCol.split(': ')[1].split('(')[0]
                df = df.reset_index()
                df = df.rename(columns={dfCol:'gen', 'index':'year'})
                #df['plant_name'] = [plantName]*len(df)
                
                df['unit'] = [seriesID[1]]*len(df)
                df['lat'] = [plantLat]*len(df)
                df['lon'] = [plantLon]*len(df)
                df['fuel'] = [fuel]*len(df)
                df['plantCode'] = [plantCode]*len(df)
                df['plantName'] = [plantName]*len(df)
                df['plantState'] = [plantState]*len(df)
                df['plantCounty'] = [plantCounty]*len(df)
                df['opYear'] = [opYear]*len(df)
                df['retYear'] = [retYear]*len(df)
                df['pMover'] = [pMover]*len(df)
                df['tech'] = [tech]*len(df)
                
                
                allPlants.append(df)
            
dfAll = pd.concat(allPlants, ignore_index = True)

dfAll.to_csv('ANNUAL_VA_FUEL_DETAILED.csv', index = False)











    