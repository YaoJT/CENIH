import numpy as np
import arcpy
import os
arcpy.CheckOutExtension('spatial')
arcpy.env.overwriteOutput = True
G2 = {'g:/GHG_Landuse/Beijing_city/lur_zonal_county_11_14_1/factor_analysis_population_maps/function_zone_f_class_1.tif':101.5616,
      'g:/GHG_Landuse/Beijing_city/lur_zonal_county_11_14_1/factor_analysis_population_maps/public_transport_point_Point_f_radius_1000_normalization.tif':12.8869}
G3 = {'g:/GHG_Landuse/Beijing_city/lur_zonal_county_11_14_1/factor_analysis_population_maps/function_zone_f_class_4.tif':2229.704,
      'g:/GHG_Landuse/Beijing_city/lur_zonal_county_11_14_1/factor_analysis_population_maps/public_transport_point_Point_f_radius_5000_normalization.tif':75.6014}
work_space = 'h:/LCMS_11_22/CE2030fff'
EF2,EF3 = ('g:/GHG_Landuse/Beijing_city/driving_factors/EF2_2010.tif','g:/GHG_Landuse/Beijing_city/driving_factors/EF_3_2010.tif')


if os.path.exists(work_space) == False:
    os.makedirs(work_space)
out_res = open(os.path.join(work_space,'result.csv'),'w+')
out_res.write('increase_radio,CE2,GDP2,CE3,GDP3\n')
res = []

GDP2,GDP3 = 0,0 
for f2 in G2:
    GDP2 = arcpy.sa.Plus(GDP2,arcpy.sa.Times(f2,G2[f2]))
CE2 = GDP2*EF2
GDP2.save(os.path.join(work_space,'GDP2.tif'))
CE2.save(os.path.join(work_space,'CE2.tif'))
for f3 in G3:
    GDP3 = arcpy.sa.Plus(GDP3,arcpy.sa.Times(f3,G3[f3]))
CE3 = GDP3*EF3
GDP3.save(os.path.join(work_space,'GDP3.tif'))
CE3.save(os.path.join(work_space,'CE3.tif'))
for IR in range(10,101,10):
    IR_list = [IR]
    land_path = 'h:/LCMS_11_22/BR'+str(IR)+'/predicting_10/predicting10.tif'
    CE20 = arcpy.sa.Con(arcpy.sa.EqualTo(land_path,1),CE2)
    GDP20 = arcpy.sa.Con(arcpy.sa.EqualTo(land_path,1),GDP2)
    CE30 = arcpy.sa.Con(arcpy.sa.EqualTo(land_path,1),CE3)
    GDP30 = arcpy.sa.Con(arcpy.sa.EqualTo(land_path,1),GDP3)
    CE20.save(os.path.join(work_space,'CE2_BR_'+str(IR)+'.tif'))
    CE30.save(os.path.join(work_space,'CE3_BR_'+str(IR)+'.tif'))
    GDP20.save(os.path.join(work_space,'GDP20_BR_'+str(IR)+'.tif'))
    GDP30.save(os.path.join(work_space,'GDP30_BR_'+str(IR)+'.tif'))
    array_2 = arcpy.RasterToNumPyArray(CE20)
    array_3 = arcpy.RasterToNumPyArray(CE30)
    array_g2 = arcpy.RasterToNumPyArray(GDP20)
    array_g3 = arcpy.RasterToNumPyArray(GDP30)
    none_2,none_3 = CE20.noDataValue,CE30.noDataValue
    none_g2,none_g3 = GDP20.noDataValue,GDP30.noDataValue
    value = [0,0,0,0]
    for i in range(len(array_2)):
        for j in range(len(array_2[i])):
            if array_2[i,j] != none_2:
                value[0] += array_2[i,j]
            if array_g2[i,j] != none_g2:
                value[1] += array_g2[i,j]
            if array_3[i,j] != none_3:
                value[2] += array_3[i,j]
            if array_g3[i,j] != none_g3:
                value[3] += array_g3[i,j]
    IR_list.append(value)
    res.append(IR_list)
    out_res.write('{0},{1},{2},{3},{4}\n'.format(IR,value[0],value[1],value[2],value[3]))
    print IR_list
arcpy.CheckInExtension('spatial')
out_res.close()
    
    
