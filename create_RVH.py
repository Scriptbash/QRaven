#!python
import os
import sys
import timeit
import logging
from basinmaker import basinmaker
import time

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
    print(facthreshold)
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
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
    # start add new outlets 
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



modelname = "Temporary_name"

#Opens the parameters file created by QRaven and imports them into a dictionary
params = {}
with open("/home/francis/Documents/Geoinfo/parameters.txt") as f:
    for line in f:
        (key, val) = line.split()
        params[key] = val



path_folder_to_save_intermediate_outputs = os.path.join(os.getcwd(),'bm_tmp')
datafolder = os.path.join(os.getcwd(),'Data')
bm = basinmaker.delineate(path_working_folder=path_folder_to_save_intermediate_outputs)
maxmemory = params['maxmemory']

defineExtent()
delineateNoLakes()
if params['pathlakes'] !='#':
    addOutletPts()



#params['']

# pathdem = params['pathdem']
# pathlandusepoly = params['pathdem']
# pathlanduserast = params['pathdem']
# pathlakes = params['pathdem']
# pathbankfull = params['pathdem']
# pathsoil = params['pathdem']
# pathpointsinterest = params['pathdem']
# maxmemory = params['pathdem']
# extentMode = params['pathdem']
# path_hybasin = params['pathdem']
# hybasinid = params['pathdem']
# bufferdistance = params['pathdem']
# outletlat = params['pathdem']
# outletlon = params['pathdem']
# path_providedpoly = params['pathdem']
# lakeid = params['pathdem']
# laketype = params['pathdem']
# lakevol = params['pathdem']
# lakeavgdepth = params['pathdem']
# lakearea = params['pathdem']
# connectedlake = params['pathdem']
# nonconnectedlake = params['pathdem']
# poiid = params['pathdem']
# poiname = params['pathdem']
# poidrainarea = params['pathdem']
# poisource = params['pathdem']
# epsgcode = params['pathdem']
# bankfullwidth = params['pathdem']
# bankfulldepth = params['pathdem']
# bankfulldischarge = params['pathdem']
# bankfulldrainage =
# kcoef =
# ccoef =
# landusemanning =








