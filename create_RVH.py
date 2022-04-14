#!python
import os
import sys
import timeit
import logging
from basinmaker import basinmaker
import time

#Sets the python path for BasinMaker
sys.path.append('/usr/lib/grass80/etc/python')
sys.path.append('/usr/share/qgis/python/plugins')
sys.path.append("$PYTHONPATH:'/usr/share/qgis/python'")

logging.captureWarnings(True)


#Function to validate if file was sent to the script
def validateFile(inputfile):
    if os.path.is_file(inputfile):
        return True
    else:
        return False

#Use Basinmaker Define Project spatial extent.  
def defineExtent():
    mode = params['extentmode']
    demname = os.path.basename(params['pathdem'])

    start = time.time()
    print(mode)
    try:
        print('\nDefine_Project_Spatial_Extent running...\n')
        if mode == "using_dem":
            bm.Define_Project_Spatial_Extent(
                mode=mode,
                path_to_dem_input = os.path.join(os.getcwd(),datafolder,'DEM',demname),
                gis_platform="qgis"
            )
        elif mode == "using_hybasin":
            hybasinname = os.path.basename(params['pathhybasin'])
            hybasinID = int(params['hybasinid'])
            bufferdist = float(params['bufferdistance'])
            bm.Define_Project_Spatial_Extent(
                mode=mode,
                path_to_dem_input = os.path.join(os.getcwd(),datafolder,'DEM',"DEM.tif"),
                gis_platform="qgis",
                path_to_hydrobasin_polygon = os.path.join(os.getcwd(),datafolder,'hybasin',hybasinname),
                hydrobasin_id_of_watershed_outlet = hybasinID,
                buffer_distance = bufferdist
            )
        elif mode == "using_outlet_pt":
            outletcoordinates = params['outletlat'], params['outletlon']
            bm.Define_Project_Spatial_Extent(
                mode=mode,
                path_to_dem_input = os.path.join(os.getcwd(),datafolder,'DEM',demname),
                gis_platform="qgis",
                watershed_outlet_coordinates = outletcoordinates
            )
        elif mode == "using_provided_ply":
            extentpolyname = os.path.basename(params['path_providedpoly'])
            bufferdist = float(['bufferdistance'])
            bm.Define_Project_Spatial_Extent(
                mode=mode,
                path_to_dem_input = os.path.join(os.getcwd(),datafolder,'DEM',demname),
                gis_platform="qgis",
                path_to_spatial_extent_polygon = os.path.join(os.getcwd(),datafolder,'extent_poly', extentpolyname),
                buffer_distance = bufferdist
            )
  
        print('Define_Project_Spatial_Extent was successful...\n')
    except Exception as e:
        print('Define_Project_Spatial_Extent failed...')
        print(e)
        sys.exit()
    end = time.time()
    print("Define_Project_Spation_Extent took", end - start, "seconds")


#Use Basinmaker Delineate routing structure without lakes.  
def delineateNoLakes():
    mode = params['delineatemode']
    facthreshold = float(params['facthreshold'])
       
    start = time.time()

    try:
        print('\nDelineation_Initial_Subbasins_Without_Lakes running...\n')
        if mode == "using_dem":
            bm.Delineation_Initial_Subbasins_Without_Lakes(
                fac_thresold = facthreshold,
                mode=mode,
                max_memroy= maxmemory,
                gis_platform="qgis",
            )
        elif mode == "using_fdr":
            fdrname = os.basename(params['pathfdr'])
            bm.Delineation_Initial_Subbasins_Without_Lakes(
                fac_thresold = facthreshold,
                mode=mode,
                max_memroy= maxmemory,
                path_flow_dirction = os.path.join(datafolder, "flow_direction", fdrname),
                gis_platform="qgis",
            )
        print('Delineation_Initial_Subbasins_Without_Lakes was successful...\n')
    except Exception as e:
        print('Delineation_Initial_Subbasins_Without_Lakes failed...')
        print(e)
    end = time.time()
    print("Delineation_Initial_Subbasins_Without_Lakes took", end - start, "seconds")


#Add lake and obs control points
def addOutletPts():
    
    lakesname = os.path.basename(params['pathlakes'])
    pointsinterestname = os.path.basename(params['pathpointsinterest'])
    lakeid = params['lakeid']
    laketype = params['laketype']
    lakevol = params['lakevol']
    lakeavgdepth = params['lakeavgdepth']
    lakearea = params['lakearea']
    poiid = params['poiid']
    poiname = params['poiname']
    poindrainage = params['poidrainarea']
    poinsource = params['poisource']
    
    start = time.time()

    try:
        print('\nAdd_New_Subbasin_Outlet_Points running...\n')
        bm.Add_New_Subbasin_Outlet_Points(
            path_lake_polygon=os.path.join(datafolder,"lakes",lakesname),
            lake_attributes=[lakeid, laketype, lakearea, lakevol, lakeavgdepth],
            connected_lake_area_thresthold=float(params['connectedlake']),
            non_connected_lake_area_thresthold=float(params['nonconnectedlake']),
            path_point_of_interest=os.path.join(os.getcwd(),datafolder,'stations',pointsinterestname), 
            point_of_interest_attributes=[poiid, poiname, poindrainage, poinsource],
            max_memroy=maxmemory,
            gis_platform="qgis",
        )
        print('Add_New_Subbasin_Outlet_Points was successful...\n')
    except Exception as e:
        print('Add_New_Subbasin_Outlet_Points failed...')
        print(e)
    end = time.time()
    print("Add_New_Subbasin_Outlet_Points took", end - start, "seconds")



def genHydroRoutingAtt():
    
    bankfullname = os.path.basename(params['pathbankfull'])
    landuserast = os.path.basename(params['pathlanduserast'])
    manningtablename = os.path.basename(params['landusemanning'])
    width = params['bankfullwidth']
    depth = params['bankfulldepth']
    discharge = params['bankfulldischarge']
    drainage = params['bankfulldrainage']
    poiid = params['poiid']
    poiname = params['poiname']
    poindrainage = params['poidrainarea']
    poinsource = params['poisource']
    lakeid = params['lakeid']
    laketype = params['laketype']
    lakevol = params['lakevol']
    lakeavgdepth = params['lakeavgdepth']
    lakearea = params['lakearea']
    if params['epsgcode'] != '#':
        projected_epsg_code = params['epsgcode']
    if params['pathlanduserast'] != '#':
        path_landuse=os.path.join(datafolder,"landuse", landuserast)
        path_manning_table = os.path.join(datafolder,"landuse", manningtablename)
    else: 
        path_landuse = params['pathlanduserast']
        path_manning_table = '#'
        
    start = time.time()

    try:
        print('\nGenerate_Hydrologic_Routing_Attributes running...\n')
        if params['pathbankfull'] != '#':
            
            bm.Generate_Hydrologic_Routing_Attributes(
                path_bkfwidthdepth_polyline=os.path.join(datafolder,"bkf_width",bankfullname),
                bkfwd_attributes=[width, depth, discharge, drainage],
                path_landuse= path_landuse,
                path_landuse_and_manning_n_table = path_manning_table,
                gis_platform="qgis",
                point_of_interest_attributes=[poiid, poiname, poindrainage, poinsource],
                lake_attributes=[lakeid, laketype, lakearea, lakevol, lakeavgdepth],
                path_output_folder=path_output_folder,
                projected_epsg_code =projected_epsg_code,
            )
        else:
            bm.Generate_Hydrologic_Routing_Attributes(
                gis_platform="qgis",
                point_of_interest_attributes=[poiid, poiname, poindrainage, poinsource],
                lake_attributes=[lakeid, laketype, lakearea, lakevol, lakeavgdepth],
                path_output_folder=path_output_folder,
                projected_epsg_code =projected_epsg_code,
                k = float(params['kcoef']),
                c = float(params['ccoef'])
            )
        print('Generate_Hydrologic_Routing_Attributes was successful...\n')
    except Exception as e:
        print('Generate_Hydrologic_Routing_Attributes failed...')
        print(e)
    end = time.time()
    print("Generate_Hydrologic_Routing_Attributes took", end - start, "seconds")



#Combine catchment covered by the same lake

def combinecatchment():
    start = time.time()
    try:
        print('\Combine_Subbasins_Covered_by_The_Same_Lake running...\n')
        bm.Combine_Subbasins_Covered_by_The_Same_Lake(
            gis_platform="qgis",
            routing_product_folder = path_output_folder,
        )
        print('Combine_Subbasins_Covered_by_The_Same_Lake was successful...\n')
    except Exception as e:
        print('Combine_Subbasins_Covered_by_The_Same_Lake failed...')
        print(e)
    end = time.time()
    print("Combine_Subbasins_Covered_by_The_Same_Lake took", end - start, "seconds")

modelname = "Temporary_name"

#Opens the parameters file created by QRaven and imports them into a dictionary
params = {}
with open("~/BasinMaker/parameters.txt") as f:
    for line in f:
        (key, val) = line.split()
        params[key] = val


path_folder_to_save_intermediate_outputs = os.path.join(os.getcwd(),'bm_tmp')
datafolder = os.path.join(os.getcwd(),'Data')
path_output_folder = os.path.join(os.getcwd(),'OIH_Output','network_without_simplification')

bm = basinmaker.delineate(path_working_folder=path_folder_to_save_intermediate_outputs)
maxmemory = params['maxmemory']

defineExtent()
delineateNoLakes()
if params['pathlakes'] !='#':
    addOutletPts()
combinecatchment()
genHydroRoutingAtt()
