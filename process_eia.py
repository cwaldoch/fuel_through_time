# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 19:32:41 2020

@author: .3
"""
import eia
import pandas as pd
import pdb 


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

plantCodes = list(set(vaPlants['plant_code']))
with open(localPath+"apiKey.txt", 'r') as txt:
    apiKey = txt.read()

api = eia.API(apiKey)

allPlants = []
for plantCode in plantCodes:
    print(plantCode)
    
    dfPlant = plantRef[plantRef['plant_code'] == plantCode]
    plantFuels = dfPlant['fuels'].values[0]
    plantFuels = plantFuels[1:-1].replace("'",'').replace(' ', '').split(',')
    
    plantCoords = eia860[eia860['Plant Code'] == plantCode]
    
    plantLat = plantCoords['lat'].values[0]
    plantLon = plantCoords['lon'].values[0] 
    
    for fuel in plantFuels:
        if fuel != 'nan':
            
           # Example series id
            #ELEC.PLANT.GEN.3772-WAT-ALL.A
            
            serB = 'ELEC.PLANT.GEN.'
            serE = '-ALL.A'
            
            seriesID = serB +str(plantCode)+'-'+fuel+serE

            try:
                df = retrieve_time_series(api, seriesID)
            except KeyError:
                # these errors should only occur for plants that haven't been
                # built yet.
                print('Plant not in yet')
                continue
                
            dfCol = df.columns[0]
            plantName = dfCol.split(': ')[1].split('(')[0]
            df = df.reset_index()
            df = df.rename(columns={dfCol:'gen', 'index':'year'})
            df['plant_name'] = [plantName]*len(df)
            
            df['lat'] = [plantLat]*len(df)
            df['lon'] = [plantLon]*len(df)
            df['fuel'] = [fuel]*len(df)
                           
            allPlants.append(df)
            
dfAll = pd.concat(allPlants, ignore_index = True)

dfAll.to_csv('annual_va_fuel_gen_data.csv', index = False)
    