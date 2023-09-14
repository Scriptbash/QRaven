import urllib.request, os, zipfile, tarfile, shutil, processing
from PyQt5.QtWidgets import *
from qgis.core import Qgis, QgsVectorLayer, QgsRasterLayer,QgsCoordinateReferenceSystem,QgsProject,QgsProcessingFeedback
from ..utilities import extract_archive, download_request, make_folder
from ..gis_processing import *


class HydroSheds:

    def download_dem(self, dlg, region):
        output = dlg.file_gis_download_output.filePath()
        url = 'https://data.hydrosheds.org/file/hydrosheds-v1-con/na_con_3s.zip'
        dlg.lbl_progressbar.setText('Downloading DEM')
        make_folder(output + '/unprocessed/DEM')
        extract_output = output + '/unprocessed/DEM/dem.zip'
        download_request(dlg, url, extract_output)
        dlg.lbl_progressbar.setText('Extracting...')
        extract_archive(extract_output)

        if dlg.chk_process_gis_data.isChecked():
            make_folder(output + '/DEM')
            overlay = dlg.file_gis_clip_layer.filePath()
            raster = output + '/unprocessed/DEM/na_con_3s.tif'
            clip_raster(dlg, overlay, raster, output + '/DEM/qrvn_dem.tif')

    def download_flow_direction(self, dlg, region):
        output = dlg.file_gis_download_output.filePath()
        url = 'https://data.hydrosheds.org/file/hydrosheds-v1-dir/hyd_na_dir_15s.zip'
        dlg.lbl_progressbar.setText('Downloading flow direction')
        make_folder(output + '/unprocessed/flow_dir')
        extract_output = output + '/unprocessed/flow_dir/flowdir.zip'
        download_request(dlg, url, extract_output)
        dlg.lbl_progressbar.setText('Extracting...')
        extract_archive(extract_output)

        if dlg.chk_process_gis_data.isChecked():
            make_folder(output + '/flow_dir')
            overlay = dlg.file_gis_clip_layer.filePath()
            raster = output + '/unprocessed/flow_dir/hyd_na_dir_15s.tif'
            clip_raster(dlg, overlay, raster, output + '/flow_dir/qrvn_flowdir.tif')

    def download_lakes(self, dlg):
        output = dlg.file_gis_download_output.filePath()
        url = 'https://data.hydrosheds.org/file/hydrolakes/HydroLAKES_polys_v10_shp.zip'
        dlg.lbl_progressbar.setText('Downloading lakes')
        make_folder(output + '/unprocessed/lakes')
        extract_output = output + '/unprocessed/lakes/lakes.zip'
        download_request(dlg, url, extract_output)
        dlg.lbl_progressbar.setText('Extracting...')
        extract_archive(extract_output)

        if dlg.chk_process_gis_data.isChecked():
            make_folder(output + '/lakes')
            overlay = dlg.file_gis_clip_layer.filePath()
            vector = output + '/unprocessed/lakes/HydroLAKES_polys_v10.shp'
            clip_vector(dlg,overlay, vector, output + '/lakes/qrvn_lakes.shp', False)

    def download_bankfull(self, dlg):
        output = dlg.file_gis_download_output.filePath()
        url = 'https://zenodo.org/record/61758/files/hydrosheds_wqd.tgz?download=1'
        dlg.lbl_progressbar.setText('Downloading bankfull width')
        make_folder(output + '/unprocessed/bkf_width')
        extract_output = output + '/unprocessed/bkf_width/bankfull.tgz'
        download_request(dlg, url, extract_output)
        dlg.lbl_progressbar.setText('Extracting...')
        extract_archive(extract_output)

        if dlg.chk_process_gis_data.isChecked():
            make_folder(output + '/bkf_width')
            overlay = dlg.file_gis_clip_layer.filePath()
            vector = output + '/unprocessed/bkf_width/nariv.shp'
            clip_vector(dlg, overlay, vector, output + '/bkf_width/qrvn_bankfull.shp', False)
