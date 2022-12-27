How to use QRaven
=================

.. _Usage:


Open QRaven
-----------
.. |qrvn_ico| image:: https://github.com/Scriptbash/QRaven/blob/main/qraven/icon.png?raw=true
  :width: 20

Click on the QRaven icon in your toolbar |qrvn_ico| or go in the "Plugins" menu, select the QRaven option and click on "Generate Raven input files"

.. image:: https://user-images.githubusercontent.com/98601298/170999781-22514c96-7611-424a-b946-69fd465c5181.png
  :width: 600

You will have four main tabs

 * :ref:`Raven RVI<createRVI>`
 * :ref:`BasinMaker RVH<createRVH>`
 * :ref:`GridWeights<gridweights>`
 * :ref:`Run Model<runrvn>`

.. _createRVI:

Create a RVI file
-----------------
*To-do

.. _createRVH:

Create a RVH file
-----------------
*To-do

.. _gridweights:

Associate a NetCDF grid to HRUs
-------------------------------
.. warning::
  The Docker daemon must be running to use this feature.

1. **NetCDF file** : The NetCDF file to process (inluding the file extension).
2. **Shapefile attribute** (Optional) : Only needed if the Netcdf file is a shapefile. It is the attribute containing the numbering of the subbasins.
3. **Dim name longitude (x)** : The dimension name for the longitude (e.g. rlon).
4. **Dim name latitude (y)** : The dimension name for the latitude (e.g. rlat).
5. **Var name longitude (x)** : The variable name for the longitude (e.g. lon).
6. **Var name latitude (y)** : The variable name for the latitude (e.g. lat).
7. **HRUs file** : The final shapefile created by the BasinMaker tools.
8. **Use gauge ID** and **Use subbasins ID** : Either use a gauge ID or subbasins ID. The ID must be entered manually in the field below these options.
9. **Output path** : The path and file name of the results.

.. figure:: https://user-images.githubusercontent.com/98601298/188149605-f67b527a-4069-4a51-9830-4290c79fd0b8.png
  :width: 600
  
  Example of the gridweights generator interface.

.. _runrvn:

Run a Raven model
-----------------
To run a Raven model, you need to provide three information.

1. **Input directory** : The directory containing your Raven model files.
2. **Output directory** : The directory where the results of the simulation will be saved.
3. **Raven executable location** : The path to the Raven.exe file (including the filename).

Two other fields are also available, but they should be automatically filled by reading the .rvi file of your model.
If an error occurs and they are not filled automatically, please submit a `bug report <https://github.com/Scriptbash/QRaven/issues>`_.

1. **Filename prefix** : The name of the .rvi file (without the file extension)
2. **RunName** : The text following the command ":RunName" if used in the .rvi file. 

Draw the hydrograph
-------------------
After running a Raven model successfully (with or without QRaven), you will be able to draw the resulting hydrograph.
To do so, all that is required is the "Output directory" field and a click on the "Draw hydrograph" button. 

In the graph window, multiple buttons are available. They will allow you to zoom in and out, modify the graph size, customize the axis and export the graph as an image.

.. figure:: https://user-images.githubusercontent.com/98601298/188150121-ff889b56-5aa3-4e17-9d7f-28848896932d.png
  :width: 450
  
  Example of an hydrograph produced by QRaven.

Autofill a .rvp template file
------------------------------
A cool feature based on a RavenR function is available to attempt to automatically fill a .rvp template file.

In order to use this feature, a few steps are required.

1. Make sure the ":CreateRVPTemplate" command is used inside the .rvi file.
2. Run the model.
3. Click on the "Auto fill rvp template".
4. Review the generated .rvp file for any values that doe not have a default value. Those values will show as "0.12345".

.. note::
  This feature needs more testing and could have many oversights. To help improve it, please submit any problems you encounter by opening a `new issue <https://github.com/Scriptbash/QRaven/issues>`_.
  If possible, also send your Raven model so the issue can be easily reproduced.
