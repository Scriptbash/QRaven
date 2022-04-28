# QRaven
A QGIS Plugin to help generate input files for Raven

## Description

QRaven aims to simplify the creation of the primary input file (.RVI) and HRU/Basin definition file (.RVH) for the Raven hydrological modelling framework. It allows the user to choose all the options for the RVI file (except for the hydrological processes at the moment) and it automates the setup, as well as the use of the BasinMaker python library.

## Getting Started

### Dependencies

* QGIS (3.20 and above) must be installed. Prior versions may not work with the plugin
* To use the BasinMaker options, Docker must be installed on your computer and properly configured. Linux users must make sure to follow the post-installation steps provided by Docker
* QRaven works on Linux and should work on Windows and Mac as well

### Installing

* Go to the releases page and download the .zip file : https://github.com/Scriptbash/QRaven/releases
* Open QGIS, go to "Plugins", click on "Manage and Install plugins". Finally, click on the "Install from ZIP" menu, select the downloaded .zip file and click on "Install"

### How to use QRaven

* Click on the QRaven icon in your toolbar ![image](https://user-images.githubusercontent.com/98601298/162262632-ead9b9aa-2034-4e5b-bba2-859040995ed5.png) or go in the "Plugins" menu, select the QRaven option and click on "Generate Raven input files"
* You will have three main tabs
  * Raven RVI
  * BasinMaker RVH 
  * Run Model 

* Raven RVI tab
  * Use this tab to create the RVI file. The plugin __does not__ validate the inputs, meaning that the RVI file generated may not work in Raven if the configuration made is invalid
  * Select and enter all the information to add inside the RVI file. Once done, click on the "Write" button to generate the RVI file. Make sure to have selected a valid directory inside the "Output Directory" field and that your user has write permissions to it
  * Screenshots
    *  ![image](https://user-images.githubusercontent.com/98601298/162264611-48160e69-9435-49f0-ae0f-5b6d912644d5.png)
    *  ![image](https://user-images.githubusercontent.com/98601298/162264955-e076fcb2-9c10-4fd6-981e-1472dcf7ae60.png)
* BasinMaker RVH tab
  * Use this tab to launch BasinMaker and generate the RVH files
  * This section needs to be tested on Windows and MacOS
  * Like the RVI file, select the parameters values and select the files to process
  * When a file is added, more parameters fields unlock and will need to be filled
  * At the end of the process, the shapefile results are added to the QGIS canvas and the results folder is copied in the output directory chosen
  * Screenshots
    * ![image](https://user-images.githubusercontent.com/98601298/163680321-47b75579-3d5e-4506-bed7-8e2a31c87d50.png)
    * ![image](https://user-images.githubusercontent.com/98601298/163680334-43064748-5298-43ee-ad34-79b827ea8998.png)
    * ![image](https://user-images.githubusercontent.com/98601298/163680338-aed31db0-2bd6-4903-9385-7f424d4b410b.png)
* Run Model tab
  * Use this tab to run your Raven model
  * A Raven executable must be provided as well as an input and output directory
  * The file name prefix is the name as the model
  * The RunName is only required if the command :RunName is used in the .rvi file
  * Once the Raven has finished processing the model, the hydrograph can be visualized by clicking on the Gather Output button
  * Screenshots
    * ![image](https://user-images.githubusercontent.com/98601298/165858419-1748cd2f-bab9-4f26-82d5-033f11105c06.png)
    * ![image](https://user-images.githubusercontent.com/98601298/165858439-f31f9959-d3c6-48b0-8b29-a79fada5720b.png)

## Help

If you run into any issue, have a question or feedback while using QRaven, please open an issue here : https://github.com/Scriptbash/QRaven/issues
