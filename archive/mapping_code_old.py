# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 19:32:27 2020

@author: .3
"""


import numpy as np #basic numeric calculation
import pandas as pd #split-apply-combine operations on dataframe
import geopandas as gpd #geometric manipulations on GeoDataFrames
import matplotlib.pyplot as plt #plotting tool
from matplotlib.patches import RegularPolygon, Circle #drawing hexagons
import shapely #to attribute geometric properties for shapes
from shapely.geometry import Polygon, Point
import matplotlib.colors
import pdb
import datetime
import matplotlib as mpl
#from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import matplotlib.patches as mpatches
import imageio
import os, sys

start = datetime.datetime.now()
dataSource = r'C:\Users\.3\Desktop\fuel_through_time\\'
dmSize = 75000
fName = str(dmSize)[:2]+'_test8_va.mp4'

vaShape = gpd.read_file(r"C:\Users\.3\Desktop\va_maps\va_counties.shp")

vaShape2 = gpd.GeoDataFrame(vaShape,geometry='geometry',crs={'init':'epsg:4269'})
vaShape3 = vaShape2.to_crs("epsg:32618")

eia860 = pd.read_csv(r"C:\Users\.3\Desktop\national_energy\eia860.csv")

va860 = eia860[eia860['State'] == 'VA']

va860['plant-fuel'] = [x+'-'+y for x,y in zip(va860['Plant Name'].values, va860['Energy Source 1'].values)]
allPlants = gpd.GeoDataFrame(va860,
                 geometry=gpd.points_from_xy(va860.lon, va860.lat),
                     crs={'init':'epsg:4326'})
allPlants2 = allPlants.to_crs("epsg:32618")

dfPlants = pd.read_csv(dataSource+'annual_va_fuel_gen_data.csv')
dfPlants['plant-fuel'] = [x[:-1]+'-'+y for x,y in zip(dfPlants['plant_name'].values, dfPlants['fuel'].values)]

#nyzips = gpd.read_file(dataSource+'union_test5.shp')
#nyzips = gpd.GeoDataFrame(nyzips,geometry='geometry')#,crs={'init':'epsg:32618'})
#
#
##allShapes = gpd.read_file(dataSource+'all_zones_raw.shp')
#allShapes = gpd.read_file(dataSource+'allzonesraw2.shp')
#allShapes = gpd.GeoDataFrame(allShapes,geometry='geometry',crs={'init':'epsg:4326'})
#allShapes2 = allShapes.to_crs("epsg:32618")

cmap = matplotlib.cm.get_cmap('jet')


normBubble = matplotlib.colors.Normalize(0,15000000)

hexColors = []
faceColors = []

dfDict = {}


for year in range(min(dfPlants['year']),max(dfPlants['year'])+1):
    circlesArray = []
    yearPlants = dfPlants[dfPlants['year'] == year]
    plantNames = list(set(yearPlants['plant-fuel']))
    for plantName in plantNames:
        #pdb.set_trace()
        #print(plantName)
        plantValues = allPlants2[allPlants2['plant-fuel'] == plantName]
        
#        if len(plantValues)<1:
#            hexColor = (1,1,1,0)
#            faceColor = (1,1,1,0)
#        else:        
        #pdb.set_trace()
        
        yearPlant = yearPlants[yearPlants['plant-fuel'] == plantName]
        sumMW = yearPlant['gen'].values[0]
    
        if sumMW <= 5000:
            cSize = 3000
        else:
            cSize = normBubble(sumMW) * 25000
    
        hexCircle = plantValues.buffer(cSize)
        #hexCircle.plot()
        #pdb.set_trace()
        # overwriting with grey
        if len(plantValues) >1:
            try:
                cVals = plantValues['color'].values[0].replace('(','').replace(')', '').replace(' ', '').split(',')
                
                circColor = (int(cVals[0])/255,int(cVals[1])/255,int(cVals[2])/255,0.7)
                faceColor = (int(cVals[0])/255,int(cVals[1])/255,int(cVals[2])/255,0.7)
                faceColor = (int(cVals[0])/255,int(cVals[1])/255,int(cVals[2])/255,0.7)
            except AttributeError:
                # this is lazy, but accurate for the data as it exists, some
                # MSW got N/A in color assignment
                hexColor = (133/255,75/255,25/255,1)
            circlesArray.append([hexCircle, circColor, sumMW, plantName, year])
            #pdb.set_trace()
                
            hexColors.append(circColor)
            faceColors.append(faceColor)
    dfCircles = pd.DataFrame(circlesArray, columns = ['geometry', 'color', 'mw', 'plantName', 'year'])
    
    #geoCircles = gpd.GeoDataFrame(dfCircles,geometry='geometry',crs={'init':'epsg:2163'})
    
    dfDict[year] = dfCircles
    
plt.close()


#pp = dfDict[2001]
#
#for idx, row in pp.iterrows():
#    print(row['plantName'])
#    print(row['geometry'].geom_type)


fig, ax = plt.subplots(figsize=(20,16))

mpl.rcParams.update({'font.size' : 14,
                     'font.weight' : "bold"})

#mpl.rcParams['figure.figsize'] = 12, 12

def animate(year):
    ax.clear()
    plotPlants = dfDict[year]
    plotPlants = plotPlants.sort_values(['mw'], ascending=False)
    #plotPlants.to_csv(dataSource+'plot_plants_'+str(year)+'.csv')
    
    vaShape3.plot(ax = ax, color = (0.1, 0.1, 0.1, 0.1), edgecolor = 'k', linewidth =1)
    for idx, row in plotPlants.iterrows():
        circlePlot = gpd.GeoDataFrame({'geometry':row['geometry']},crs='epsg:32618')
        #pdb.set_trace()
        # I think every year is showing all the year for a plant? or someething?
        # it seems like maybe each year is plotting all previous years at once with it
        circlePlot.plot(ax=ax, color=row['color'], edgecolor='k', linewidth=0.5)
        
#    plotPlants.plot(ax=ax, color = plotPlants['color'],
#            legend=False, linewidth=0)
    

    
    solidsPatch = mpatches.Patch(color=(0,0,0, 0.9), label='Coal/Solids')
    hydroPatch = mpatches.Patch(color=(36/255, 99/255, 224/255, 0.8), label='All Hydro')
    gasPatch = mpatches.Patch(color=(237/255, 104/255, 38/255, 0.7), label='Natural Gases')
    wastePatch = mpatches.Patch(color=(133/255, 75/255, 25/255, 0.7), label='Wood/Waste')
    #windPatch = mpatches.Patch(color=(32/255, 135/255, 70/255, 0.7), label='Wind')
    solarPatch = mpatches.Patch(color=(240/255, 206/255, 17/255, 0.7), label='Solar')
    nukePatch = mpatches.Patch(color=(22/255, 255/255, 5/255, 0.7), label='Nuclear')
    #storagePatch = mpatches.Patch(color=(209/255, 8/255, 199/255, 0.7), label='Storage')
    liquidPatch = mpatches.Patch(color=(105/255, 102/255, 100/255, 0.7), label='Oil/Liquids')
    #geoPatch = mpatches.Patch(color=(207/255, 50/255, 6/255, 0.9), label='Geothermal')
    
    plt.legend(loc=1,handles=[solidsPatch, hydroPatch, gasPatch, wastePatch,
                         solarPatch, nukePatch,
                        liquidPatch])
    plt.tight_layout()
    ax.set_title(str(year)+' MWh Generation by Fuel in VA (EIA)',
                 fontdict={'fontsize': '23'})
    ax.axis('off')
    
    
years = list(range(min(dfPlants['year']),max(dfPlants['year'])+1))
#years  = [2001,2018]
aniMap = animation.FuncAnimation(fig, animate, years,interval=1, blit=False)

Writer = animation.writers['ffmpeg']
writer = Writer(fps=0.75, metadata=dict(artist='Me'), bitrate=4000)

aniMap.save(dataSource+fName, writer=writer)
    
end = datetime.datetime.now()
diff = end-start
print(diff)



class TargetFormat(object):
    GIF = ".gif"
    MP4 = ".mp4"
    AVI = ".avi"

def convertFile(inputpath, targetFormat):
    outputpath = os.path.splitext(inputpath)[0] + targetFormat
    print("converting\r\n\t{0}\r\nto\r\n\t{1}".format(inputpath, outputpath))

    reader = imageio.get_reader(inputpath)
    fps = reader.get_meta_data()['fps']

    writer = imageio.get_writer(outputpath, fps=fps)
    for i,im in enumerate(reader):
        sys.stdout.write("\rframe {0}".format(i))
        sys.stdout.flush()
        writer.append_data(im)
    print("\r\nFinalizing...")
    writer.close()
    print("Done.")

convertFile(dataSource+fName, TargetFormat.GIF)
    
