import requests, csv, datetime
from html.parser import HTMLParser
import re

class cehq:
    
    def sendRequest(city,river,region):
        url = "https://www.cehq.gouv.qc.ca/hydrometrie/historique_donnees/ListeStation.asp?regionhydro=aucune&Tri=Non"
        headers = {'User-Agent': 'Mozilla/5.0'}
        payload = {'lstStation':'',
                   'BtnRechercher1':'Rechercher',
                   'lstMunicipalite':city.encode("latin-1"),
                   'lstRiviere':river.encode("latin-1"),
                   'lstRegion':region.encode("latin-1")  
                  }

        r= requests.post(url,headers=headers,data=payload)
        return r.text

    def parseTable(data):
        valu= []
        for line in data:
            line = line.splitlines()
            if line != '' and line[0] !='':
                valu.append(line)
        stations = []
        tmplist = []
        reachedtable = False
        for data in valu:
            if data[0].isnumeric() and len(data[0]) > 1:
                count = 0
                reachedtable = True
                tmplist.append(data[0])
            elif reachedtable == False:
                pass
            elif count <=8:
                text = data[0].replace('\xa0','')
                if text !='':
                    tmplist.append(text)
                count+=1
                if count == 8 and reachedtable == True:
                    stations.append(tmplist.copy())
                    tmplist.clear()
                    reachedtable = False
        stations = [x for x in stations if x[7] != 'Niveau']
        return stations
    
    def downloadData(station):
        baseurl = 'https://www.cehq.gouv.qc.ca/depot/historique_donnees/fichier/'
        sufix = '_Q.txt'
        link = baseurl + station + sufix
        page = requests.get(link)
        content = page.text
        return content
    
    def extractData(data,id):
        isContent = False
        observationtmp = []
        lat = ""
        lon = ""
        area = ""

        for i, line in enumerate(data.split('\n')):
            if 'Bassin versant' in line:
                line = line.split()
                area = line[2]

            if 'Coordonnées' in line:
                line = line.split()
                lat = line[2]+line[3]+line[4]+'N'   #Add the degrees minutes seconds coordinate of the station... could break at some point
                lon = line[6]+line[7]+line[8]+'W'
            
            if 'Station' in line and 'Date' in line and 'Débit' in line:
                isContent = True
            elif isContent:
                if line !='':
                    content = line.split()
                    try:
                        content[2]
                        observationtmp.append(content)
                    except:
                        text = content[0] + ' ' + content[1] + ' -1.2345' + ' MJ'
                        observationtmp.append(text.split())
        
        lat = toLatLon(lat)
        lon = toLatLon(lon)
        stationinfo = [id, lat, lon, area]
        return observationtmp, stationinfo


    def exportRVT(data,path,mode,startdate,enddate):
        isContent = False
        observationtmp = []
      
        if mode == 'web':
            observationtmp = data
        elif mode == 'local':
            isContent = False
            with open(data,'r',encoding = 'latin-1') as file:
                for line in file:
                    content = line.split()
                    if 'Station' in content and 'Date' in line and 'Débit' in content:
                        isContent = True
                    elif isContent:
                        try:
                            content[2]
                            observationtmp.append(content)
                        except:
                            text = content[0] + ' ' + content[1] + ' -1.2345' + ' MJ'
                            observationtmp.append(text.split())
            del observationtmp[0]
        
        observation =[]
        for row in observationtmp:
            obsdate = datetime.datetime.strptime(row[1], '%Y/%m/%d')
            if  obsdate.date() >= startdate and obsdate.date() < enddate:
                observation.append(row)
            else:
                pass
                
        totalLines = len(observation)
        with open(path,'w') as rvt:
            rvt.write(':ObservationData HYDROGRAPH <Basin_ID or HRU_ID> 1.0 m3/s \n')
            rvt.write('\t'+observation[0][1].replace('/','-') + ' 00:00:00 ' + str(totalLines))
            for line in observation:
                rvt.write('\n\t'+line[2])
            rvt.write('\n:EndObservationData')


class watersurvey:

    def sendRequest(type,value,regulation,status):
        
        baseurl = 'https://wateroffice.ec.gc.ca/search/historical_results_e.html'
        params = { 'search_type':type,type: value, 
                   'parameter_type': 'flows', 'start_year':'1850', 
                   'end_year':'2023', 'minimum_years':'', 
                   'regulation' : regulation, 'station_status': status,
                   'gross_drainage_operator':'>', 'gross_drainage_area':'',
                   'effective_drainage_operator':'>','effective_drainage_area':''
                 }
       
        r = requests.get(url=baseurl,params=params)

        return r.text

    def parseTable(data):
        results = []
        tmplist = []
        count = 0
        newlist = False
        
        for line in data:
            line = line.splitlines()
            if newlist == True and count == 2:
                try:
                    float(line[0].replace(",",'.'))
                    tmplist.append(line[0])
                    #del tmplist[-3:]
                    results.append(tmplist.copy())
                    tmplist.clear()
                    count = 0
                    newlist = False
                except:
                    tmplist.append('')
                    #del tmplist[-3:]
                    results.append(tmplist.copy())
                    tmplist.clear()
                    tmplist.append(line[0])
                    count = 0
                    newlist = False
            elif '°' in line[0]:
                count+=1
                tmplist.append(line[0])
                newlist = True
            else:
                tmplist.append(line[0])
        
        results = [x for x in results if x != []]
        
        #Brings the station IDs to the front of the lists
        for result in results:
            try:
                result.insert(0, result.pop(3))
                result[-3] = toLatLon(result[-3])
                result[-2] = toLatLon(result[-2])
            except:
                print("Couldn't move the id in front of the string.")
        return results


    def downloadData(id):
        url = 'https://wateroffice.ec.gc.ca/search/relay_e.html'
        headers = {'results_type': 'historical',
                   'download': 'download?',
                   'check[]': id+',1,1959,2021,Flow'
                  }
        
        s=requests.session()
        s.get(url,params=headers,)

        headers2 = {'dt': 'dd',
                   'df': 'ddf',
                   'md': '1',
                   'ext': 'csv'
                  }

        url2= 'https://wateroffice.ec.gc.ca/download/report_e.html'
        r = s.get(url2,params=headers2,)

        s.close()
        return r.text
        
    def fetchDates(data):
        reader = csv.reader(data.split('\n'))
        observationtmp =[]
        for row in reader:
            observationtmp.append(row)
        del observationtmp[:2]
        observationtmp = [x for x in observationtmp if x != []]
        startdate = observationtmp[0][2]
        enddate = observationtmp[-1][2]
        return startdate, enddate
        

    def exportRVT(data,path, startdate, enddate):
        reader = csv.reader(data.split('\n'))
        observationtmp =[]
        observation = []
        
        for row in reader:
            observationtmp.append(row)
        del observationtmp[:2]
        observationtmp = [x for x in observationtmp if x != []]
        
        for row in observationtmp:
            obsdate = datetime.datetime.strptime(row[2], '%Y/%m/%d')
            if  obsdate.date() >= startdate and obsdate.date() < enddate:
                observation.append(row)
            else:
                pass

        with open(path,'w') as rvt:
            rvt.write(':ObservationData HYDROGRAPH <Basin_ID or HRU_ID> 1.0 m3/s \n')
            rvt.write('\t'+observation[0][2].replace('/','-') + ' 00:00:00 ' + str(len(observation)))
            for line in observation:
                if line[3] != '':
                    rvt.write('\n\t' + line[3])
                else:
                    rvt.write('\n\t' + '-1.2345')
            rvt.write('\n:EndObservationData')


class MyHTMLParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.data = []
        self.capture = False

    def handle_starttag(self, tag, attrs):
        if tag in ('td'):
            self.capture = True

    def handle_endtag(self, tag):
        if tag in ('td'):
            self.capture = False

    def handle_data(self, data):
        if self.capture:
            self.data.append(data)


def toLatLon(coord):
    deg, minutes, seconds, direction =  re.split('[°\'"]', coord)
    newcoord=(abs(float(deg)) + (float(minutes)/60) + (float(seconds)/(3600))) * (-1 if direction.strip() in ['W', 'S'] else 1)
    return newcoord