from qgis.core import QgsVectorLayer, QgsField, QgsFeature, QgsGeometry, QgsProject, QgsVectorFileWriter, \
    QgsCoordinateReferenceSystem, QgsCoordinateTransform
from qgis.PyQt.QtCore import *
from owslib.ogcapi.features import Features
from osgeo import ogr, osr
import json
import re

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
            geom = feat.geometry()
            # Extract bounding box
            bbox = geom.boundingBox()
            xmin, ymin, xmax, ymax = bbox.toRectF().getCoords()
            bbox = [str(round(xmin, 2)), str(round(ymin, 2)), str(round(xmax, 2)), str(round(ymax, 2))]

            # Get the area of the watershed
            if crs != 'EPSG:4326':
                desired_crs = QgsCoordinateReferenceSystem(crs)  # keep the original crs
            else:
                desired_crs = QgsCoordinateReferenceSystem('EPSG:3348')  # Reproject the layer in metric
            transform = QgsCoordinateTransform(layer.crs(), desired_crs, QgsProject.instance())
            geom.transform(transform)
            area_km2 = geom.area() / 1e6  # Convert square meters to square kilometers
        print('Bounding box extraction done.')
        self.bbox = bbox
        self.area = round(area_km2, 3)
        print("Watershed's drainage area is : ", self.area, ' km2')

    def get_hydro_station_by_poly(self):
        self.define_area()

        station_data = self.oafeat.collection_items(
            "hydrometric-stations",
            bbox=self.bbox,
            limit=10000
        )
        if "features" in station_data:

            # Open the polygon shapefile
            input_polygon = self.dlg.file_thunder_polygon.filePath()
            polygon_datasource = ogr.Open(input_polygon)
            polygon_layer = polygon_datasource.GetLayer()
            polygon_feature = polygon_layer.GetNextFeature()
            polygon_geometry = polygon_feature.GetGeometryRef()

            stations = []
            # Iterate through the point features and check if they intersect with the polygon
            for feature in station_data['features']:
                point_geometry = ogr.CreateGeometryFromJson(json.dumps(feature['geometry']))
                if polygon_geometry.Intersects(point_geometry):
                    stations.append([feature['properties']['STATION_NUMBER'],
                                     feature['geometry']['coordinates'][0],
                                     feature['geometry']['coordinates'][1]])
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
                STATION_NUMBER=station[0],
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
                    with open(output + '/' + structure + '/' + station[0] + '.rvt', 'w') as rvt:
                        rvt.write(':ObservationData HYDROGRAPH <hruid> 1.0 m3/s \n')
                        rvt.write('\t' + str(start_date) + ' 00:00:00 ' + str(len(discharge)))
                        for value in discharge:
                            rvt.write('\n\t' + str(value))
                        rvt.write('\n:EndObservationData')
                print('Done.')
            else:
                print('There are no data for station ' + station[0] + ' at the selected dates.')
        self.create_station_layer(stations)

    def create_station_layer(self, stations):
        output = self.dlg.file_thunder_output.filePath()
        output = output + '/BasinMaker/Data/gauges/qrvn_stations.shp'

        # Creates layer
        vl = QgsVectorLayer('Point', "qrvn_stations", "memory")
        pr = vl.dataProvider()

        # Adds fields
        pr.addAttributes([
            QgsField("id", QVariant.Int),
            QgsField("name", QVariant.String),
            QgsField("drain_area", QVariant.Double, "double", 10, 3),
            QgsField("source", QVariant.String)])
        vl.updateFields()  # tell the vector layer to fetch changes from the provider

        for station in stations:
            station_id = re.sub("[^0-9]", "", station[0])
            # Creates a feature
            fet = QgsFeature()
            # Sets the geometry
            pt = QgsGeometry.fromWkt('Point(' + str(station[1]) + ' ' + str(station[2]) + ')')
            fet.setGeometry(pt)
            # Sets the attributes
            fet.setAttributes([int(station_id), station[0], self.area, "CA"])
            # Adds the feature
            pr.addFeatures([fet])
        # update layer's extent when new features have been added
        # because change of extent in provider is not propagated to the layer
        vl.updateExtents()
        if vl.isValid():
            # Save the layer to the specified shapefile path
            QgsVectorFileWriter.writeAsVectorFormat(vl, output, 'UTF-8', vl.crs(), 'ESRI Shapefile')
            station_layer = QgsVectorLayer(output, "qrvn_stations", "ogr")
            QgsProject.instance().addMapLayer(station_layer)
