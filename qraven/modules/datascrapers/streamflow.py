import requests, csv
from html.parser import HTMLParser

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

    def exportRVT(data,path,mode):
        totalLines = 0
        isContent = False
        observation = []

        if mode == 'web':
            for i, line in enumerate(data.split('\n')):
                if 'Station' in line and 'Date' in line and 'Débit' in line:
                    isContent = True
                elif isContent:
                    if line !='':
                        content = line.split()
                        try:
                            content[2]
                            observation.append(content)
                        except:
                            text = content[0] + ' ' + content[1] + ' -1.2345' + ' MJ'
                            observation.append(text.split())
                        totalLines +=1
        elif mode == 'local':
            with open(data,'r') as file:
                for line in file:
                    content = line.split()
                    #print(line)
                    try:
                        content[2]
                        observation.append(content)
                    except:
                        text = content[0] + ' ' + content[1] + ' -1.2345' + ' MJ'
                        observation.append(text.split())
            del observation[0]
            totalLines = len(observation)
        
        with open(path,'w') as rvt:
            rvt.write(':ObservationData HYDROGRAPH <Basin_ID or HRU_ID> m3/s \n')
            rvt.write('\t'+observation[0][1].replace('/','-') + ' 00:00:00 ' + str(totalLines))
            for line in observation:
                rvt.write('\n\t'+line[2])
            rvt.write('\n:EndObservationData')


class watersurvey:

    def sendRequest(type,value,regulation,status):
        
        baseurl = 'https://wateroffice.ec.gc.ca/search/historical_results_e.html'#?search_type='+searchtype
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
                    del tmplist[-3:]
                    results.append(tmplist.copy())
                    tmplist.clear()
                    count = 0
                    newlist = False
                except:
                    tmplist.append('')
                    del tmplist[-3:]
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

        return r.text
        
        
    def exportRVT(data,path):
        reader = csv.reader(data.split('\n'))
        observation =[]
        
        for row in reader:
            observation.append(row)
        del observation[:2]
        observation = [x for x in observation if x != []]
        with open(path,'w') as rvt:
            rvt.write(':ObservationData HYDROGRAPH <Basin_ID or HRU_ID> m3/s \n')
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