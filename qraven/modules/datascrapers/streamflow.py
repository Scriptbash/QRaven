import requests
from html.parser import HTMLParser

class cehq:
    def __init__(self):
        self.url = "https://www.cehq.gouv.qc.ca/hydrometrie/historique_donnees/ListeStation.asp?regionhydro=aucune&Tri=Non"
        
    def sendRequest(self):
        headers = {'User-Agent': 'Mozilla/5.0'}
        payload = {'lstStation':'',
                   'BtnRechercher1':'Rechercher',
                   'lstMunicipalite':'Sainte-Catherine',
                   'lstRiviere':'',
                   'lstRegion':''  
                  }

        r= requests.post(self.url,headers=headers,data=payload)
        self.html = r.text
        return r.text
        #self.parseTable()

    def parseTable(data):
        valu= []
        for line in data:

            line = line.splitlines()
            if line != '' and line[0] !='':
            #print(line)
                valu.append(line)

        newlist = []
        tmplist = []
        reached = False
        for data in valu:
            if data[0].isnumeric() and len(data[0]) > 1:
                count = 0
                reached = True
                tmplist.append(data[0])
                #print(data)
            elif reached == False:
                pass
            elif count <=8:
                text = data[0].replace('\xa0','')
                if text !='':
                    tmplist.append(text)
                count+=1
                if count == 8 and reached == True:
                    newlist.append(tmplist.copy())
                    tmplist.clear()
                    reached = False
        print(newlist)

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




