import numpy as np
import arcpy
import os
arcpy.CheckOutExtension('spatial')
arcpy.env.overwriteOutput = True
factor_space = 'g:/GHG_Landuse/Beijing_city/lur_zonal_county_11_28_2010f'
NI = {factor_space+'/factor_analysis_population_maps/function_zone_f_class_4.tif':2582.652651,
      factor_space+'/factor_analysis_population_maps/public_transport_point_Point_f_radius_3000_normalization.tif':293.0581969,
      factor_space+'/factor_analysis_population_maps/road_radius_5000_normalization.tif':125.2388418}
PP = {factor_space+'/factor_analysis_population_maps/function_zone_f_class_3.tif':10.2148,
      factor_space+'/factor_analysis_population_maps/public_transport_point_Point_f_radius_1000_normalization.tif':27.4550,
      factor_space+'/factor_analysis_population_maps/road_radius_5000_normalization.tif':36.2477}
CV = {factor_space+'/factor_analysis_population_maps/public_transport_point_Point_f_radius_10000_normalization.tif':103.4630462,
      factor_space+'/factor_analysis_population_maps/road_radius_1000_normalization.tif':30.43934702}
work_space = factor_space
EFI,EFH = ('g:/GHG_Landuse/Beijing_city/driving_factors/EF2_2010.tif',[0.7325,0.2411])


if os.path.exists(work_space) == False:
    os.makedirs(work_space)


NIV,PPV,CVV = 0,0,0
for n in NI:
    NIV = arcpy.sa.Plus(NIV,arcpy.sa.Times(n,NI[n]))

NIV.save(os.path.join(work_space,'NIV.tif'))
##CEI = arcpy.sa.Times(NIV,EFI)
##CEI.save(os.path.join(work_space,'CEI.tif'))
for p in PP:
    PPV = arcpy.sa.Plus(PPV,arcpy.sa.Times(p,PP[p]))
for c in CV:
    CVV = arcpy.sa.Plus(CVV,arcpy.sa.Times(c,CV[c]))

PPV.save(os.path.join(work_space,'PPV.tif'))
CVV.save(os.path.join(work_space,'CVV.tif'))
CEH = arcpy.sa.Plus(arcpy.sa.Times(PPV,EFH[0]),arcpy.sa.Times(CVV,EFH[1]))
CEH.save(os.path.join(work_space,'CEH.tif'))
    
    
