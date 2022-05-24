#!python
import os
import sys
import timeit
import logging
from basinmaker import basinmaker
import time
import ntpath
#Fakes a display to avoid an error with Qt
os.system('Xvfb :99 -screen 0 640x480x8 -nolisten tcp &')

logging.captureWarnings(True)

#Use Basinmaker Define Project spatial extent.  
def defineExtent():
    mode = params['extentmode']
    demname = ntpath.basename(params['pathdem'])
    start = time.time()

    try:
        print('\nDefine_Project_Spatial_Extent running...\n')
        if mode == "using_dem":
            bm.Define_Project_Spatial_Extent(
                mode=mode,
                path_to_dem_input = os.path.join(os.getcwd(),datafolder,'DEM',demname),
                gis_platform="qgis"
            )
        elif mode == "using_hybasin":
            hybasinname = ntpath.basename(params['pathhybasin'])
            hybasinID = int(params['hybasinid'])
            bufferdist = params['bufferdistance']
            bm.Define_Project_Spatial_Extent(
                mode=mode,
                path_to_dem_input = os.path.join(os.getcwd(),datafolder,'DEM',demname),
                gis_platform="qgis",
                path_to_hydrobasin_polygon = os.path.join(os.getcwd(),datafolder,'hybasin',hybasinname),
                hydrobasin_id_of_watershed_outlet = hybasinID,
                buffer_distance = float(bufferdist)
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
            extentpolyname = ntpath.basename(params['path_providedpoly'])
            bufferdist = params['bufferdistance']
            bm.Define_Project_Spatial_Extent(
                mode=mode,
                path_to_dem_input = os.path.join(os.getcwd(),datafolder,'DEM',demname),
                gis_platform="qgis",
                path_to_spatial_extent_polygon = os.path.join(os.getcwd(),datafolder,'extent_poly', extentpolyname),
                buffer_distance = float(bufferdist)
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
            fdrname = ntpath.basename(params['pathfdr'])
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
    
    lakesname = ntpath.basename(params['pathlakes'])
    pointsinterestname = ntpath.basename(params['pathpointsinterest'])
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

#Add hydrology related attributes
def genHydroRoutingAtt():
    
    bankfullname = ntpath.basename(params['pathbankfull'])
    landuserast = ntpath.basename(params['pathlanduserast'])
    manningtablename = ntpath.basename(params['landusemanning'])
    poiid = params['poiid']
    poiname = params['poiname']
    poindrainage = params['poidrainarea']
    poinsource = params['poisource']
    lakeid = params['lakeid']
    laketype = params['laketype']
    lakevol = params['lakevol']
    lakeavgdepth = params['lakeavgdepth']
    lakearea = params['lakearea']
    projected_epsg_code = str(params['epsgcode'])
    
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
            width = params['bankfullwidth']
            depth = params['bankfulldepth']
            discharge = params['bankfulldischarge']
            drainage = params['bankfulldrainage']
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
                path_landuse= path_landuse,
                path_landuse_and_manning_n_table = path_manning_table,
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


# Remove small lakes 
def removesmalllakes():

    input_routing_product_folder=path_output_folder
    folder_product_after_filter_lakes = os.path.join(os.getcwd(),'OIH_Output','network_after_filter_lakes')
    filterconnectedlakes = float(params['filterconnectedlakes'])
    filternonconnectedlakes = float(params['filternonconnectedlakes'])
    #selectedlakeid = params['selectedlakeid']
    start = time.time()

    try:
        print('\Remove_Small_Lakes running...\n')
        bm_post.Remove_Small_Lakes(
            path_output_folder = folder_product_after_filter_lakes,
            routing_product_folder = input_routing_product_folder,
            connected_lake_area_thresthold=filterconnectedlakes,
            non_connected_lake_area_thresthold=filternonconnectedlakes,
            #selected_lake_ids = selectedlakeid,
            gis_platform="qgis",
        )
        print('Remove_Small_Lakes was successful...\n')
    except Exception as e:
        print('Remove_Small_Lakes failed...')
        print(e)
    end = time.time()
    print("Remove_Small_Lakes took", end - start, "seconds")


#Increase catchment area
def increaseCatchArea():

    input_routing_product_folder = os.path.join(os.getcwd(),'OIH_Output','network_after_filter_lakes')
    folder_product_after_increase_catchment = os.path.join(os.getcwd(),'OIH_Output','network_after_increase_catchment')
    minsubbasinarea = float(params['minsubbasinarea'])
    start = time.time()

    try:
        print('\Increase_catchment_area running...\n')
        bm_post.Decrease_River_Network_Resolution(
            path_output_folder = folder_product_after_increase_catchment,
            routing_product_folder = input_routing_product_folder,
            minimum_subbasin_drainage_area= minsubbasinarea,
            gis_platform="qgis",
        )
        print('Increase_catchment_area was successful...\n')
    except Exception as e:
        print('Increase_catchment_area failed...')
        print(e)
    end = time.time()
    print("Increase_catchment_area took", end - start, "seconds")


#Generate HRUs
def generateHRUs():
    folder_product_after_increase_catchment=os.path.join(os.getcwd(),'OIH_Output','network_after_increase_catchment')
    input_routing_product_folder=folder_product_after_increase_catchment
    folder_product_after_gen_hrus=os.path.join(os.getcwd(),'OIH_Output','network_after_gen_hrus')

    demname = ntpath.basename(params['pathdem'])
    landusepoly = ntpath.basename(params['pathlandusepoly'])
    landuseinfo = ntpath.basename(params['pathlanduseinfo'])
    soilpoly = ntpath.basename(params['pathsoil'])
    soilinfo = ntpath.basename(params['pathsoilinfo'])
    veginfo = ntpath.basename(params['pathveginfo'])
    start = time.time()

    try:
        print('\Generate_HRUs running...\n')
        bm_post.Generate_HRUs(
            path_output_folder=folder_product_after_gen_hrus,
            path_subbasin_polygon        =os.path.join(input_routing_product_folder, "finalcat_info.shp"),
            path_connect_lake_polygon    =os.path.join(input_routing_product_folder, "sl_connected_lake.shp"),
            path_non_connect_lake_polygon='#',
            path_landuse_polygon=os.path.join(os.getcwd(),'Data','landuse', landusepoly),
            path_soil_polygon   =os.path.join(os.getcwd(),'Data','soil',soilpoly),
            #path_vegetation_polygon    ="#",
            #path_other_polygon_1="#",
            #path_other_polygon_2="#",
            path_landuse_info=os.path.join(os.getcwd(),'Data','landuse', landuseinfo),
            path_soil_info   =os.path.join(os.getcwd(),'Data','soil', soilinfo),
            path_veg_info    =os.path.join(os.getcwd(),'Data','landuse', veginfo),
            path_to_dem=os.path.join(os.getcwd(),datafolder,'DEM',demname),
            importance_order = ['Soil_ID','Landuse_ID'],
            min_hru_subbasin_area_ratio = 0.0,
            gis_platform="qgis",
            #projected_epsg_code = 'EPSG:3161',
        )
        print('Generate_HRUs was successful...\n')
    except Exception as e:
        print('Generate_HRUs failed...')
        print(e)
    end = time.time()
    print("Generate_HRUs took", end - start, "seconds")


#Generate the Raven RVH files
def generateRavenFiles():
    folder_product_after_filter_lakes=os.path.join(os.getcwd(),'OIH_Output','network_after_gen_hrus')
    input_routing_product_folder=folder_product_after_filter_lakes
    raven_model_dir = folder_product_after_filter_lakes
    modelname = params['modelname']

    try:
        print('Generate_Raven_Model_Inputs running...\n')
        bm_post.Generate_Raven_Model_Inputs(
            path_hru_polygon               = os.path.join(input_routing_product_folder, "finalcat_hru_info.shp"),
            model_name                     = modelname,
            subbasingroup_names_channel    =["Allsubbasins"],
            subbasingroup_length_channel   =[-1],
            subbasingroup_name_lake        =["AllLakesubbasins"],
            subbasingroup_area_lake        =[-1],
            path_output_folder             = raven_model_dir,
            aspect_from_gis                = 'grass',
        )
        print('Raven model inputs were successfully generated!\n')
    except Exception as e:
        print('Generate Raven model inputs failed...')
        print(e)


#Opens the parameters file created by QRaven and imports them into a dictionary
params = {}
with open("/root/BasinMaker/parameters.txt") as f:
    for line in f:
        (key, val) = line.split()
        params[key] = val


path_folder_to_save_intermediate_outputs = os.path.join(os.getcwd(),'bm_tmp')
datafolder = os.path.join(os.getcwd(),'Data')
path_output_folder = os.path.join(os.getcwd(),'OIH_Output','network_without_simplification')

bm = basinmaker.delineate(path_working_folder=path_folder_to_save_intermediate_outputs)
bm_post = basinmaker.postprocess()

maxmemory = params['maxmemory']

defineExtent()
delineateNoLakes()
if params['pathlakes'] !='#':
    addOutletPts()
genHydroRoutingAtt()
combinecatchment()
removesmalllakes()
increaseCatchArea()
generateHRUs()
generateRavenFiles()
