import os
import subprocess
from pathlib import Path
from qgis.core import QgsVectorLayer, QgsProject

#This method runs the command that it receives with subprocess
def dockerCommand(cmd, computerOS): 
    '''Executes the command it receives with subprocess.Popen
    
        param cmd: The command to run (string or tuple)
    ''' 
    if computerOS == 'windows':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE,startupinfo=startupinfo)
    else:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == b'':
            break
        if output:
            print(output.strip().decode("utf-8","ignore").replace('',''))  #Surely there's a better way to remove the %08 character (shows as BS in str format)
    rc = process.poll() 

#This method fully removes the container, as well as the image to free up space
def dockerdelete(self):
    '''Stops the Docker container, removes it as well as the image'''
    try:
        print("Making sure the container is stopped > docker stop qraven")
        os.system("docker stop qraven")
        print("Removing the docker container > docker rm qraven")
        os.system("docker rm qraven")
        print("Removing the image > docker rmi scriptbash/qraven")
        os.system("docker rmi scriptbash/qraven")
        os.system("docker rmi scriptbash/qraven_arm")
        print("container stopped and removed")
        self.iface.messageBar().pushSuccess("Success", "The docker container and the image were removed")
    except Exception as e:
        print("An error occured while attempting to remove the docker container and image")
        print(e)

#This method pulls the scriptbash/qraven docker container
def dockerPull(computerOS, contnrCMD):
    '''Pulls the scriptbash/qraven docker container
    
        Depends on the following method:

        dockerCommand()
    '''
    try:
        if computerOS !='macos':
            print("Trying to pull the scriptbash/qraven image...")
            cmd=contnrCMD, 'pull', 'scriptbash/qraven:latest'  
            dockerCommand(cmd, computerOS)
        else:
            print("Trying to pull the scriptbash/qraven_arm image...")
            cmd=contnrCMD, 'pull', 'scriptbash/qraven_arm:latest'  
            dockerCommand(cmd,computerOS)
        print("The pull was successfull")
    except Exception as e:
        print(e)

#This method starts the docker container
def dockerStart(computerOS,contnrCMD):
    '''Starts the docker container detached, with a pseudo-tty. The working directory is /root/BasinMaker
    
        Depends on the following method:

        dockerCommand()
    '''
    try:
        print("Attempting to start the container...")
        if computerOS != 'macos':
            cmd=contnrCMD, 'run', '-t', '-d','-w','/root/BasinMaker','--name', 'qraven', 'scriptbash/qraven'
            dockerCommand(cmd, computerOS)
        else:
            cmd=contnrCMD, 'run', '-t', '-d','-w','/root/BasinMaker','--name', 'qraven', 'scriptbash/qraven_arm'
            dockerCommand(cmd, computerOS)
        print("The container was started successfully")
    except Exception as e:
        print(e)

#This function stops the docker container and removes it
def dockerStop(contnrCMD):
    os.system(contnrCMD+" stop qraven")     #Stops the container after the process
    os.system(contnrCMD+" rm qraven")       #Deletes the container

#This method starts the create_RVH.py script
def runBasinMaker(computerOS,contnrCMD):
    '''Launches the create_RVH.py script inside the Docker container.
        Uses the bash shell in interactive mode in order to get the proper python paths and 
        environment variables set in ~/.bashrc.

        Depends on the following method:

        dockerCommand()
    '''
    print("Starting BasinMaker process, this will take a while to complete")
    pythoncmd = "python3 -u create_RVH.py"  #Bash command to start the BasinMaker script
    cmd =contnrCMD, 'exec','-t', 'qraven','/bin/bash','-i','-c',pythoncmd    #Docker command to run the script
    try:
       # os.system("docker start qraven")    #Make sure the container is started. Only needed when the plugin is run a second time
        dockerCommand(cmd, computerOS)
        print("BasinMaker has finished processing the files")  
    except Exception as e:
        print("The BasinMaker process failed...")
        print(e)

#This method copies the RVH parameters file and the user's data to the docker container
def dockerCopy(self, params, computerOS, separator,contnrCMD):
    '''Copy the RVH parameters file and the user's geospatial data to the Docker container'''
    outputdir = self.dlg.file_outputfolder.filePath()   #Get the output directory
    dockerBMpath = '/root/BasinMaker'   #The path to the BasinMaker folder inside the container 
    dockerDEMPath = dockerBMpath + '/Data/DEM'  #The path to the DEM folder inside the container
    dockerLandusePath = dockerBMpath + '/Data/landuse'  #The path to the landuse folder inside the container
    dockerLakesPath = dockerBMpath + '/Data/lakes'  #The path to the lakes folder inside the container
    dockerBankfullPath = dockerBMpath + '/Data/bkf_width'   #The path to the bkf_width folder inside the container
    dockerSoilPath = dockerBMpath + '/Data/soil'    #The path to the soil folder inside the container
    dockerPoIPath = dockerBMpath + '/Data/stations' #The path to the point of interest folder inside the container
    dockerHybasinPath = dockerBMpath + '/Data/hybasin'  #The path to the hydro basin folder inside the container
    dockerProvPolyPath = dockerBMpath + '/Data/extent_poly' #The path to the extent polygon folder inside the container
    dockerFDRPath = dockerBMpath + '/Data/flow_direction'   #The path to the flow direction folder inside the container
    
    #Dictionary of the data path provided by the user
    datapaths = {
        'dem'               : params['pathdem'],
        'landusepoly'       : params['pathlandusepoly'],
        'landuserast'       : params['pathlanduserast'],
        'lakes'             : params['pathlakes'],
        'bankfull'          : params['pathbankfull'],
        'soil'              : params['pathsoil'],
        'pointinterest'     : params['pathpointsinterest'],
        'hybasin'           : params['pathhybasin'],
        'provpoly'          : params['path_providedpoly'],
        'manning'           : params['landusemanning'],
        'flowdirection'     : params['pathfdr'],
        'landuseinfo'       : params['pathlanduseinfo'],
        'soilinfo'          : params['pathsoilinfo'],
        'veginfo'           : params['pathveginfo']

    }
    shpExt = ['cfg', 'dbf', 'prj','qmd','shp', 'shx']   #List with the shapefile extensions
    rvhScript = outputdir+separator+ "parameters.txt"   #Get the path to the exported parameters file
    cmd=contnrCMD, 'cp', rvhScript, 'qraven:'+ dockerBMpath
    dockerCommand(cmd, computerOS)
    
    #Loop through the dictionary of paths
    for key, path in datapaths.items():
        if path != '' or path != '#':   #If the path has a file provided
            filename = Path(path).stem  #Get the file name without extension and path
            folder = os.path.dirname(path)  #Get only the file path (without the file name)
            if key == 'dem':
                cmdData=contnrCMD, 'cp', params['pathdem'], 'qraven:'+ dockerDEMPath
                dockerCommand(cmdData, computerOS) #Sends the DEM to the container
            elif key == 'landusepoly':
                for extension in shpExt:
                    file = folder+separator+filename + '.' + extension
                    cmdData=contnrCMD, 'cp', file, 'qraven:'+ dockerLandusePath
                    dockerCommand(cmdData, computerOS) #Sends the complete landuse polygon shapefile to the container
            elif key == 'landuserast':
                cmdData=contnrCMD, 'cp', params['pathlanduserast'], 'qraven:'+ dockerLandusePath
                dockerCommand(cmdData, computerOS) #Sends the landuse raster to the container
            elif key == 'lakes':
                for extension in shpExt:
                    file = folder+separator+filename + '.' + extension
                    cmdData=contnrCMD, 'cp', file, 'qraven:'+ dockerLakesPath
                    dockerCommand(cmdData, computerOS) #Sends the complete lakes shapefile to the container
            elif key == 'bankfull':
                for extension in shpExt:
                    file = folder+separator+filename + '.' + extension
                    cmdData=contnrCMD, 'cp', file, 'qraven:'+ dockerBankfullPath
                    dockerCommand(cmdData, computerOS) #Sends the complete bankfull width shapefile to the container
            elif key == 'soil':
                for extension in shpExt:
                    file = folder+separator+filename + '.' + extension
                    cmdData=contnrCMD, 'cp', file, 'qraven:'+ dockerSoilPath
                    dockerCommand(cmdData, computerOS)     #Sends the complete soil shapefile to the container
            elif key == 'pointinterest':
                for extension in shpExt:
                    file = folder+separator+filename + '.' + extension
                    cmdData=contnrCMD, 'cp', file, 'qraven:'+ dockerPoIPath
                    dockerCommand(cmdData, computerOS) #Sends the complete point of interest shapefile to the container
            elif key == 'hybasin':
                for extension in shpExt:
                    file = folder+separator+filename + '.' + extension
                    cmdData=contnrCMD, 'cp', file, 'qraven:'+ dockerHybasinPath
                    dockerCommand(cmdData, computerOS) #Sends the complete hydro basin shapefile to the container
            elif key == 'provpoly':
                for extension in shpExt:
                    file = folder+separator+filename + '.' + extension
                    cmdData=contnrCMD, 'cp', file, 'qraven:'+ dockerProvPolyPath
                    dockerCommand(cmdData, computerOS) #Sends the complete extent polygon shapefile to the container
            elif key == 'manning':
                for extension in shpExt:
                    cmdData=contnrCMD, 'cp', params['landusemanning'], 'qraven:'+ dockerLandusePath
                    dockerCommand(cmdData, computerOS) #Sends the landuse manning table to the container
            elif key == 'flowdirection':
                for extension in shpExt:
                    cmdData=contnrCMD, 'cp', params['pathfdr'], 'qraven:'+ dockerFDRPath
                    dockerCommand(cmdData, computerOS)  #Sends flow direction file to the container
            elif key == 'landuseinfo':
                cmdData=contnrCMD, 'cp', params['pathlanduseinfo'], 'qraven:'+ dockerLandusePath
                dockerCommand(cmdData, computerOS)     #Sends landuse info csv file to the container
            elif key == 'soilinfo':
                cmdData=contnrCMD, 'cp', params['pathsoilinfo'], 'qraven:'+ dockerSoilPath
                dockerCommand(cmdData, computerOS) #Sends soil info csv file to the container
            elif key == 'veginfo':
                cmdData=contnrCMD, 'cp', params['pathveginfo'], 'qraven:'+ dockerLandusePath
                dockerCommand(cmdData, computerOS) #Sends vegetation csv file to the container

    print("Done copying the files to the container") 


#This method retrieves the results folder generated by BasinMaker and saves it in the user's output directory
def getDockerResults(self, computerOS, separator, contnrCMD):
    '''Grabs the OIH_Output folder from the Docker container and places it into the user's specified directory
    
        Depends on the following method:

        dockerCommand()
    '''
    outputdir = self.dlg.file_outputfolder.filePath()   #Get the output directory
    dockerBMResultsPath = '/root/BasinMaker/OIH_Output' #Get the docker path where the results are
    print("Grabbing the results, this could take a while...")
    cmd =contnrCMD, 'cp','qraven:'+dockerBMResultsPath, outputdir
    try:
        dockerCommand(cmd, computerOS)
        print("The results are now in " + outputdir) 
    except Exception as e:
        print("Failed to retrieve the results...")
        print(e)
    try:    
        hrulayer = QgsVectorLayer(outputdir+separator+"OIH_Output"+separator+"network_after_gen_hrus"+separator+"finalcat_hru_info.shp", 'finalcat_hru_info', "ogr")
        lakelayer = QgsVectorLayer(outputdir+separator+"OIH_Output"+separator+"network_after_gen_hrus"+separator+"finalcat_hru_lake_info.shp", 'finalcat_hru_lake_info', "ogr")
        QgsProject.instance().addMapLayer(hrulayer)  #Adds the HRU layer to the QGIS map
        QgsProject.instance().addMapLayer(lakelayer) #Add the HRU lakes layer to the QGIS map           
    except Exception as e:
        print("Failed to load the results shapefile...")
        print(e)
    self.iface.messageBar().pushInfo("Info", "The BasinMaker process has finished. Check the python logs for more details.")