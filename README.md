# QRaven
A QGIS Plugin to help generate input files for Raven

## Description

QRaven aims to simplify the creation of the input files for the Raven hydrological modelling framework. It allows the user to choose all the options for the primary input file (.rvi) and it automates the setup, as well as the use of the BasinMaker python library for the HRU/Basin definition file (.rvh). It can run models, draw hydrographs and open RavenView using the default web browser. QRaven can also automatically fill the classed parameter input file (.rvp) using default values and it can generate grid weights blocks using the GridWeightGenerator script.

## Getting Started

### Dependencies

* QGIS (3.20 and above) must be installed. Prior versions may not work with the plugin
  * https://qgis.org/en/site/forusers/download.html  
* To use the BasinMaker options and the GridWeights generator, Docker must be installed on your computer and be properly configured. Also make sure that the Docker daemon is running before running BasinMaker or the GridWeights generator. Linux users must make sure to follow the post-installation steps provided by Docker, more specifically the "Manage Docker as a non-root user" steps.
  * https://docs.docker.com/get-docker/ 
  * https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user
* QRaven works on Linux and Windows. It currently works partially on MacOS, only BasinMaker and the GridWeightsGenerator script do not work at the moment. Make sure to read the extra steps for MacOS if you are planning on running models with QRaven.


### Installing

* Go to the releases page and download the .zip file (qraven.zip) : https://github.com/Scriptbash/QRaven/releases
* Open QGIS, go to "Plugins", click on "Manage and Install plugins"

![image](https://user-images.githubusercontent.com/98601298/170998843-1fa7c283-e15b-4dce-a684-59e16a5c71d4.png)
* Finally, click on the "Install from ZIP" menu, select the downloaded .zip file and click on "Install"

![image](https://user-images.githubusercontent.com/98601298/170999288-1d8db5dc-5709-4139-8aff-412dc76eb1c2.png)

* The plugin also searches for an available update on startup. If it finds one, it will let you know and you will need to follow the same steps as the installation. The message will show at the bottom of the plugin.
  ![image](https://user-images.githubusercontent.com/98601298/188141266-755cd342-9105-4143-b93a-4a12c77b3cb7.png)


### MacOS extra steps
If you want to run a model within QRaven, you will need to give the proper permissions to the raven executable and allow it to run. 
First, to give the proper permissions, Open a __Terminal__ and use the cd command to get inside the directory that contains the executable. If your path has spaces, surround it with quotes like the example below.

Example:  cd /Downloads/'Raven Directory'

You can then use the command: sudo chmod 755 name_of_executable.exe

Where "name_of_executable is the name of the raven executable

Try to run the executable by typing: ./RavenExecutableMacOS_v3.5.exe
*You will need to use the proper file name after the ./

You should receive a popup saying it cannot be opened because the developper cannot be verified. Click on cancel to close the popup. Then open the "Security & Privacy" settings in the system preferences. Click on the lock, authenticate and then click on "Allow anyway".

Try to run the executable again with ./RavenExecutableMacOS_v3.5.exe. There should be the final popup. Click on Open and Raven should now be able to run properly.

### How to use QRaven

* Click on the QRaven icon in your toolbar ![image](https://user-images.githubusercontent.com/98601298/162262632-ead9b9aa-2034-4e5b-bba2-859040995ed5.png) or go in the "Plugins" menu, select the QRaven option and click on "Generate Raven input files"

![image](https://user-images.githubusercontent.com/98601298/170999781-22514c96-7611-424a-b946-69fd465c5181.png)

* You will have four main tabs
  * Raven RVI
  * BasinMaker RVH 
  * GridWeights
  * Run Model 

* Raven RVI tab
  * Use this tab to create the RVI file. The plugin __does not__ validate the inputs, meaning that the RVI file generated may not work in Raven if the configuration made is invalid
  * Select and enter all the information to add inside the RVI file. Once done, click on the "Write" button to generate the RVI file. Make sure you have selected a valid directory inside the "Output Directory" field and that your user has write permissions to it
  * Templates are also now available. Simply click on the desired template and its options will be automatically filled in the GUI, allowing you to easily customize it. If you would like a template to be added, please submit your request in the github issues
  * Screenshots
    
    ![image](https://user-images.githubusercontent.com/98601298/188142999-bcdffa91-2255-4d6e-95c2-55804f944ded.png)
    
    ![image](https://user-images.githubusercontent.com/98601298/188143330-3da0c874-7c28-4f31-82b0-0ddf90f8e628.png)

    ![image](https://user-images.githubusercontent.com/98601298/188143641-2e264563-eb8d-4972-ad5c-9c8e37d3c3cf.png)
    
   * Example of output file generated: 
    ![image](https://user-images.githubusercontent.com/98601298/188145605-b6ad2280-3383-4ae9-a889-1d6993de5eb6.png)

    
* BasinMaker RVH tab
  * Use this tab to launch BasinMaker and generate the RVH files
  * Like the RVI file, select the parameters values and select the files to process
  * When a file is added, more parameters fields unlock and will need to be filled
  * At the end of the process, the shapefile results are added to the QGIS canvas and the results folder is copied in the output directory chosen
  * Screenshots
    
    ![image](https://user-images.githubusercontent.com/98601298/188148617-439381da-ea4e-4ef9-9b1f-0ab51d926eda.png)
    
    ![image](https://user-images.githubusercontent.com/98601298/188148882-aaa4dfcc-b249-4a50-b823-062b60edc037.png)
    
    ![image](https://user-images.githubusercontent.com/98601298/188149131-8b1825b3-966b-4624-9d71-0e8b5457a825.png)

    
* GridWeights tab
  * Use this tab to generate the grid weights for your NetCDF input data
  * Simply specify the NetCDF file to process, its dimensions and variables
  * The HRUs file is the BasinMaker final output
  * Screenshots
  ![image](https://user-images.githubusercontent.com/98601298/188149605-f67b527a-4069-4a51-9830-4290c79fd0b8.png)


* Run Model tab
  * Use this tab to run your Raven model. This section basically attempts to mimic the RavenViewLite4 Excel file
  * A Raven executable must be provided as well as an input and output directory
  * The file name prefix is the same name as the model, but it should fill itself automatically after selecting an input folder
  * The RunName is only required if the command :RunName is used in the .rvi file. It should be added automatically after selecting an input folder
  * Once Raven has finished processing the model, the hydrograph can be viewed by clicking on the "Draw hydrograph" button
  * By clicking on the RavenView button, RavenView will open in a new tab in the user's default web browser
  * If the :CreateRVPTemplate command was used in the .rvi file before processing the model, the Auto fill rvp template button can be used to automatically generate a .rvp file with default values
  * Screenshots
    
    ![image](https://user-images.githubusercontent.com/98601298/188149995-0dbed886-7906-412a-b798-09bae286959e.png)

    ![image](https://user-images.githubusercontent.com/98601298/188150121-ff889b56-5aa3-4e17-9d7f-28848896932d.png)

## Credits
* The BasinMaker tools used in the plugins are developped by Ming and its official website can be found at : http://hydrology.uwaterloo.ca/basinmaker/
* The GridWeights Generator is made by Julie and the script can be found at : https://github.com/julemai/GridWeightsGenerator 
* The Auto fill rvp template feature is heavily based on RavenR's rvn_rvp_fill_template function by Robert Chlumsky : https://github.com/rchlumsk/RavenR/blob/master/R/rvn_rvp_fill_template.R

## Help

If you run into any issue, have a question or feedback while using QRaven, please open an issue here : https://github.com/Scriptbash/QRaven/issues
