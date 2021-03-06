import numpy as np
import pandas as pd
from tqdm import tqdm
import json
import matplotlib.pyplot as plt

import rasterio
from rasterio.plot import show
from osgeo import gdal

df = pd.read_csv('Karnataka_data.csv')
df = df[df['yod']<=2013]
df = df.drop(['prec','label','land_cover_5yr','land_cover'],axis=1)

#year = 2003
for year in range(2010,2014):
    df['prec_'+str(year)] = 0
    for month in ['01','02','03','04','05','06','07','08','09','10','11','12']:
        filepath = 'Prec/CHELSA_prec_'+str(year)+'_'+month+'_V1.2.1.tif'
        src = rasterio.open(filepath,)
        prec = src.read(1)
        print(month,year, end=' ')
        df['prec_'+str(year)] += df.apply(lambda row : prec[row['row']][row['col']] , axis=1)
    df.to_csv('Karnataka_final.csv',index=False)
