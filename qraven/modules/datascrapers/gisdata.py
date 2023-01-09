import urllib.request, os, zipfile, tarfile, processing
from PyQt5.QtWidgets import *
from qgis.core import Qgis, QgsVectorLayer, QgsRasterLayer,QgsCoordinateReferenceSystem,QgsProject,QgsProcessingFeedback

class gisScraper:
        
    def dem(self,output):
        url = 'https://data.hydrosheds.org/file/hydrosheds-v1-con/na_con_3s.zip'
        self.dlg.lbl_progressbar.setText('Downloading DEM')
        sendRequest(self,url,output)
        self.dlg.lbl_progressbar.setText('Extracting...')
        extractarchives(output)

    def flowdirection(self, output):
        url = 'https://data.hydrosheds.org/file/hydrosheds-v1-dir/hyd_na_dir_15s.zip'
        self.dlg.lbl_progressbar.setText('Downloading flow direction')
        sendRequest(self, url, output) 
        self.dlg.lbl_progressbar.setText('Extracting...')
        extractarchives(output)

    def lakes(self,output):
        url = 'https://data.hydrosheds.org/file/hydrolakes/HydroLAKES_polys_v10_shp.zip'
        self.dlg.lbl_progressbar.setText('Downloading lakes')
        sendRequest(self,url,output)
        self.dlg.lbl_progressbar.setText('Extracting...')
        extractarchives(output)
    
    def bankfull(self,output):
        url = 'https://zenodo.org/record/61758/files/hydrosheds_wqd.tgz?download=1'
        self.dlg.lbl_progressbar.setText('Downloading bankfull width')
        sendRequest(self,url,output)
        self.dlg.lbl_progressbar.setText('Extracting...')
        extractarchives(output)

    def landuse(self,output):
        url = 'https://datacube-prod-data-public.s3.ca-central-1.amazonaws.com/store/land/landcover/landcover-2020-classification.tif'
        self.dlg.lbl_progressbar.setText('Downloading landuse cover')
        sendRequest(self,url,output)
    
    def soil(self, output):
        url = 'https://sis.agr.gc.ca/cansis/nsdb/slc/v2.2/slc_v2r2_canada.zip'
        self.dlg.lbl_progressbar.setText('Downloading soil layer')
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
        overlay = QgsVectorLayer(overlay, 'watershed', "ogr")
        f = QgsProcessingFeedback()
        f.progressChanged.connect(qgisprogressbar)

        if extension == '.tif':
            #inputlayer = QgsRasterLayer(inputlayer, 'rasterlayer')
            result = processing.runAndLoadResults("gdal:cliprasterbymasklayer", 
                            {'INPUT':inputlayer,
                                'MASK':overlay,
                                'SOURCE_CRS':None,
                                'TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:4326'),
                                'TARGET_EXTENT':None,'NODATA':None,'ALPHA_BAND':False,'CROP_TO_CUTLINE':True,
                                'KEEP_RESOLUTION':False,'SET_RESOLUTION':False,'X_RESOLUTION':None,'Y_RESOLUTION':None,
                                'MULTITHREADING':True,'OPTIONS':'','DATA_TYPE':0,'EXTRA':'',
                                'OUTPUT':'TEMPORARY_OUTPUT'
                            },feedback=f)
        else:
            #inputlayer = QgsVectorLayer(inputlayer, 'vectorlayer', "ogr")
            result = processing.run("native:clip", 
                            {'INPUT':inputlayer,
                                'OVERLAY':overlay,
                                'OUTPUT':'TEMPORARY_OUTPUT'
                            },feedback=f)
            
            layer = result['OUTPUT']
        #layer.setName('grille_information')
            QgsProject.instance().addMapLayer(layer)

    def joinattributes(self, inputlayer):
        print('OK')

def sendRequest(self, url, output):
    
    req = urllib.request.Request(
                                url, 
                                data=None, 
                                headers={
                                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                                }
                                )
    response = urllib.request.urlopen(req, timeout=10)

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
    extractpath = os.path.dirname(file)
    filename, extension = os.path.splitext(file)
    if extension == '.zip':
        with zipfile.ZipFile(file, 'r') as zip_ref:
            for elem in zip_ref.namelist() :
                    zip_ref.extract(elem, extractpath)
                    QApplication.processEvents() 

    elif extension == '.tgz' or extension == '.tar':
        tar = tarfile.open(file)
        for member in tar.getmembers():
            if member.isreg():  # skip if the TarInfo is not files
                if 'nariv' in member.name:
                    member.name = os.path.basename(member.name) # remove the path by reset it
                    tar.extract(member,extractpath) # extract
                    QApplication.processEvents()  
    os.remove(file)


def qgisprogressbar(progress):
    progressbar.setValue(progress)
    #self.dlg.progress_gisprocess.setValue(progress)
    QApplication.processEvents()