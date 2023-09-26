from qgis.core import QgsVectorLayer
from owslib.ogcapi.features import Features
import processing

# Todo Create a shapefile for the stations, check if regulation and drainage area info can be get with the API
class StreamFlow:
    def __init__(self, dlg):
        self.dlg = dlg
        self.oafeat = Features("https://api.weather.gc.ca/")

    def define_area(self):
        input_polygon = self.dlg.file_thunder_polygon.filePath()
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
        self.bbox = bbox

    def get_hydro_station_by_poly(self):
        self.define_area()

        station_data = self.oafeat.collection_items(
            "hydrometric-stations",
            bbox=self.bbox,
            limit=10000
        )
        if "features" in station_data:
            stations = []

            for feature in station_data['features']:
                stations.append(feature['properties']['STATION_NUMBER'])
            return stations
        else:
            print("No hydrometric stations were found at this location.")

    def get_hydro_station_by_name(self):
        pass

    def get_hydro_data(self, selected_structures):

        stations = self.get_hydro_station_by_poly()
        start_date = self.dlg.date_thunder_start.date().toPyDate()
        end_date = self.dlg.date_thunder_end.date().toPyDate()
        output = self.dlg.file_thunder_output.filePath()

        for station in stations:
            hydro_data = self.oafeat.collection_items(
                "hydrometric-daily-mean",
                bbox=self.bbox,
                datetime=f"{start_date}/{end_date}",
                STATION_NUMBER=station,
                sortby= '+DATE',
                limit=10000
            )
            discharge = []
            if hydro_data['features']:
                for data in hydro_data['features']:
                    if data['properties']['DISCHARGE'] is None:
                        discharge.append(-1.2345)
                    else:
                        discharge.append(data['properties']['DISCHARGE'])
                for structure in selected_structures:
                    with open(output + '/' + structure + '/' + station + '.rvt', 'w') as rvt:
                        rvt.write(':ObservationData HYDROGRAPH <hruid> 1.0 m3/s \n')
                        rvt.write('\t' + str(start_date) + ' 00:00:00 ' + str(len(discharge)))
                        for value in discharge:
                            rvt.write('\n\t' + str(value))
                        rvt.write('\n:EndObservationData')
                print('Done.')
            else:
                print('There are no data for station ' + station + ' at the selected dates.')
