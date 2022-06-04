# QRaven
A QGIS Plugin to help generate input files for Raven

## Description

QRaven aims to simplify the creation of the primary input file (.RVI) and HRU/Basin definition file (.RVH) for the Raven hydrological modelling framework. It allows the user to choose all the options for the RVI file and it automates the setup, as well as the use of the BasinMaker python library. It can run a model, draw the hydrograph and open RavenView using the default web browser.

## Getting Started

### Dependencies

* QGIS (3.20 and above) must be installed. Prior versions may not work with the plugin
  * https://qgis.org/en/site/forusers/download.html  
* To use the BasinMaker options, Docker must be installed on your computer and properly configured. Linux users must make sure to follow the post-installation steps provided by Docker
  * https://docs.docker.com/get-docker/ 
* QRaven works on Linux and Windows. It should work on Mac as well, but testing must be done

### Installing

* Go to the releases page and download the .zip file : https://github.com/Scriptbash/QRaven/releases
* Open QGIS, go to "Plugins", click on "Manage and Install plugins"

![image](https://user-images.githubusercontent.com/98601298/170998843-1fa7c283-e15b-4dce-a684-59e16a5c71d4.png)
* Finally, click on the "Install from ZIP" menu, select the downloaded .zip file and click on "Install"

![image](https://user-images.githubusercontent.com/98601298/170999288-1d8db5dc-5709-4139-8aff-412dc76eb1c2.png)

### How to use QRaven

* Click on the QRaven icon in your toolbar ![image](https://user-images.githubusercontent.com/98601298/162262632-ead9b9aa-2034-4e5b-bba2-859040995ed5.png) or go in the "Plugins" menu, select the QRaven option and click on "Generate Raven input files"

![image](https://user-images.githubusercontent.com/98601298/170999781-22514c96-7611-424a-b946-69fd465c5181.png)

* You will have three main tabs
  * Raven RVI
  * BasinMaker RVH 
  * Run Model 

* Raven RVI tab
  * Use this tab to create the RVI file. The plugin __does not__ validate the inputs, meaning that the RVI file generated may not work in Raven if the configuration made is invalid
  * Select and enter all the information to add inside the RVI file. Once done, click on the "Write" button to generate the RVI file. Make sure to have selected a valid directory inside the "Output Directory" field and that your user has write permissions to it
  * Screenshots
    
    ![image](https://user-images.githubusercontent.com/98601298/169550474-769171a0-3cf6-4678-8737-411dbbc7c2f9.png)
    
    ![image](https://user-images.githubusercontent.com/98601298/172007387-fea593d4-266c-4247-914e-3061560d9d89.png)
    
    ![image](https://user-images.githubusercontent.com/98601298/172006990-0cd05ac1-dc93-493f-9eba-2373130e65a2.png)
* BasinMaker RVH tab
  * Use this tab to launch BasinMaker and generate the RVH files
  * This section was tested on Linux and Windows, but needs to be tested MacOS
  * Like the RVI file, select the parameters values and select the files to process
  * When a file is added, more parameters fields unlock and will need to be filled
  * At the end of the process, the shapefile results are added to the QGIS canvas and the results folder is copied in the output directory chosen
  * Screenshots
    
    ![image](https://user-images.githubusercontent.com/98601298/163680321-47b75579-3d5e-4506-bed7-8e2a31c87d50.png)
    
    ![image](https://user-images.githubusercontent.com/98601298/169554028-a5a38f52-985e-4709-a4bf-4782dfd9e8a3.png)
    
    ![image](https://user-images.githubusercontent.com/98601298/163680338-aed31db0-2bd6-4903-9385-7f424d4b410b.png)
* Run Model tab
  * Use this tab to run your Raven model. This section basically attempts to mimic the RavenViewLite4 Excel file
  * A Raven executable must be provided as well as an input and output directory
  * The file name prefix is the same name as the model
  * The RunName is only required if the command :RunName is used in the .rvi file
  * Once Raven has finished processing the model, the hydrograph can be viewed by clicking on the "Draw hydrograph" button
  * By clicking on the RavenView button, RavenView will open a new tab in the user's default web browser
  * Screenshots
    
    ![image](https://user-images.githubusercontent.com/98601298/171002436-09b8b4b9-6732-4ceb-9dec-fc41bee594df.png)

    ![image](https://user-images.githubusercontent.com/98601298/169554447-858c4eb4-d79b-4839-8157-4ce727931d1f.png)

## Help

If you run into any issue, have a question or feedback while using QRaven, please open an issue here : https://github.com/Scriptbash/QRaven/issues
