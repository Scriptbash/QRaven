from ..utilities import download_request, make_folder
from ..gis_processing import *
import csv


class LandUseDownload:

    def natural_resources_canada(self, dlg):
        output = dlg.file_gis_download_output.filePath()
        url = 'https://datacube-prod-data-public.s3.ca-central-1.amazonaws.com/store/land/landcover/' \
              'landcover-2020-classification.tif'
        dlg.lbl_progressbar.setText('Downloading landuse cover')
        make_folder(output + '/unprocessed/landuse')
        download_output = output + '/unprocessed/landuse/landuse.tif'
        download_request(dlg, url, download_output)

        if dlg.chk_process_gis_data.isChecked():
            make_folder(output + '/landuse')
            overlay = dlg.file_gis_clip_layer.filePath()
            raster = output + '/unprocessed/landuse/landuse.tif'
            clip_raster(dlg, overlay, raster, output + '/landuse/qrvn_landuse.tif')
            tmp_polygonized = polygonize(dlg, output + '/landuse/qrvn_landuse.tif')

            formula = 'if("DN"=1,\'FOREST\',if("DN"=2,\'FOREST\',if("DN"=5,\'FOREST\',if("DN"=6,\'FOREST\',if("DN"=8,' \
                      '\'SHRUBLAND\',if("DN"=10,\'GRASSLAND\',if("DN"=11,\'SHRUBLAND\',if("DN"=12,\'GRASSLAND\',' \
                      'if("DN"=13,\'BARREN\',if("DN"=14,\'WETLAND\',if("DN"=15,\'AGRICULTURE\',if("DN"=16,\'BARREN\',' \
                      'if("DN"=17,\'URBAN\',if("DN"=18,\'WATER\',if("DN"=19,\'SNOW\',\'NA\')))))))))))))))'
            tmp_calculated = field_calculator(dlg, tmp_polygonized, formula, 'LAND_USE_C', 2)

            formula = 'if( "LAND_USE_C"=\'WATER\',1, if("LAND_USE_C"=\'OPEN\',2,if("LAND_USE_C"=\'FOREST\'' \
                      ',3,if("LAND_USE_C"=\'GRASSLAND\',5,if("LAND_USE_C"=\'URBAN\',6,if("LAND_USE_C"=\'WETLAND\'' \
                      ',7,if("LAND_USE_C"=\'NA\',8,if("LAND_USE_C"=\'SHRUBLAND\',9,if("LAND_USE_C"=\'BARREN\'' \
                      ',10,if("LAND_USE_C"=\'SNOW\',11,if("LAND_USE_C"=\'AGRICULTURE\',12,if("LAND_USE_C"=\'LAKE' \
                      '\',-1,0))))))))))))'
            calculated = field_calculator(dlg, tmp_calculated, formula, 'Landuse_ID', 1)
            cleaned_layer = remove_small_areas(dlg, calculated, 100)
            fixed_geometries = fix_geometries(dlg, cleaned_layer)
            merge_same_polygons(dlg, fixed_geometries, output + '/landuse/qrvn_landuse.shp')

            row_list = [["Landuse_ID", "LANDUSE_C"],
                       [1, "WATER"],
                       [2, "OPEN"],
                       [3, "FOREST"],
                       [5, "GRASSLAND"],
                       [6, "URBAN"],
                       [7, "WETLAND"],
                       [8, "NA"],
                       [9, "SHRUBLAND"],
                       [10, "BARREN"],
                       [11, "SNOW"],
                       [12, "AGRICULTURE"],
                       [-1, "LAKE"]]
            with open(output + '/landuse/landuse_info.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(row_list)
            # TODO add vegetation info csv file!!
