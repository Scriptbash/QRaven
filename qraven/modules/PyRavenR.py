import csv

#Returns the number of soil layers of the model
def getSoilLayers(inputdir,separator,rvifile):
    try:
        with open(inputdir+separator+rvifile, "r") as rvi:
            rvilines = rvi.readlines()
            for line in rvilines:
                if ':SoilModel' in line:
                    soilmodelline = line.split()
                    soilmodel = soilmodelline[soilmodelline.index(':SoilModel')+1]
                    if soilmodel == 'SOIL_ONE_LAYER':
                        soil_layers = 1
                    elif soilmodel == 'SOIL_TWO_LAYER':
                        soil_layers = 2
                    elif soilmodel == 'SOIL_MULTILAYER':
                        soil_layers = int(soilmodelline[soilmodelline.index(':SoilModel')+2])
                    else:
                        print('Unknown soil model, please check your rvi file')
                        #Raise exception?
        return soil_layers
    except Exception as e:
        print('An error occured when reading the rvi file.')
        print(e)
        #self.iface.messageBar().pushMessage("Error", "An error occured when reading the rvi file. Check the python console for more details.",level=Qgis.Critical)

#Extracts the HRUs information block from the provided rvh file
def extractRVHhrus(inputdir, separator,rvhfile):
    try:
        landuseclasses = []
        vegclasses = []
        terrainclasses = []
        soilprofileclasses = []
        data=[] #List with the raw HRUs text
        hrudata=[] #List with the HRUs text cleaned up (no units, no comments)
        isheadertext = True #The line read is before the HRUs information
        isfootertext = False   #The line read is after the HRUs information
        with open(inputdir+separator+rvhfile, "r") as rvh:
            rvhlines = rvh.readlines()
            for line in rvhlines:
                if ':HRUs' in line:
                    isheadertext = False
                    #Reached the HRUs information block
                elif ':EndHRUs' in line:
                    isfootertext = True
                    #Reached the end of the HRUs information block
                if isheadertext == False and isfootertext == False:
                    line = line.replace('\t','')
                    if ',' in line:
                        cells = line.strip().split(',')
                    else:
                        cells = line.strip().split()
                    data.append(cells)
                else:
                    pass
            #Removes the useless rows
            for row in data:
                datarow = []
                for col in row:
                    if ':HRUs' in col:
                        break
                    elif ':Units' in col:
                        break
                    elif '#' in col:
                        break
                    else:
                        datarow.append(col)
                if datarow:
                    hrudata.append(datarow)
            #Extracts the column index of the useful info
            for col in range(len(hrudata[0])):
                if 'LAND_USE_CLASS' in hrudata[0][col]:
                    landuseclasscol = col-1
                elif 'TERRAIN_CLASS' in hrudata[0][col]:
                    terrainclasscol = col-1
                elif 'VEG_CLASS' in hrudata[0][col]:
                    vegclasscol = col-1
                elif 'SOIL_PROFILE' in hrudata[0][col]:
                    soilprofilecol = col-1
                else:
                    pass
            #The "-1" is to avoid counting the "":Attribute" tag
            if len(hrudata[0])-1 < len(hrudata[1]) or len(hrudata[0])-1 > len(hrudata[1]):
                print('Columns mismatch. The attributes name do not match the number of attributes. Please check your .rvh file.')
                landuseclasscol += 1
                terrainclasscol += 1
                vegclasscol += 1
                soilprofilecol += 1
                print('Shifted columns, please double check the resulting .rvp file.')

            del hrudata[0]
            #Get the classes information
            for row in range(len(hrudata)):
                if hrudata[row][landuseclasscol].strip() not in landuseclasses:
                    landuseclasses.append(hrudata[row][landuseclasscol].strip().replace(',',''))
                if hrudata[row][terrainclasscol].strip() not in terrainclasses:
                    terrainclasses.append(hrudata[row][terrainclasscol].strip().replace(',',''))
                if  hrudata[row][vegclasscol].strip() not in vegclasses:
                    vegclasses.append(hrudata[row][vegclasscol].strip().replace(',',''))
                if hrudata[row][soilprofilecol].strip() not in soilprofileclasses:
                    soilprofileclasses.append(hrudata[row][soilprofilecol].strip().replace(',',''))
        return landuseclasses,terrainclasses,vegclasses,soilprofileclasses
    except Exception as e:
        print('An error occured when reading the rvh file.')
        print(e)

#Reads the RavenParameters.dat file and returns a 2d list of the parameters and their values
def readRavenParams(ravenparametersfile):
    try:
        rvn_paramsList = []
        paramscolname = ["param", "class_type", "units", "auto","default", "min", "max"] 
        with open(ravenparametersfile, "r") as rvn_params:
            rdr = csv.DictReader(filter(lambda row: row[0]!='#', rvn_params))
            dictlist = list(rdr)
            rvn_paramsDict = [d[None] for d in dictlist if None in d] 
            for row in range(len(rvn_paramsDict)):
                for col in range(len(rvn_paramsDict[row])):
                    cell = rvn_paramsDict[row][col].split(' ') 
                    rvn_paramsList.append(cell)
            rvn_paramsList.insert(0,paramscolname)  #Add the columns names
        return rvn_paramsList
    except Exception as e:
        print('An error occured when reading the RavenParameters.dat file.')
        print(e)

#Reads the RVP template and return the important information as a 2d list
def readRVPtemplate(rvptemplatefile):
    try:
        rvp=[]
        with open(rvptemplatefile, "r") as rvptmp:
            rvptmplines = rvptmp.readlines()
            for line in rvptmplines:
                if '#' in line: #Don't add comments
                    pass
                else:
                    rvp.append(line.split())
        rvp = [x for x in rvp if x != []]   #Removes empty lists (empty lines)
        return rvp
    except Exception as e:
        print('An error occured when reading the rvp template file.')
        print(e)
        #self.iface.messageBar().pushMessage("Error", "An error occured when reading the rvp template file. Check the python console for more details.",level=Qgis.Critical)

#Returns the default parameter value of a specific attribute by searching in the 2d list provided by readRavenParams()
def getDefaultParamValue(rvnParams,attribute):
    attribute = attribute.replace(',','')
    for row in range(len(rvnParams)):
        if attribute in rvnParams[row]:
            return rvnParams[row][4], rvnParams[row][2]
    return '0.12345', 'none'

#Writes the RVP file with the information gathered from the rvi, rvh and rvp template files
def writeAttributes(tag,rvp,rvptemplate,rvn_paramsList,rvhprofile,soil_layers):
    if tag == ':LandUseClasses':
        rvp.write(("#".ljust(10, '-')+"LANDUSE CLASSES".ljust(21,'-')+"#\n\n"))
        rvp.write(tag+"\n")
    elif tag == ':VegetationClasses':
        rvp.write(("#".ljust(10, '-')+"VEGETATION CLASSES".ljust(21,'-')+"#\n\n"))
        rvp.write(tag+"\n")
    elif tag == ':SoilProfiles':
        rvp.write(("#".ljust(10, '-')+"SOIL PROFILES".ljust(21,'-')+"#\n\n"))
        rvp.write(tag+"\n")
        rvp.write('  LAKE, 0\n  ROCK, 0')
    linecount = 0
    classattributes={}
    for line in rvptemplate:
        if tag+',' in line:
            for attribute in rvptemplate[linecount+1]:
                rvp.write(" "+attribute)
                if ':' not in attribute:
                    paramvalue,units = getDefaultParamValue(rvn_paramsList,attribute)
                    classattributes[attribute]=paramvalue
            rvp.write('\n')
            for unit in rvptemplate[linecount+2]:
                rvp.write(" "+unit.rjust(4))
            break
        linecount +=1
    for profile in rvhprofile:
        if tag ==':SoilProfiles':
            rvp.write('\n  '+profile+', '+str(soil_layers))
            for numlayer in range(soil_layers):
                layer = str(numlayer+1)
                rvp.write(', SOIL_'+layer+', 0.5')
        else:
            rvp.write('\n  '+profile+', ')
            rvp.write(", ".join(classattributes.values()))
    rvp.write("\n:End"+tag.replace(':','')+"\n\n")    

#Writes the global parameters into the RVP file
def writeGlobalParameters(rvp,rvptemplate,rvn_paramsList):
    rvp.write(("#".ljust(10, '-')+"GLOBAL PARAMETERS".ljust(21,'-')+"#\n\n"))
    firstloop = True
    classattributes={}
    for line in rvptemplate:
        if ':GlobalParameter' in line:
            paramvalue,units = getDefaultParamValue(rvn_paramsList,line[1])
            classattributes[line[1]]=paramvalue
    for key, value in classattributes.items():
        if value == None:
            value = '0.12345'
            if firstloop == True:
                print('Warning: some global parameters values were not found. Please check the rvp file.')
                firstloop = False
        rvp.write(':GlobalParameter '+ str(key)+ ' '+ str(value)+'\n')
    rvp.write('\n')

#Writes the soil, landuse, vegetation parameters
def writeParametersList(tag,rvp,rvptemplate,rvn_paramsList,rvhprofile):
    if tag == ':LandUseParameterList':
        rvp.write(("#".ljust(10, '-')+"LANDUSE PARAMETERS".ljust(21,'-')+"#\n\n"))
        rvp.write(tag+"\n")
    elif tag == ':VegetationParameterList':
        rvp.write(("#".ljust(10, '-')+"VEGETATION PARAMETERS".ljust(21,'-')+"#\n\n"))
        rvp.write(tag+"\n")
    elif tag == ':SoilParameterList':
        rvp.write(("#".ljust(10, '-')+"SOIL PARAMETERS".ljust(21,'-')+"#\n\n"))
        rvp.write(tag+"\n") 
    parameters=[]
    defaultvalues = []
    units = []
    linecount=0
    for line in rvptemplate:
        if tag in line:
            for attribute in rvptemplate[linecount+1]:
                if ':' not in attribute:
                    paramvalue,paramunits = getDefaultParamValue(rvn_paramsList,attribute)
                    parameters.append(attribute)
                    defaultvalues.append(paramvalue)
                    units.append(paramunits)
            break
        linecount+=1
    rvp.write(' :Parameters,')
    for param in parameters:
        rvp.write(' '+param)
    rvp.write('\n :Units')
    for unit in units:
        rvp.write(', '+unit)
    if tag == ':SoilParameterList':
        for layer in range(rvhprofile):
            rvp.write('\n  SOIL_'+str(layer+1))
            for value in defaultvalues:
                rvp.write(', '+value)
    else:
        for profile in rvhprofile:
            rvp.write('\n  '+profile)
            for value in defaultvalues:
                rvp.write(', '+value)
    rvp.write('\n:End'+tag.replace(':', '') + "\n\n")
