import os
import subprocess
from pathlib import Path
from qgis.core import QgsVectorLayer, QgsProject
from PyQt5.QtWidgets import *

class Docker:
    def __init__(self,computerOS,separator,containerization,registry,image):
        self.computerOS = computerOS
        self.separator = separator
        self.containerization = containerization.lower()
        self.registry = registry
        self.image = image

        if self.containerization == 'docker':
            if self.computerOS == 'macos':
                os.environ["PATH"] = "/Applications/Docker.app/Contents/Resources/bin" #This is needed for docker to work on MacOS
            elif self.computerOS == 'windows':
                os.environ["PATH"] = "C:\\Program Files\\Docker\\Docker\\resources\\bin"    #This is needed so that the docker commands work on Windows
        elif self.containerization == 'podman':
            if self.computerOS == 'macos':
                os.environ["PATH"] = "/opt/podman/bin"
            elif self.computerOS == 'windows':
                os.environ["PATH"] = "C:\\Program Files\\RedHat\\Podman"

    def runCommand(self, cmd):
        '''Executes the command it receives with subprocess.Popen
            
           param cmd: The command to run (string or tuple)
        ''' 
        if self.computerOS == 'windows':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE,startupinfo=startupinfo)
        else:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        #QApplication.processEvents() #Unfreezes the GUI, but slows down the process heavily
        while True:
            output = process.stdout.readline()
            if output == b'':
                break
            if output:
                print(output.strip().decode("utf-8","ignore").replace('',''))  #Surely there's a better way to remove the %08 character (shows as BS in str format)
        rc = process.poll()

        return rc

    def pull(self):
        '''Pulls the scriptbash/qraven docker container
        
            Depends on the following method:

            runCommand()
        '''
        try:
            print("Attempting to pull the "+self.image+" image...")
            cmd=self.containerization, 'pull', self.registry+'/'+self.image  
            rc =self.runCommand(cmd)
            if rc == 0:
                print('Image pull - Success.')
            else:
                print('Image pull - Failed.')
        except Exception as e:
            print(e)

    def stop(self):
        '''Stops and removes the container'''
        print("Stopping the container...")
        cmd = self.containerization, 'stop', 'qraven'   #Stops the container
        rc=self.runCommand(cmd)
        print("Removing the container...")
        cmd = self.containerization, 'rm', 'qraven' #Deletes the container
        rc=self.runCommand(cmd)
        print("Done.")
    
    def delete(self):
        '''Stops the Docker container, removes it as well as the image'''
        try:
            self.stop()
            print("Removing the image...")
            cmd = self.containerization, 'rmi', self.registry+'/'+self.image
            rc=self.runCommand(cmd)
            print("Done.")   
        except Exception as e:
            print("An error occured while attempting to remove the docker container and image")
            print(e)
    
    def start(self, workingdir, volume1, volume2):
        '''Starts the docker container detached, with a pseudo-tty. The working directory is /root/BasinMaker
        
            Depends on the following method:

            runCommand()
        '''
        try:
            if volume1 == None and volume2 == None:
                print('Skipping volume mounting...')
                cmd=self.containerization, 'run', '-t', '-d', '-w', workingdir, '--name', 'qraven', self.registry+'/'+self.image
            elif volume1 != None and volume2 == None:
                print('Running container with a volume...')
                cmd=self.containerization, 'run', '-t', '-d', '-w', workingdir, '-v', volume1, '--name', 'qraven', self.registry+'/'+self.image
            else:
                print('Running container with volumes...')
                cmd=self.containerization, 'run', '-t', '-d', '-w', workingdir, '-v', volume1, '-v', volume2, '--name', 'qraven', self.registry+'/'+self.image
            rc=self.runCommand(cmd)
            if rc == 0:
                print('Container start - Success.')
            else:
                print("Container start - Failed.")
        except Exception as e:
            print(e)

    def runBasinMaker(self):
        '''Launches the create_RVH.py script inside the Docker container.
            Uses the bash shell in interactive mode in order to get the proper python paths and 
            environment variables set in ~/.bashrc.

            Depends on the following method:

            runCommand()
        '''
        print("Starting BasinMaker process, this will take a while to complete")
        pythoncmd = "python3 -u create_RVH.py"  #Bash command to start the BasinMaker script
        cmd =self.containerization, 'exec', '-t', 'qraven', '/bin/bash', '-i', '-c', pythoncmd    #Docker command to run the script
        try:
            rc = self.runCommand(cmd)
            if rc == 0:
                print('BasinMaker process - Success.')
            else:
                print("BasinMaker process - Failed.")  
        except Exception as e:
            print("The BasinMaker process failed for the following reason:")
            print(e)
    
    def bmCopy(self, params, outputdir):
        '''Copy the RVH parameters file and the user's geospatial data to the Docker container'''
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
        rvhScript = outputdir + self.separator + "parameters.txt"   #Get the path to the exported parameters file
        cmd=self.containerization, 'cp', rvhScript, 'qraven:'+ dockerBMpath+'/parameters.txt'
        rc = self.runCommand(cmd)
        if rc == 0:
            print('Send parameters file to container - Success.')
        else:
            print("Send parameters file to container - Failed.") 
        
        #Loop through the dictionary of paths
        for key, path in datapaths.items():
            if path != '' or path != '#':   #If the path has a file provided
                filename = Path(path).stem  #Get the file name without extension and path
                folder = os.path.dirname(path)  #Get only the file path (without the file name)
                if key == 'dem':
                    cmdData=self.containerization, 'cp', params['pathdem'], 'qraven:'+ dockerDEMPath
                    self.runCommand(cmdData) #Sends the DEM to the container
                elif key == 'landusepoly':
                    for extension in shpExt:
                        file = folder+self.separator+filename + '.' + extension
                        cmdData=self.containerization, 'cp', file, 'qraven:'+ dockerLandusePath
                        self.runCommand(cmdData) #Sends the complete landuse polygon shapefile to the container
                elif key == 'landuserast':
                    cmdData=self.containerization, 'cp', params['pathlanduserast'], 'qraven:'+ dockerLandusePath
                    self.runCommand(cmdData) #Sends the landuse raster to the container
                elif key == 'lakes':
                    for extension in shpExt:
                        file = folder+self.separator+filename + '.' + extension
                        cmdData=self.containerization, 'cp', file, 'qraven:'+ dockerLakesPath
                        self.runCommand(cmdData) #Sends the complete lakes shapefile to the container
                elif key == 'bankfull':
                    for extension in shpExt:
                        file = folder+self.separator+filename + '.' + extension
                        cmdData=self.containerization, 'cp', file, 'qraven:'+ dockerBankfullPath
                        self.runCommand(cmdData) #Sends the complete bankfull width shapefile to the container
                elif key == 'soil':
                    for extension in shpExt:
                        file = folder+self.separator+filename + '.' + extension
                        cmdData=self.containerization, 'cp', file, 'qraven:'+ dockerSoilPath
                        self.runCommand(cmdData)     #Sends the complete soil shapefile to the container
                elif key == 'pointinterest':
                    for extension in shpExt:
                        file = folder+self.separator+filename + '.' + extension
                        cmdData=self.containerization, 'cp', file, 'qraven:'+ dockerPoIPath
                        self.runCommand(cmdData) #Sends the complete point of interest shapefile to the container
                elif key == 'hybasin':
                    for extension in shpExt:
                        file = folder+self.separator+filename + '.' + extension
                        cmdData=self.containerization, 'cp', file, 'qraven:'+ dockerHybasinPath
                        self.runCommand(cmdData) #Sends the complete hydro basin shapefile to the container
                elif key == 'provpoly':
                    for extension in shpExt:
                        file = folder+self.separator+filename + '.' + extension
                        cmdData=self.containerization, 'cp', file, 'qraven:'+ dockerProvPolyPath
                        self.runCommand(cmdData) #Sends the complete extent polygon shapefile to the container
                elif key == 'manning':
                    for extension in shpExt:
                        cmdData=self.containerization, 'cp', params['landusemanning'], 'qraven:'+ dockerLandusePath
                        self.runCommand(cmdData) #Sends the landuse manning table to the container
                elif key == 'flowdirection':
                    for extension in shpExt:
                        cmdData=self.containerization, 'cp', params['pathfdr'], 'qraven:'+ dockerFDRPath
                        self.runCommand(cmdData)  #Sends flow direction file to the container
                elif key == 'landuseinfo':
                    cmdData=self.containerization, 'cp', params['pathlanduseinfo'], 'qraven:'+ dockerLandusePath
                    self.runCommand(cmdData)     #Sends landuse info csv file to the container
                elif key == 'soilinfo':
                    cmdData=self.containerization, 'cp', params['pathsoilinfo'], 'qraven:'+ dockerSoilPath
                    self.runCommand(cmdData) #Sends soil info csv file to the container
                elif key == 'veginfo':
                    cmdData=self.containerization, 'cp', params['pathveginfo'], 'qraven:'+ dockerLandusePath
                    self.runCommand(cmdData) #Sends vegetation csv file to the container
            

    def getBasinMakerResults(self, outputdir):
        '''Grabs the OIH_Output folder from the Docker container and places it into the user's specified directory
        
            Depends on the following method:

            dockerCommand()
        '''
        dockerBMResultsPath = '/root/BasinMaker/OIH_Output' #Get the docker path where the results are
        print("Grabbing the results, this could take a while...")
        cmd =self.containerization, 'cp','qraven:'+dockerBMResultsPath, outputdir
        try:
            rc = self.runCommand(cmd)
            if rc == 0:
                print('Grab BasinMaker results - Success.')
                print("The results are now in " + outputdir)
            else:
                print("Grab BasinMaker results - Failed.")  
        except Exception as e:
            print("Couldn't retrieve the results because of the following reason:")
            print(e)
        try:    
            hrulayer = QgsVectorLayer(outputdir+self.separator+"OIH_Output"+self.separator+"network_after_gen_hrus"+self.separator+"finalcat_hru_info.shp", 'finalcat_hru_info', "ogr")
            lakelayer = QgsVectorLayer(outputdir+self.separator+"OIH_Output"+self.separator+"network_after_gen_hrus"+self.separator+"finalcat_hru_lake_info.shp", 'finalcat_hru_lake_info', "ogr")
            if len(hrulayer):
                QgsProject.instance().addMapLayer(hrulayer)  #Adds the HRU layer to the QGIS map
            if len(lakelayer):
                QgsProject.instance().addMapLayer(lakelayer) #Add the HRU lakes layer to the QGIS map 
            print("Load results shapefile - Success.")
        except Exception as e:
            print("Load results shapefile - Failed.")
            #print(e)
    
    def runGridWeights(self, pythoncmd):
        '''Launches the GridWeights.py script inside the Docker container.
            Uses the bash shell in interactive mode in order to get the proper python paths and 
            environment variables set in ~/.bashrc.

            Depends on the following method:

            runCommand()
        '''
        print("Starting GridWeights script, this will take a while to complete...")
        cmd =self.containerization, 'exec','-t', 'qraven','/bin/bash','-i','-c',pythoncmd    #Docker command to run the script
        
        try:
            rc = self.runCommand(cmd)
            if rc == 0:
                print('Start GridWeights process - Success')
            else:
                print("Start Gridweights process - Failed.")    
        except Exception as e:
            print("The GridWeights process failed because of the following reason: ")
            print(e)

    def getGridWeightsResults(self, outputfile, outputfolder):
        cmd = self.containerization, 'cp', 'qraven:/root/Gridweights/'+outputfile, outputfolder + '/'
        try:
            rc = self.runCommand(cmd)
            if rc == 0:
                print('Grab GridWeights results - Success.')
                print("Results are now in "+ outputfolder) 
            else:
                print("Grab GridWeights results - Failed.") 
        except Exception as e:
            print("Couldn't grab results because of the following reason:")
            print(e)

    def run_raven(self, prefix, run_name):
        raven_cmd = 'Raven.exe ' + '~/Raven/model/' + prefix + ' -o output -r '+ run_name
        cmd = self.containerization, 'exec', '-t', 'qraven', '/bin/bash', '-i', '-c', raven_cmd

        try:
            rc = self.runCommand(cmd)
            if rc == 0:
                print('Run Raven - Success.')
            else:
                print("Run Raven - Failed.")
        except Exception as e:
            print("Couldn't run Raven because of the following reason:")
            print(e)
    
    def get_raven_results(self, output_dir):
        cmd = self.containerization, 'cp', 'qraven:/root/Raven/output/.', output_dir
        try:
            rc = self.runCommand(cmd)
            if rc == 0:
                print('Grab Raven results - Success.')
                print("Results are now in " + output_dir)
            else:
                print("Grab Raven results - Failed.") 
        except Exception as e:
            print("Couldn't grab results because of the following reason:")
            print(e)

    def run_ostrich(self):
        cmd = self.containerization, 'exec', '-t', 'qraven', '/bin/bash', '-i', '-c', 'OstrichMPI'
        try:
            rc = self.runCommand(cmd)
            if rc == 0:
                print('Run OSTRICH - Success.')
            else:
                print("Run OSTRICH - Failed.")
        except Exception as e:
            print("Couldn't run OSTRICH because of the following reason:")
            print(e)
