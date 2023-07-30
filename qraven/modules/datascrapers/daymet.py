from PyQt5.QtWidgets import QApplication
from qgis.core import QgsVectorLayer
import processing
import urllib.request
from ..utilities import merge_netcdf, check_missing_dates, fill_missing_dates


class Daymet:

    def get_search_criteria(self, dlg):
        output_folder = dlg.file_daymet_output.filePath()
        start_date = dlg.date_daymet_start_date.date().toPyDate()
        end_date = dlg.date_daymet_end_date.date().toPyDate()
        selected_variables = dlg.list_daymet_variables.selectedItems()
        variables = ""
        if selected_variables:
            for item in selected_variables:
                variables += item.text() + ' '
        if start_date and end_date and variables:
            dlg.lbl_daymet_error.clear()
            bbox = self.define_area(dlg)
            self.get_data(bbox, start_date, end_date, variables, output_folder, dlg)
        else:
            dlg.lbl_daymet_error.setText("At least one variable must be selected.")

    def define_area(self, dlg):
        input_polygon = dlg.file_daymet_polygon.filePath()
        layer = QgsVectorLayer(input_polygon, "extent", "ogr")
        crs = layer.crs().authid()
        if crs != 'EPSG:4326':
            print('CRS mismatch... input layer CRS is ' + crs)
            print('Reprojecting layer to EPSG:4326...')
            params = {
                        'INPUT': layer,
                        'TARGET_CRS': 'EPSG:4326',
                        'OUTPUT': 'memory:Reprojected'
                     }
            reprojected = processing.run('native:reprojectlayer', params)
            layer = reprojected['OUTPUT']
            print('Reprojection done.')

        print("Extracting bounding box...")
        feats = [feat for feat in layer.getFeatures()]

        for i, feat in enumerate(feats):
            bbox = feat.geometry().boundingBox()
            xmin, ymin, xmax, ymax = bbox.toRectF().getCoords()
            bbox = [str(round(xmin, 2)), str(round(ymin, 2)), str(round(xmax, 2)), str(round(ymax, 2))]
        print('Bounding box extraction done.')
        return bbox

    def get_data(self, bbox, start, end, var, output, dlg):
        timeout = dlg.spin_connection_timeout.value()
        region = "na"
        north = bbox[3]
        west = bbox[0]
        east = bbox[2]
        south = bbox[1]

        dlg.lbl_daymet_download.setText("Initializing...")
        QApplication.processEvents()

        for variable in var.split():
            for year in range(int(start.year), int(end.year)+1):
                url = "https://thredds.daac.ornl.gov/thredds/ncss/grid/ornldaac/2129/daymet_v4_daily_" + region + "_" \
                        + variable + '_' + str(year) + ".nc?var=lat&var=lon&var=" + variable + '&north=' + north + \
                        "&west=" + west + "&east=" + east + "&south=" + south + \
                        "&disableProjSubset=on&horizStride=1&time_start=" + \
                        str(start) + "T12:00:00Z&time_end=" + str(end) + "T12:00:00Z&timeStride=1&accept=netcdf"
                req = urllib.request.Request(url)
                response = urllib.request.urlopen(req, timeout=timeout)
                totalsize = response.info()['Content-Length']
                currentsize = 0
                chunk = 4096

                filename = str(year) + variable + '.nc'
                output_file = output + "/" + filename
                dlg.lbl_daymet_download.setText("Variable " + str(var.split().index(variable) + 1) + "/" + str(len(var.split())) +
                                                " - Downloading " + filename)
                with open(output_file, 'wb') as file:
                    while 1:
                        data = response.read(chunk)
                        if not data:
                            break
                        file.write(data)
                        currentsize += chunk
                        try:  # Try required if file size too small
                            self.handle_progress(dlg, currentsize, int(totalsize))
                        except:
                            dlg.progress_daymet.setValue(100)
                if dlg.chk_daymet_insert_nan.isChecked():
                    missing_dates = check_missing_dates(output_file)
                    #print(missing_dates)
                    fill_missing_dates(output_file, missing_dates)
                else:
                    pass

            if dlg.chk_daymet_merge.isChecked():
                dlg.lbl_daymet_download.setText('Merging files...')
                QApplication.processEvents()
                merge_netcdf(output, variable)
                dlg.lbl_daymet_download.setText('Merge complete.')
        dlg.lbl_daymet_download.setText("Download complete!")
        dlg.progress_daymet.setValue(0)

    def handle_progress(self, dlg, blocksize, totalsize):
        if totalsize > 0:
            download_percentage = (blocksize / totalsize) * 100
            dlg.progress_daymet.setValue(download_percentage)
            QApplication.processEvents()
