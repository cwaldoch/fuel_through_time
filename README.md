# fuel_through_time
 
This repo contains teh code and data for making a map (in gif form) of generation by Virginia power plants 2001-2019. The plotted circles are colored by fuel type and sized by the amount of generation. 
While the data in this repo is only for Virginia, the script I used to go through the EIA's API and collect the data is also included, as well as a reference file from EIA form-860 and a national version of the virginia data. 
Let's run everything down.

The gis_data filder has a shapefile of counties in Virginia. You'll want a shapefile of whatever geography you're working with. If you don't know what a shapefile is, you can download QGIS for free and start messing around with GIS.
Most data-heavy federal offices/deparments will have a bunch of shapefiles (BLS, EIA, Census) available for free, as will your state and often your local town or county. There are two potential pain areas with this code, and the shapefile/GIS management is one of them. It's very easy to mess up
the cartographic projections piece and end up with a blank or broken map. You can check the crs on an imported shapefile with ".crs"/ In the example below, I'm importing a shapefile of Virginia counties, putting it into the GeoDataframe format, checking the crs, then converting it to the project
 crs I want to use

```python
import geopandas as gpd 
vaShape = gpd.read_file(dataSource+"gis_data\va_counties.shp")
vaShape2 = gpd.GeoDataFrame(vaShape,geometry='geometry',crs={'init':'epsg:4269'})
vaShape2.crs
vaShape3 = vaShape2.to_crs("epsg:32618")
```

