import os
import subprocess

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
    print("module yup")
    try:
        print("Making sure the container is stopped > docker stop qraven")
        os.system("docker stop qraven")
        print("Removing the docker container > docker rm qraven")
        os.system("docker rm qraven")
        print("Removing the image > docker rmi scriptbash/qraven")
        os.system("docker rmi scriptbash/qraven")
        print("container stopped and removed")
        self.iface.messageBar().pushSuccess("Success", "The docker container and the image were removed")
    except Exception as e:
        print("An error occured while attempting to remove the docker container and image")
        print(e)

#This method pulls the scriptbash/qraven docker container
def dockerPull(computerOS):
    '''Pulls the scriptbash/qraven docker container
    
        Depends on the following method:

        dockerCommand()
    '''
    try:
        if computerOS !='macos':
            print("Trying to pull the scriptbash/qraven image...")
            cmd='docker', 'pull', 'scriptbash/qraven:latest'  
            dockerCommand(cmd, computerOS)
        else:
            print("Trying to pull the scriptbash/qraven_arm image...")
            cmd='docker', 'pull', 'scriptbash/qraven_arm:latest'  
            dockerCommand(cmd,computerOS)
        print("The pull was successfull")
    except Exception as e:
        print(e)