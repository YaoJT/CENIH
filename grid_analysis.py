import arcpy
import numpy as np

def grid_analysis(input_raster,mask,grid_size_x,grid_size_y):
    min_x = float(arcpy.GetRasterProperties_management(mask,'LEFT').getOutput(0))
    min_y = float(arcpy.GetRasterProperties_management(mask,'BOTTOM').getOutput(0))
    max_x = float(arcpy.GetRasterProperties_management(mask,'Right').getOutput(0))
    max_y = float(arcpy.GetRasterProperties_management(mask,'TOP').getOutput(0))
    nrow,ncol = int((max_y-min_y)/grid_size_y)+1,int((max_x-min_x)/grid_size_x)+1
    out_array = np.zeros((nrow,ncol))
    min_x1 = float(arcpy.GetRasterProperties_management(input_raster,'LEFT').getOutput(0))
    min_y1 = float(arcpy.GetRasterProperties_management(input_raster,'BOTTOM').getOutput(0))
    max_x1 = float(arcpy.GetRasterProperties_management(input_raster,'Right').getOutput(0))
    max_y1 = float(arcpy.GetRasterProperties_management(input_raster,'TOP').getOutput(0))
    cell_size_x = float(arcpy.GetRasterProperties_management(input_raster,'cellsizex').getOutput(0))
    cell_size_y = float(arcpy.GetRasterProperties_management(input_raster,'cellsizey').getOutput(0))
    none_value = arcpy.Raster(input_raster).noDataValue
    in_array = arcpy.RasterToNumPyArray(input_raster)
    for i in range(len(in_array)):
        for j in range(len(in_array[i])):
            value = in_array[i,j]
            if value != none_value:
                x,y = min_x1+j*cell_size_x,max_y1-i*cell_size_y
                row,col = int((max_y-y)/grid_size_y),int((x-min_x)/grid_size_x)
                if row>=0 and col>=0 and row<nrow and col<ncol:
                    out_array[row,col] += value
##                    print value
    out_raster = arcpy.NumPyArrayToRaster(out_array,arcpy.Point(min_x,min_y),grid_size_x,grid_size_y)
    arcpy.DefineProjection_management(out_raster,mask)
    out_raster = arcpy.sa.Plus(arcpy.sa.Minus(mask,mask),out_raster)
    
    return out_raster

if __name__ == '__main__':
    arcpy.CheckOutExtension('spatial')
    arcpy.env.overwriteOutput = True
    in_raster = 'h:/CE2010f/CVV.tif'
    in_raster2 = 'h:/CE2015f/CVV.tif'
    mask = 'g:/CLUE-sII/data/clue_simulation/lucc2015_af.tif'
    grid_size = 5000
    out_raster = grid_analysis(in_raster,mask,grid_size,grid_size)
    out_raster2 = grid_analysis(in_raster2,mask,grid_size,grid_size)
    out_raster.save('h:/CE2010f/CVV_5kmf')
    out_raster2.save('h:/CE2015f/CVV_5kmf')
    arcpy.CheckInExtension('spatial')
