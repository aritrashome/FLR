import numpy as np
import pandas as pd
from tqdm import tqdm
import json
import matplotlib.pyplot as plt

import rasterio
from rasterio.plot import show
from osgeo import gdal
from PIL import Image, TiffImagePlugin
from osgeo import osr

def pixel2coord( y, x,gt, transform):
    # GDAL affine transform parameters, According to gdal documentation xoff/yoff are image left corner, a/e are pixel wight/height and b/d is rotation and is zero if image is north up. 
    xoff, a, b, yoff, d, e = gt

    xp = a * x + b * y + xoff
    yp = d * x + e * y + yoff

    lat_lon = transform.TransformPoint(xp, yp) 

    xp = lat_lon[0]
    yp = lat_lon[1]
    
    return [yp, xp]
def coord2pixel(yp, xp, gt, transform2):
    xoff, a, b, yoff, d, e = gt
    lat_lon = transform2.TransformPoint(xp, yp) 
    xp,yp = lat_lon[0], lat_lon[1]
    x = (xp - xoff)/a
    y = (yp - yoff)/e
    return int(round(y,0)), int(round(x,0))

df = pd.read_csv('Karnataka_data.csv')
df['land_cover'] = 0
df['land_cover_5yr'] = 0

################################## LAND COVER ########################################
for year in range(2001,2020):
    print(year)
    filepath = 'LULC/Karnataka_LULC_'+str(year)+'.tif'
    df2 = df[df['yod']==year]
    
    ds = gdal.Open(filepath)
    old_cs = osr.SpatialReference()
    old_cs.ImportFromWkt(ds.GetProjectionRef())
    wgs84_wkt = """
        GEOGCS["WGS 84",
            DATUM["WGS_1984",
                SPHEROID["WGS 84",6378137,298.257223563,
                    AUTHORITY["EPSG","7030"]],
                AUTHORITY["EPSG","6326"]],
            PRIMEM["Greenwich",0,
                AUTHORITY["EPSG","8901"]],
            UNIT["degree",0.01745329251994328,
                AUTHORITY["EPSG","9122"]],
            AUTHORITY["EPSG","4326"]]"""
    new_cs = osr.SpatialReference()
    new_cs.ImportFromWkt(wgs84_wkt)
    transform2 = osr.CoordinateTransformation(new_cs,old_cs) 
    gt = ds.GetGeoTransform()
    for idx in df2.index:
        res = json.loads(df['.geo'][idx])
        lon, lat = res['coordinates'][0],res['coordinates'][1]
        row, col = coord2pixel(lon,lat, gt, transform2)
        #print(row,col)
        src = rasterio.open(filepath, )
        land_cover = src.read(1)
        #print(land_cover[row][col])
        try:
            df['land_cover'][idx] = land_cover[row][col]
        except:
            df['land_cover'][idx] = 0

################################## LAND COVER AFTER 5 YEARS ########################################
for year in range(2001,2020):
    print(year)
    yr = min(2019,year+5)
    filepath = 'LULC/Karnataka_LULC_'+str(yr)+'.tif'
    df2 = df[df['yod']==year]
    
    ds = gdal.Open(filepath)
    old_cs = osr.SpatialReference()
    old_cs.ImportFromWkt(ds.GetProjectionRef())
    wgs84_wkt = """
        GEOGCS["WGS 84",
            DATUM["WGS_1984",
                SPHEROID["WGS 84",6378137,298.257223563,
                    AUTHORITY["EPSG","7030"]],
                AUTHORITY["EPSG","6326"]],
            PRIMEM["Greenwich",0,
                AUTHORITY["EPSG","8901"]],
            UNIT["degree",0.01745329251994328,
                AUTHORITY["EPSG","9122"]],
            AUTHORITY["EPSG","4326"]]"""
    new_cs = osr.SpatialReference()
    new_cs.ImportFromWkt(wgs84_wkt)
    transform2 = osr.CoordinateTransformation(new_cs,old_cs) 
    gt = ds.GetGeoTransform()
    for idx in df2.index:
        res = json.loads(df['.geo'][idx])
        lon, lat = res['coordinates'][0],res['coordinates'][1]
        row, col = coord2pixel(lon,lat, gt, transform2)
        #print(row,col)
        src = rasterio.open(filepath, )
        land_cover = src.read(1)
        #print(land_cover[row][col])
        try:
            df['land_cover_5yr'][idx] = land_cover[row][col]
        except:
            df['land_cover_5yr'][idx] = 0
