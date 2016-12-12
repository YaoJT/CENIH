import numpy as np
import arcpy
import os

def factor_analysis(in_factor,mask_map):
    res = arcpy.sa.Con(arcpy.sa.EqualTo(mask_map,1),in_factor)
    res_array = arcpy.RasterToNumPyArray(res)
    none_value = res.noDataValue
    count,sum_num = 0.0,0.0
    for i in res_array:
        for j in i:
            if j != none_value:
                sum_num += j
                count += 1
    res = arcpy.sa.Divide(res,sum_num/count)
    return res
def intensities(factor_lst,weight_lst):
    res = 0
    for x in range(len(factor_lst)):
        res = arcpy.sa.Plus(res,arcpy.sa.Times(factor_lst[x],weight_lst[x]))
    return res
def CENI(NIV,EF):
    return arcpy.sa.Times(NIV,EF)
def CEH(PPV,CVV,weights):
    return arcpy.sa.Plus(arcpy.sa.Times(PPV,weights[0]),arcpy.sa.Plus(CVV,weights[1]))
    
if __name__ == '__main__':    
    arcpy.CheckOutExtension('spatial')
    arcpy.env.overwriteOutput = True
    work_space = 'g:/GHG_Landuse/Beijing_city/result1212'
    if os.path.exists(work_space) == False:
        os.makedirs(work_space)
    land_maps = ['g:/GHG_Landuse/Beijing_city/result1212/built_land_2010.tif',
                 'g:/GHG_Landuse/Beijing_city/result1212/built_land_2015.tif']
    EFNI = ['g:/GHG_Landuse/Beijing_city/result1212/EFNI_2010.tif',
            'g:/GHG_Landuse/Beijing_city/result1212/EFNI_2015.tif']
    EFH = [0.7325,0.2411]
    road_maps = ['g:/GHG_Landuse/Beijing_city/lur_zonal_county_11_28_2015_final/factor_analysis_population_maps/road_radius_1000.tif',
                 'g:/GHG_Landuse/Beijing_city/lur_zonal_county_11_28_2015_final/factor_analysis_population_maps/road_radius_3000.tif',
                 'g:/GHG_Landuse/Beijing_city/lur_zonal_county_11_28_2015_final/factor_analysis_population_maps/road_radius_5000.tif',
                 'g:/GHG_Landuse/Beijing_city/lur_zonal_county_11_28_2015_final/factor_analysis_population_maps/road_radius_10000.tif']
    PTP_maps = ['g:/GHG_Landuse/Beijing_city/lur_zonal_county_11_28_2015_final/factor_analysis_population_maps/public_transport_point_Point_f_radius_1000.tif',
                'g:/GHG_Landuse/Beijing_city/lur_zonal_county_11_28_2015_final/factor_analysis_population_maps/public_transport_point_Point_f_radius_3000.tif',
                'g:/GHG_Landuse/Beijing_city/lur_zonal_county_11_28_2015_final/factor_analysis_population_maps/public_transport_point_Point_f_radius_5000.tif',
                'g:/GHG_Landuse/Beijing_city/lur_zonal_county_11_28_2015_final/factor_analysis_population_maps/public_transport_point_Point_f_radius_10000.tif']
    zonal_maps = ['g:/GHG_Landuse/Beijing_city/lur_zonal_county_11_28_2015_final/factor_analysis_population_maps/function_zone_f_class_1.tif',
                  'g:/GHG_Landuse/Beijing_city/lur_zonal_county_11_28_2015_final/factor_analysis_population_maps/function_zone_f_class_2.tif',
                  'g:/GHG_Landuse/Beijing_city/lur_zonal_county_11_28_2015_final/factor_analysis_population_maps/function_zone_f_class_3.tif',
                  'g:/GHG_Landuse/Beijing_city/lur_zonal_county_11_28_2015_final/factor_analysis_population_maps/function_zone_f_class_4.tif']
    year = 0
    for land in land_maps:
        road_maps_land = [factor_analysis(road,land) for road in road_maps]
        PTP_maps_land = [factor_analysis(PTP,land) for PTP in PTP_maps]
        NI_rasters = [zonal_maps[3],PTP_maps_land[1],road_maps_land[2]]
        NI_weights = [2582.652651,293.0581969,125.2388418]
##        NI = {zonal_maps[3]:2582.652651,PTP_maps_land[1]:293.0581969,road_maps_land[2]:125.2388418}
        PP_rasters = [zonal_maps[2],PTP_maps_land[0],road_maps_land[2]]
        PP_weights = [10.2148,27.4550,36.2477]
##        PP = {zonal_maps[2]:10.2148,PTP_maps_land[0]:27.4550,road_maps_land[2]:36.2477}
        CV_rasters = [PTP_maps_land[3],road_maps_land[0]]
        CV_weights = [103.4630462,30.43934702]
##        CV = {PTP_maps_land[3]:103.4630462,road_maps_land[0]:30.43934702}
        NIV = intensities(NI_rasters,NI_weights)
        CENI_land = CENI(NIV,EFNI[year])
        CENI_path = os.path.join(work_space,os.path.split(land)[1].replace('.','_CENI.'))
        CENI_land.save(CENI_path)
        print CENI_path
        PPV = intensities(PP_rasters,PP_weights)
        CVV = intensities(CV_rasters,CV_weights)
        CEH_land = CEH(PPV,CVV,EFH)
        CEH_path = os.path.join(work_space,os.path.split(land)[1].replace('.','_CEH.'))
        CEH_land.save(CEH_path)
        print CEH_path
        year += 1

        


