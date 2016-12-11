## coding: utf-8
import arcpy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def center_analyst(in_raster):
    out_res = {'c':[],'wc':[],'density':0}
    in_array = arcpy.RasterToNumPyArray(in_raster)
    none_value = arcpy.Raster(in_raster).noDataValue
    min_x = float(arcpy.GetRasterProperties_management(in_raster,'LEFT').getOutput(0))
    max_y = float(arcpy.GetRasterProperties_management(in_raster,'TOP').getOutput(0))
    cell_size_x = float(arcpy.GetRasterProperties_management(in_raster,'cellsizex').getOutput(0))
    cell_size_y = float(arcpy.GetRasterProperties_management(in_raster,'cellsizey').getOutput(0))
    center,weight_center = [0,0],[0,0]
    count,sum_num = 0.0,0.0
    for row in range(len(in_array)):
        for col in range(len(in_array[row])):
            if in_array[row,col] != none_value:
                count += 1
                sum_num += in_array[row,col]
                center[0] += col
                center[1] += row
                weight_center[0] += col*in_array[row,col]
                weight_center[1] += row*in_array[row,col]
    center[0] = min_x + center[0]/count*cell_size_x
    center[1] = max_y - center[1]/count*cell_size_y
    weight_center[0] = min_x + weight_center[0]/sum_num*cell_size_x
    weight_center[1] = max_y - weight_center[1]/sum_num*cell_size_y
    out_res['c'] = center
    out_res['wc'] = weight_center
    out_res['density'] = sum_num/count
    return out_res
def dis_analyst(in_raster,center,max_dis,dis_step,direction = False):
    in_array = arcpy.RasterToNumPyArray(in_raster)
    none_value = arcpy.Raster(in_raster).noDataValue
    min_x = float(arcpy.GetRasterProperties_management(in_raster,'LEFT').getOutput(0))
    max_y = float(arcpy.GetRasterProperties_management(in_raster,'TOP').getOutput(0))
    max_x = float(arcpy.GetRasterProperties_management(in_raster,'RIGHT').getOutput(0))
    min_y = float(arcpy.GetRasterProperties_management(in_raster,'BOTTOM').getOutput(0))
    cell_size_x = float(arcpy.GetRasterProperties_management(in_raster,'cellsizex').getOutput(0))
    cell_size_y = float(arcpy.GetRasterProperties_management(in_raster,'cellsizey').getOutput(0))
    index = range(0,max_dis,dis_step)
    if direction:
        columns =['count_NE','count_NW','count_SW','count_SE','sum_NE','sum_NW','sum_SW','sum_SE']
    else:
        columns = ['count','sum']
    out_res = pd.DataFrame(np.zeros((len(index),len(columns))),index,columns)
    for dis in range(dis_step,max_dis,dis_step):
        if direction:
            dirc_lst = ['NE','NW','SW','SE']
            count_lst,sum_lst,ds = [0.0]*4,[0.0]*4,[0.0]*4
            if (max_y - (center[1]+dis)) <0:
                min_row = 0
            else:
                min_row = int((max_y - (center[1]+dis))/cell_size_y)
            if int((max_y - (center[1]-dis))/cell_size_y) >= len(in_array):
                max_row = len(in_array)-1
            else:
                max_row = int((max_y - (center[1]-dis))/cell_size_y)
            if center[0]-dis < min_x:
                min_col = 0
            else:
                min_col = int((center[0]-dis-min_x)/cell_size_x)
            if int((center[0]+dis-min_x)/cell_size_x) >= len(in_array[0]):
                max_col = len(in_array[0])-1
            else:
                max_col = int((center[0]+dis-min_x)/cell_size_x)
            for row in range(min_row,max_row):
                for col in range(min_col,max_col):
                    x,y = min_x +col*cell_size_x,max_y -row*cell_size_y
                    r = ((x-center[0])**2+(y-center[1])**2)**0.5
                    if in_array[row,col] != none_value and r <= dis:
                        if x >= center[0] and y >= center[1]:
                            sum_lst[0] += in_array[row,col]
                            count_lst[0] += 1
                        elif x <=center[0] and y >= center[1]:
                            sum_lst[1] += in_array[row,col]
                            count_lst[1] += 1
                        elif x <=center[0] and y <= center[1]:
                            sum_lst[2] += in_array[row,col]
                            count_lst[2] += 1
                        elif x >=center[0] and y <= center[1]:
                            sum_lst[3] += in_array[row,col]
                            count_lst[3] += 1
            for i in range(4):
                out_res['count_'+dirc_lst[i]][dis] = count_lst[i]
                out_res['sum_'+dirc_lst[i]][dis] = sum_lst[i]
            if min_row == 0 and min_col == 0 and max_row == len(in_array)-1 and max_col == len(in_array[0])-1:
                break
        else:
            count_num,sum_num = 0.0,0.0
            if (max_y - (center[1]+dis)) <0:
                min_row = 0
            else:
                min_row = int((max_y - (center[1]+dis))/cell_size_y)
            if int((max_y - (center[1]-dis))/cell_size_y) >= len(in_array):
                max_row = len(in_array)-1
            else:
                max_row = int((max_y - (center[1]-dis))/cell_size_y)
            if center[0]-dis < min_x:
                min_col = 0
            else:
                min_col = int((center[0]-dis-min_x)/cell_size_x)
            if int((center[0]+dis-min_x)/cell_size_x) >= len(in_array[0]):
                max_col = len(in_array[0])-1
            else:
                max_col = int((center[0]+dis-min_x)/cell_size_x)
            print min_row,max_row,min_col,max_col
            for row in range(min_row,max_row):
                for col in range(min_col,max_col):
                    x,y = min_x +col*cell_size_x,max_y -row*cell_size_y
                    r = ((x-center[0])**2+(y-center[1])**2)**0.5
                    if in_array[row,col] != none_value and r <= dis:
                        sum_num += in_array[row,col]
                        count_num += 1
            out_res['count'][dis] = count_num
            out_res['sum'][dis] = sum_num
            if min_row == 0 and min_col == 0 and max_row == len(in_array)-1 and max_col == len(in_array[0])-1:
                break
    return out_res

def change_analyst(or_raster,fi_raster):
    arcpy.CheckOutExtension('spatial')
##    out_raster = arcpy.sa.Con(arcpy.sa.NotEqual(arcpy.sa.Plus(arcpy.sa.IsNull(fi_raster),arcpy.sa.IsNull(or_raster)),0),
##                              arcpy.sa.Times(arcpy.sa.IsNull(fi_raster),fi_raster)- arcpy.sa.Times(arcpy.sa.IsNull(or_raster),or_raster))

##    out_raster = arcpy.sa.Con(arcpy.sa.IsNull(or_raster),
##                              arcpy.sa.Con(arcpy.sa.IsNull(fi_raster),0,fi_raster),
##                              arcpy.sa.Con(arcpy.sa.IsNull(fi_raster),or_raster,arcpy.sa.Minus(fi_raster,or_raster)))
    out_raster = arcpy.sa.Times(arcpy.sa.IsNull(fi_raster),fi_raster)- arcpy.sa.Times(arcpy.sa.IsNull(or_raster),or_raster)
    arcpy.CheckInExtension('spatial')
    return out_raster
                    
        
    
    

if __name__ == '__main__':
    CE = ['h:/CE2010f/CEH.tif','h:/CE2015f/CEH.tif','h:/CE2010f/PPV.tif',
           'h:/CE2010f/CVV.tif','h:/CE2015f/PPV.tif','h:/CE2015f/CVV.tif',]
    local_center = [955380,4344154]
## change analyst
    arcpy.env.overwriteOutput = True
    CEH_change = change_analyst(CE[0],CE[1])
    CEH_change.save('h:/CE2015f/change10_15.tif')
## center analyst    
##    CA = []
##    for h in CEH:
##        print h
##        res = center_analyst(h)
##        CA.append(res)
##        print res
##    x,y,s = [],[],[]
##    for c in CA:
##        x += [c['c'][0],c['wc'][0]]
##        y += [c['c'][1],c['wc'][1]]
##    for c in CEH:
##        s += [c+'_center',c+'_weight_center']
##    plt.scatter(x,y)
##    for i in range(len(x)):
##        plt.text(x[i],y[i],s[i])
##    plt.show()
    
## distance and direction analyst
##    max_dis = 100000
##    dis_step = 5000
##    center = local_center
##    ds = dis_analyst(CE[0],center,max_dis,dis_step,True)
##    ds.to_csv('CEH_2010.csv')


##
##    center15 = center_analyst(CEH[1])['wc']
## 
##    ds15 = dis_analyst(CEH[1],center15,max_dis,dis_step)
##    density15 = [d[2] for d in ds15]
##    plt.plot(dis_range,density15,'-*',label = '2015')

## altitude analyst
    
    
    
                
