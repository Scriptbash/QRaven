=================================
Create a Raven model step by step
=================================

This tutorial will explain how to build a Raven model from scratch using QRaven.
The HBV-EC template will be used to model the watershed of Dumoine River.

Get the required data
=====================

The data needed can be separated for two uses ; for Raven (Temperature, precipitations, streamflow, etc.) and 
for BasinMaker (Landuse polygons, rivers network, DEM, etc.).

Data for Raven
--------------

Streamflow
^^^^^^^^^^
Downloading streamflow data for Canada is quite easy in QRaven. 

1. Click on the Streamflow menu.
2. Since the watershed is in the province of Quebec, we will use the CEHQ data scraper. Make sure the CEHQ tab is active.
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
    The streamflow will already be transformed into a .rvt file. We will only need to edit the basin/hru ID later.
    You will also notice some information about the station has been added below the download button. Each time you download data from a station, its information will be added there.

9. Click on "Create layer". This will generate a points layer to be used with BasinMaker.
    .. image:: ./images/tutorial/create_points_layer.png
        :width: 600

Precipitations and Temperature
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* To-do

Data for BasinMaker
-------------------
Data needed to run BasinMaker can be fetch automatically by QRaven (Canada only for now).

1. Download and extract the shapefile of the Dumoine river here: `https://github.com/Scriptbash/QRaven/raw/main/bv_dumoine.zip <https://github.com/Scriptbash/QRaven/raw/main/bv_dumoine.zip>`_
2. Click on the GIS menu
3. Select a path where to save the files. Do this for all of the Data.
4. Click on "Download". This could take a while for some of the data.
    .. image:: ./images/tutorial/download_gis_data.png
            :width: 600
5. Once the download is finished, check the "Use the same paths as above" checkbox. This tell QRaven where the files to process are.
6. In the "Clip layer" field, select the watershed's polygon shapefile.
7. Click on "Process"
    .. image:: ./images/tutorial/gis_data_process.png
            :width: 600
8. The results will be saved inside each data folder and inside a folder named "Results".
