=================================
Create a Raven model step by step
=================================

This tutorial will explain how to build a Raven model from scratch using QRaven.
The HBV-EC template will be used to model the watershed of Dumoine river.

Get the required data
=====================

The data needed can be separated for two uses;

1. for Raven (Temperature, precipitations, streamflow, etc.)
2. for BasinMaker (Landuse polygons, rivers network, DEM, etc.)

Data for Raven
--------------

Streamflow
^^^^^^^^^^
Downloading streamflow data for Canada is quite easy in QRaven. 

1. Click on the Streamflow menu.
2. Since the watershed is in the province of Quebec, we will use the DPPHC data scraper. Make sure the DPPHC tab is active.
3. Search for "Dumoine,Rivière" in the "River or lake" field.
4. Click on the "Search button".
    
    .. image:: ./images/tutorial/search_stream_station.png
        :width: 600

5. Next, copy the station ID of the only operational station.
6. Paste the ID into the "Station ID" field
7. Click on fetch date range. This will set the start date and end date widgets with the first and last date of observation data available.
8. By clicking on fetch date range, the download button will be made available. Select a path where to save the data and click on Download.
    
    .. image:: ./images/tutorial/fetch_daterange.png
        :width: 600

.. note:: 
    The streamflow will already be transformed into a .rvt file. We will only need to edit the basin/HRU ID later.
    You will also notice some information about the station has been added below the download button. Each time you download data from a station, its information will be added there.

9. Click on "Create layer". This will generate a points layer to be used with BasinMaker.
    
    .. image:: ./images/tutorial/create_points_layer.png
        :width: 600

Precipitations and Temperature
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
For this tutorial we will only use data coming from the Daymet services. To do so, we will use the Daymet component of QRaven.

1. Download and extract the shapefile of the Dumoine river here: `https://github.com/Scriptbash/QRaven/raw/main/bv_dumoine.zip <https://github.com/Scriptbash/QRaven/raw/main/bv_dumoine.zip>`_
2. Click on the Daymet menu.
3. Select an output folder where the files will be saved.
4. In the "Input polygon" field, select the extracted shapefile from step 1.
5. Set the start date to 2010-01-01 and the end date to 2020-12-31.
6. In the variable list, select "tmin", "tmax" and "prcp".
7. Leave both the "Insert missing dates" and "Merge downloaded files" checkboxes checked. Since Daymet strips december 31st from the NetCDF files during leap years to include february 29, this will automatically fix the problem for us.
8. Click on the "Download" button and wait for the process to finish. It could take quite a while to finish.

    .. image:: ./images/tutorial/get_daymet_data.png
            :width: 600

Data for BasinMaker
-------------------
Data needed to run BasinMaker can be fetch automatically by QRaven (Canada only for now).

1. Click on the GIS menu
2. Select a path where to save the files. Do this for all of the Data.
3. Click on "Download". This could take a while depending on the files being downloaded.
    
    .. image:: ./images/tutorial/download_gis_data.png
            :width: 600

4. Once the download is finished, check the "Use the same paths as above" checkbox. This tells QRaven where the files to process are.
5. In the "Clip layer" field, select the watershed's polygon shapefile.
7. Click on "Process"
    
    .. image:: ./images/tutorial/gis_data_process.png
            :width: 600

8. The results will be saved inside each data folder and inside a folder named "Results".

Setup the Raven files
=====================
Now that we have all the required data and some model files, we can start setting up the Raven model files.

Generate a .rvi file
--------------------
1. Click on the "Raven RVI" menu.
2. Make sure the selected tab is "Model info".
3. Click on the "HBV-EC" template button. This will load a basic template with the HBV-EC structure.
4. Select an output directory where the generated .rvi file will be saved.
5. In the model name, type "Dumoine".
6. Set the simulation start date to 2010-01-01 and the end date to 2020-12-31. Leave the hours to 0:00:00.
7. Set the "TimeStep" to 1 hour.

    .. image:: ./images/tutorial/rvi_model_info.png
            :width: 600

8. Next, click on the "Optional I/O" tab
9. Check the "CreateRVPTemplate" checkbox. This will allow us to generate an .rvp file with the required parameters for HBV-EC when we will first run the model.
10. While we are in the "Optional I/O", we will select a few evaluation metrics. Let's select Nash-Sutcliffe.

    .. image:: ./images/tutorial/rvi_optional_io.png
            :width: 600

11. Click on the "Custom output" tab.
12. Click on the "Add output" button to add a new row
13. Select the proper options to get a custom output that will be "DAILY AVERAGE SNOW BY_HRU"
14. Generate to .rvi file by clicking on the "Write" button.


Run BasinMaker to create a .rvh file
------------------------------------
to-do

Run the raven model
===================
to-do

Calibration with OSTRICH
========================
to-do