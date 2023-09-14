from ..utilities import download_request, extract_archive, make_folder
from ..gis_processing import *
import csv


class SoilTypeDownload:

    def cansis(self, dlg):
        output = dlg.file_gis_download_output.filePath()
        url = 'https://sis.agr.gc.ca/cansis/nsdb/slc/v2.2/slc_v2r2_canada.zip'
        dlg.lbl_progressbar.setText('Downloading soil layer')
        make_folder(output + '/unprocessed/soil')
        extract_output = output + '/unprocessed/soil/soil.zip'
        download_request(dlg, url, extract_output)
        dlg.lbl_progressbar.setText('Extracting...')
        extract_archive(extract_output)

        if dlg.chk_process_gis_data.isChecked():
            make_folder(output + '/soil')
            overlay = dlg.file_gis_clip_layer.filePath()
            vector = output + '/unprocessed/soil/slc_v2r2_canada.shp'
            attributes_table = output + '/unprocessed/soil/slc_v2r2_canada_cmp.dbf'
            clipped = clip_vector(dlg, overlay, vector, None, True)
            extracted_table = extract_by_attribute(dlg, attributes_table, 'CMP', 1)
            joined = join_attributes(dlg, clipped, extracted_table, 'SL', 'SL', 'KINDMAT')
            formula = 'if( "KINDMAT" = \'OR\',\'ORGANIC\',if( "KINDMAT" =\'SO\',\'MINERAL\',if( "KINDMAT" =\'R1\',' \
                      '\'SOFTROCK\',if( "KINDMAT" =\'R2\',\'GRANITE\',if( "KINDMAT" =\'R3\',\'LIMESTONE\',' \
                      'if( "KINDMAT" =\'R4\',\'HARDROCK\',if( "KINDMAT" =\'F\',\'ROCKFIELD\',if( "KINDMAT" =\'UR\',' \
                      '\'URBAN\',if( "KINDMAT" =\'IC\',\'SNOW\',if( "KINDMAT" =\'WA\',\'WATER\',\'NA\'))))))))))'
            calculated = field_calculator(dlg, joined, formula, 'SOIL_PROF', '2', None, True)
            formula = 'if( "KINDMAT" = \'OR\',1,if( "KINDMAT" =\'SO\',2,if( "KINDMAT" =\'R1\',3,' \
                      'if( "KINDMAT" =\'R2\',4,if( "KINDMAT" =\'R3\',5,if( "KINDMAT" =\'R4\',6,' \
                      'if( "KINDMAT" =\'F\',7,if( "KINDMAT" =\'UR\',9,if( "KINDMAT" =\'IC\',8,' \
                      'if( "KINDMAT" =\'WA\',-1,0))))))))))'
            calculated = field_calculator(dlg, calculated, formula, 'Soil_ID', '1', None, True)
            reproject_layer(dlg, calculated, output + '/soil/qrvn_soil.shp')

            row_list = [["Soil_ID", "SOIL_PROF"],
                        [1, "ORGANIC"],
                        [2, "MINERAL"],
                        [3, "SOFTROCK"],
                        [4, "GRANITE"],
                        [5, "LIMESTONE"],
                        [6, "HARDROCK"],
                        [7, "ROCKFIELD"],
                        [8, "SNOW"],
                        [9, "UBRAN"],
                        [-1, "WATER"]]
            with open(output + '/soil/soil_info.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(row_list)

