import urllib.request, os, zipfile, tarfile, shutil, processing
from PyQt5.QtWidgets import *
from qgis.core import Qgis, QgsVectorLayer, QgsRasterLayer,QgsCoordinateReferenceSystem,QgsProject,QgsProcessingFeedback

class gisScraper:
        
    def dem(self,output):
        url = 'https://data.hydrosheds.org/file/hydrosheds-v1-con/na_con_3s.zip'
        self.dlg.lbl_progressbar.setText('Downloading DEM')
        output+='/dem.zip'
        sendRequest(self,url,output)
        self.dlg.lbl_progressbar.setText('Extracting...')
        extractarchives(output)

    def flowdirection(self, output):
        url = 'https://data.hydrosheds.org/file/hydrosheds-v1-dir/hyd_na_dir_15s.zip'
        self.dlg.lbl_progressbar.setText('Downloading flow direction')
        output+='/flowdir.zip'
        sendRequest(self, url, output) 
        self.dlg.lbl_progressbar.setText('Extracting...')
        extractarchives(output)

    def lakes(self,output):
        url = 'https://data.hydrosheds.org/file/hydrolakes/HydroLAKES_polys_v10_shp.zip'
        self.dlg.lbl_progressbar.setText('Downloading lakes')
        output+='/lakes.zip'
        sendRequest(self,url,output)
        self.dlg.lbl_progressbar.setText('Extracting...')
        extractarchives(output)
    
    def bankfull(self,output):
        url = 'https://zenodo.org/record/61758/files/hydrosheds_wqd.tgz?download=1'
        self.dlg.lbl_progressbar.setText('Downloading bankfull width')
        output+='/bankfull.tgz'
        sendRequest(self,url,output)
        self.dlg.lbl_progressbar.setText('Extracting...')
        extractarchives(output)

    def landuse(self,output):
        url = 'https://datacube-prod-data-public.s3.ca-central-1.amazonaws.com/store/land/landcover/landcover-2020-classification.tif'
        self.dlg.lbl_progressbar.setText('Downloading landuse cover')
        output+='/landuse.tif'
        sendRequest(self,url,output)
    
    def soil(self, output):
        url = 'https://sis.agr.gc.ca/cansis/nsdb/slc/v2.2/slc_v2r2_canada.zip'
        self.dlg.lbl_progressbar.setText('Downloading soil layer')
        output+='/soil.zip'
        sendRequest(self,url,output)
        self.dlg.lbl_progressbar.setText('Extracting...')
        extractarchives(output)

        # output = os.path.dirname(output)+'/soil.dbf'
        # url = 'https://sis.agr.gc.ca/soildata/canada/soil_name_canada_v2r20140529.dbf'
        # self.dlg.lbl_progressbar.setText('Downloading soil attribute table')
        # sendRequest(self,url,output)

    def cliplayer(self, overlay, inputlayer):
        global progressbar 
        progressbar =self.dlg.progress_gisprocess
        filename, extension = os.path.splitext(inputlayer)
        filename = os.path.basename(filename)
        outputpath = os.path.dirname(inputlayer)

        f = QgsProcessingFeedback()
        f.progressChanged.connect(qgisprogressbar)

        if filename == 'HydroLAKES_polys_v10':
                outfilename = 'qrvn_lakes.shp'
        elif filename == 'nariv':
            outfilename =  'qrvn_bankfull.shp'
        elif filename == 'slc_v2r2_canada':
            outfilename =  'qrvn_soiltmp.shp'
        elif filename == 'na_con_3s':
            outfilename = 'qrvn_DEM.tif'
        elif filename == 'hyd_na_dir_15s':
            outfilename =  'qrvn_flowdir.tif'
        else:
            outfilename = 'tmp_landuse.tif'

        if filename !='landuse' and filename != 'slc_v2r2_canada':
            makefolders(outputpath+"/results")
            output = outputpath+'/results/'+outfilename
        else:
            output = outputpath+'/'+outfilename

        if extension == '.tif': #input layer is a raster
            if filename !='landuse':
                processing.runAndLoadResults("gdal:cliprasterbymasklayer", 
                                                {'INPUT':inputlayer,
                                                    'MASK':overlay,
                                                    'SOURCE_CRS':None,
                                                    'TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:4326'),
                                                    'TARGET_EXTENT':None,'NODATA':None,'ALPHA_BAND':False,'CROP_TO_CUTLINE':True,
                                                    'KEEP_RESOLUTION':False,'SET_RESOLUTION':False,'X_RESOLUTION':None,'Y_RESOLUTION':None,
                                                    'MULTITHREADING':True,'OPTIONS':'','DATA_TYPE':0,'EXTRA':'',
                                                    'OUTPUT':output
                                                },feedback=f)
            else:
                processing.run("gdal:cliprasterbymasklayer", 
                                {'INPUT':inputlayer,
                                    'MASK':overlay,
                                    'SOURCE_CRS':None,
                                    'TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:4326'),
                                    'TARGET_EXTENT':None,'NODATA':None,'ALPHA_BAND':False,'CROP_TO_CUTLINE':True,
                                    'KEEP_RESOLUTION':False,'SET_RESOLUTION':False,'X_RESOLUTION':None,'Y_RESOLUTION':None,
                                    'MULTITHREADING':True,'OPTIONS':'','DATA_TYPE':0,'EXTRA':'',
                                    'OUTPUT':output
                                },feedback=f)
            
        else:   #input layer is a shapefile 
            if filename !='slc_v2r2_canada':
                processing.runAndLoadResults("native:clip", 
                                                {'INPUT':inputlayer,
                                                    'OVERLAY':overlay,
                                                    'OUTPUT':output
                                                },feedback=f)
            else:
                processing.run("native:clip", 
                                {'INPUT':inputlayer,
                                    'OVERLAY':overlay,
                                    'OUTPUT':output
                                },feedback=f)
            

    def joinattributes(self,inputlayer,table,field1,field2,fieldscopy):
        output = self.dlg.file_processsoil.filePath()
        makefolders(os.path.dirname(output)+"/results")
        output = os.path.dirname(output)+'/results/qrvn_soil.shp'
  
        processing.runAndLoadResults("native:joinattributestable", 
                                        {'INPUT':inputlayer,
                                        'FIELD':field1,
                                        'INPUT_2':table,
                                        'FIELD_2':field2,
                                        'FIELDS_TO_COPY':[fieldscopy],
                                        'METHOD':1,'DISCARD_NONMATCHING':False,'PREFIX':'',
                                        'OUTPUT':output})


    def polygonize(self,inputlayer):
        global progressbar 
        progressbar =self.dlg.progress_gisprocess
        f = QgsProcessingFeedback()
        f.progressChanged.connect(qgisprogressbar)
        reclassified = processing.run("native:reclassifybytable", 
                            {'INPUT_RASTER':inputlayer,
                            'RASTER_BAND':1,
                            'TABLE':['20','99999','0'],
                            'NO_DATA':0,'RANGE_BOUNDARIES':1,
                            'NODATA_FOR_MISSING':False,'DATA_TYPE':5,
                            'OUTPUT':'TEMPORARY_OUTPUT'},feedback=f)
        layer = reclassified['OUTPUT']

        polygons = processing.run("gdal:polygonize", 
                                        {'INPUT':layer,
                                        'BAND':1,
                                        'FIELD':'DN',
                                        'EIGHT_CONNECTEDNESS':False,'EXTRA':'',
                                        'OUTPUT':'TEMPORARY_OUTPUT'},feedback=f)
        layer = polygons['OUTPUT']

        output = self.dlg.file_processlanduse.filePath()
        makefolders(os.path.dirname(output)+"/results")
        output = os.path.dirname(output)+'/results/qrvn_landuse.tif'
        processing.runAndLoadResults("native:fieldcalculator", 
                        {'INPUT':layer,
                        'FIELD_NAME':'LAND_USE_C',
                        'FIELD_TYPE':2,'FIELD_LENGTH':222,'FIELD_PRECISION':0,
                        'FORMULA':'if("DN"=1,\'FOREST\',if("DN"=2,\'FOREST\',if("DN"=5,\'FOREST\',if("DN"=6,\'FOREST\',if("DN"=8,\'GRASSLAND\',if("DN"=10,\'GRASSLAND\',if("DN"=11,\'GRASSLAND\',if("DN"=12,\'GRASSLAND\',if("DN"=13,\'OPEN\',if("DN"=14,\'WETLAND\',if("DN"=15,\'AGRICULTURE\',if("DN"=16,\'OPEN\',if("DN"=17,\'URBAN\',if("DN"=18,\'WATER\',if("DN"=19,\'NA\',\'NA\')))))))))))))))',
                        'OUTPUT':output})


def sendRequest(self, url, output):
    timeout = self.dlg.spin_connection_timeout.value()
    req = urllib.request.Request(
                                url, 
                                data=None, 
                                headers={
                                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                                }
                                )
    response = urllib.request.urlopen(req, timeout=timeout)

    totalsize = response.info()['Content-Length']
    currentsize = 0
    chunk = 4096
    with open(output,'wb') as file:
        while 1:
            data = response.read(chunk)
            if not data:
                #print ("Download complete.")
                break
            file.write(data)
            currentsize += chunk
            try:    #Try required for the soil dbf file... maybe file size too small
                Handle_Progress(self,currentsize,int(totalsize))
            except:
                self.dlg.progress_gisdownload.setValue(100)


def Handle_Progress(self,blocksize, totalsize):
    if totalsize > 0:
        download_percentage = (blocksize / totalsize) * 100 
        self.dlg.progress_gisdownload.setValue(download_percentage)
        QApplication.processEvents()


def extractarchives(file):
    folder = os.path.dirname(file)
    filename, extension = os.path.splitext(file)

    if extension == '.zip':
        with zipfile.ZipFile(file, 'r') as zip_ref:
            for elem in zip_ref.namelist():
                filename = os.path.basename(elem)
                # skip directories
                if not filename:
                    continue
                source = zip_ref.open(elem)
                target = open(os.path.join(folder, filename), "wb")
                with source, target:
                    shutil.copyfileobj(source, target)
                QApplication.processEvents() 

    elif extension == '.tgz' or extension == '.tar':
        tar = tarfile.open(file)
        for member in tar.getmembers():
            if member.isreg():  # skip if the TarInfo is not files
                if 'nariv' in member.name:
                    member.name = os.path.basename(member.name)
                    tar.extract(member,folder) # extract
                    QApplication.processEvents()  
    os.remove(file)


def qgisprogressbar(progress):
    progressbar.setValue(progress)
    #self.dlg.progress_gisprocess.setValue(progress)
    QApplication.processEvents()


def makefolders(path):
    if not os.path.exists(path):
        os.makedirs(path)
