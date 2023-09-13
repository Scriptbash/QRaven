from qgis.core import Qgis, QgsVectorLayer, QgsRasterLayer,QgsCoordinateReferenceSystem,QgsProject,QgsProcessingFeedback
import processing
import os


def clip_raster(dlg, overlay, input_raster, output):
    #progressbar = dlg.progress_gisprocess
    #filename, extension = os.path.splitext(input_raster)
    #filename = os.path.basename(filename)
    #outputpath = os.path.dirname(input_raster)

    #f = QgsProcessingFeedback()
    #f.progressChanged.connect(qgisprogressbar)

    processing.runAndLoadResults("gdal:cliprasterbymasklayer",
                                 {'INPUT': input_raster,
                                  'MASK': overlay,
                                  'SOURCE_CRS': None,
                                  'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:4326'),
                                  'TARGET_EXTENT': None, 'NODATA': None, 'ALPHA_BAND': False,
                                  'CROP_TO_CUTLINE': True,
                                  'KEEP_RESOLUTION': False, 'SET_RESOLUTION': False, 'X_RESOLUTION': None,
                                  'Y_RESOLUTION': None,
                                  'MULTITHREADING': True, 'OPTIONS': '', 'DATA_TYPE': 0, 'EXTRA': '',
                                  'OUTPUT': output
                                  })#, feedback=f)


def clip_vector(dlg, overlay, input_vector, output):
    processing.runAndLoadResults("native:clip",
                                 {'INPUT': input_vector,
                                  'OVERLAY': overlay,
                                  'OUTPUT': output
                                  })#, feedback=f)


def join_attributes(dlg, source1, source2, field1, field2, fieldscopy):
    output = dlg.file_processsoil.filePath()
    make_folder(os.path.dirname(output) + "/results")
    output = os.path.dirname(output) + '/results/qrvn_soil.shp'
    processing.runAndLoadResults("native:joinattributestable",
                                 {'INPUT': source1,
                                  'FIELD': field1,
                                  'INPUT_2': source2,
                                  'FIELD_2': field2,
                                  'FIELDS_TO_COPY': [fieldscopy],
                                  'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '',
                                  'OUTPUT': output})


def reclassify_by_table(dlg, inputlayer):
    reclassified = processing.run("native:reclassifybytable",
                                  {'INPUT_RASTER': inputlayer,
                                   'RASTER_BAND': 1,
                                   'TABLE': ['20', '99999', '0'],
                                   'NO_DATA': 0, 'RANGE_BOUNDARIES': 1,
                                   'NODATA_FOR_MISSING': False, 'DATA_TYPE': 5,
                                   'OUTPUT': 'TEMPORARY_OUTPUT'}, feedback=f)
    layer = reclassified['OUTPUT']


def polygonize(dlg, inputlayer):
    #progressbar =dlg.progress_gisprocess
    #f = QgsProcessingFeedback()
    #f.progressChanged.connect(qgisprogressbar)

    polygons = processing.run("gdal:polygonize",
                                    {'INPUT':inputlayer,
                                    'BAND':1,
                                    'FIELD':'DN',
                                    'EIGHT_CONNECTEDNESS':False,'EXTRA':'',
                                    'OUTPUT':'TEMPORARY_OUTPUT'})#,feedback=f)
    layer = polygons['OUTPUT']
    return layer


def field_calculator(dlg, layer, formula, field_name, field_type):
    calculated = processing.run("native:fieldcalculator",
                            {'INPUT':layer,
                            'FIELD_NAME':field_name,
                            'FIELD_TYPE':field_type,'FIELD_LENGTH':120,'FIELD_PRECISION':0,
                            'FORMULA': formula,
                            'OUTPUT':'TEMPORARY_OUTPUT'})
    layer = calculated['OUTPUT']
    return layer


def remove_small_areas(dlg, layer, threshold):
    cleaned = processing.run("grass7:v.clean", {'input': layer,
                                      'type': [0, 1, 2, 3, 4, 5, 6], 'tool': [10], 'threshold': '', '-b': False,
                                      '-c': True, 'output': 'TEMPORARY_OUTPUT', 'error': 'TEMPORARY_OUTPUT',
                                      'GRASS_REGION_PARAMETER': None, 'GRASS_SNAP_TOLERANCE_PARAMETER': threshold,
                                      'GRASS_MIN_AREA_PARAMETER': 0.0001, 'GRASS_OUTPUT_TYPE_PARAMETER': 0,
                                      'GRASS_VECTOR_DSCO': '', 'GRASS_VECTOR_LCO': '',
                                      'GRASS_VECTOR_EXPORT_NOCAT': False})
    layer = cleaned['OUTPUT']
    return layer


def fix_geometries(dlg, layer):
    fixed_geometries = processing.run("native:fixgeometries",
                   {'INPUT': layer, 'METHOD': 1,
                    'OUTPUT': 'TEMPORARY_OUTPUT'})
    layer = fixed_geometries['OUTPUT']
    return layer


def merge_same_polygons(dlg, layer, output):
    processing.runAndLoadResults("native:dissolve", {
        'INPUT': layer,
        'FIELD': ['Landuse_ID'], 'SEPARATE_DISJOINT': True, 'OUTPUT': output})
