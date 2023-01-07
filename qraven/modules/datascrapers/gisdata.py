import zipfile
import urllib.request, os
from PyQt5.QtWidgets import *

class gisScraper:
        
    def dem(self,output):
        url = 'https://data.hydrosheds.org/file/hydrosheds-v1-con/na_con_3s.zip'
        self.dlg.lbl_progressbar.setText('Downloading DEM')
        sendRequest(self,url,output)

    def flowdirection(self, output):
        url = 'https://data.hydrosheds.org/file/hydrosheds-v1-dir/hyd_na_dir_15s.zip'
        self.dlg.lbl_progressbar.setText('Downloading flow direction')
        sendRequest(self, url, output) 

    def lakes(self,output):
        url = 'https://data.hydrosheds.org/file/hydrolakes/HydroLAKES_polys_v10_shp.zip'
        self.dlg.lbl_progressbar.setText('Downloading lakes')
        sendRequest(self,url,output)
    
    def bankfull(self,output):
        url = 'https://zenodo.org/record/61758/files/hydrosheds_wqd.tgz?download=1'
        self.dlg.lbl_progressbar.setText('Downloading bankfull width')
        sendRequest(self,url,output)
    
    def soil(self, output):
        url = 'https://sis.agr.gc.ca/nsdb/ca/cac003/cac003.20110308.v3.2/ca_all_slc_v3r2.zip'
        self.dlg.lbl_progressbar.setText('Downloading soil layer')
        sendRequest(self,url,output)

        output = os.path.dirname(output)+'/soil.dbf'
        print(output)
        url = 'https://sis.agr.gc.ca/soildata/canada/soil_name_canada_v2r20140529.dbf'
        self.dlg.lbl_progressbar.setText('Downloading soil attribute table')
        sendRequest(self,url,output)


def sendRequest(self, url, output):
    
    req = urllib.request.Request(
                                url, 
                                data=None, 
                                headers={
                                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                                }
                                )
    response = urllib.request.urlopen(req)

    totalsize = response.info()['Content-Length']
    currentsize = 0
    chunk = 4096
    with open(output,'wb') as file:
        while 1:
            data = response.read(chunk)
            if not data:
                print ("Download complete.")
                break
            file.write(data)
            currentsize += chunk
            try:    #Try required for the soil dbf file... maybe too small
                Handle_Progress(self,currentsize,int(totalsize))
            except:
                self.dlg.progressBar.setValue(100)


def Handle_Progress(self,blocksize, totalsize):

    ## calculate the progress
    #readed_data = blocknum * blocksize
    if totalsize > 0:
        download_percentage = (blocksize / totalsize) * 100 
        self.dlg.progressBar.setValue(download_percentage)
        #print(download_percentage)
        QApplication.processEvents()

