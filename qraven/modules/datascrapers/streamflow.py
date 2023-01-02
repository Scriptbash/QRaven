import requests
from html.parser import HTMLParser

class cehq:
    def __init__(self):
        self.url = "https://www.cehq.gouv.qc.ca/hydrometrie/historique_donnees/ListeStation.asp?regionhydro=aucune&Tri=Non"
        
    def sendRequest(self):
        headers = {'User-Agent': 'Mozilla/5.0'}
        payload = {'lstStation':'',
                   'BtnRechercher1':'Rechercher',
                   'lstMunicipalite':'Coaticook',
                   'lstRiviere':'',
                   'lstRegion':''  
                  }

        r= requests.post(self.url,headers=headers,data=payload)
        self.html = r.text
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
    
    def downloadData(station):
        baseurl = 'https://www.cehq.gouv.qc.ca/depot/historique_donnees/fichier/'
        sufix = '_N.txt'
        link = baseurl + station + sufix
        page = requests.get(link)
        content = page.text
        return content

    def exportRVT(data):
        totalLines = 0
        isContent = False
        observation = []
        for i, line in enumerate(data.split('\n')):
            if 'Station' in line and 'Date' in line and 'Niveau' in line:
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
        with open('/Users/francis/Documents/test.rvt','w') as rvt:
            rvt.write(':ObservationData HYDROGRAPH <Basin_ID or HRU_ID> m3/s \n')
            rvt.write('\t'+observation[0][1].replace('/','-') + ' 00:00:00 ' + str(totalLines))
            for line in observation:
                rvt.write('\n\t'+line[2])
            rvt.write('\n:EndObservationData')
        print('Wrote RVT')


class watersurvey:
    # def __init__(self):
    #     print('ok')
    def sendRequest():
        #print('ok')
        searchtype = 'station_name'   #could be province
        province = 'Coaticook'
        paramtype = 'flows'
        start_year = '1850'
        end_year = '2023'
        
        baseurl = 'https://wateroffice.ec.gc.ca/search/historical_results_e.html?search_type='+searchtype
        url = baseurl + '&station_name='+province+'&parameter_type='+paramtype+'&start_year='+start_year+'&end_year='+end_year+'&minimum_years=&gross_drainage_operator=>&gross_drainage_area=&effective_drainage_operator=>&effective_drainage_area='

        # params = { 'province': province, 'parameter_type': 'levels',
        #            'start_year':'1850', 'end_year':'2023',
        #            'gross_drainage_operator':'', 'gross_drainage_area':'',
        #            'effective_drainage_operator':'','effective_drainage_area':''
        #          }
        params = { 'station_name': 'Coaticook', 'parameter_type': 'flows',
                   'start_year':'1850', 'end_year':'2023',
                   'gross_drainage_operator':'', 'gross_drainage_area':'',
                   'effective_drainage_operator':'','effective_drainage_area':''
                 }
    
        r = requests.get(url=url)
        return r.text

    def parseTable(data):
        results = []
        tmplist = []
        for line in data:
            line = line.splitlines()
            #print(line[0])
            if len(tmplist) > 7:
                del tmplist[-3:]
                results.append(tmplist.copy())
                tmplist.clear()
                tmplist.append(line[0])
            else:
                tmplist.append(line[0])
        del tmplist[-3:]
        results.append(tmplist) #Could rework this a little
        print(results)
        

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

test = cehq()
html=cehq.sendRequest(test)
parser = MyHTMLParser()
parser.feed(html)
data= parser.data
cehq.parseTable(data)

streamflowfile = cehq.downloadData('043206')
cehq.exportRVT(streamflowfile)

# parser = MyHTMLParser()
# html2 = watersurvey.sendRequest()

# parser.feed(html2)
# data = parser.data
# #print(data2)
# watersurvey.parseTable(data)


