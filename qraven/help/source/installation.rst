Installation
============

.. _Installation:

Dependencies
------------

To use QRaven, first install a recent version of QGIS (3.20 and above):
`https://qgis.org/en/site/forusers/download.html <https://qgis.org/en/site/forusers/download.html>`_


Some features, such as the BasinMaker tools and the GridWeight Generator, require Docker to be installed. If you are not planning on using those features, you can skip this step. Otherwise, you can get Docker here:
`https://docs.docker.com/get-docker <https://docs.docker.com/get-docker>`_

.. warning::
   Linux users must run Docker as a non root user. This can be done with the following command:

   .. code-block:: console

      sudo usermod -aG docker $USER

   For more information, go to:
   `https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user <https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user>`_


Plugin installation
-------------------
Now that QGIS is installed, simply download the latest release of QRaven here:
`https://github.com/Scriptbash/QRaven/releases/latest/download/qraven.zip <https://github.com/Scriptbash/QRaven/releases/latest/download/qraven.zip>`_

Alternatively, you can view all of QRaven versions here : 
`https://github.com/Scriptbash/QRaven/releases <https://github.com/Scriptbash/QRaven/releases>`_


Next, open QGIS and go to the "Plugins" menu. Click on "Manage and Install Plugins"

.. image:: https://user-images.githubusercontent.com/98601298/170998843-1fa7c283-e15b-4dce-a684-59e16a5c71d4.png
  :width: 400

Finally, click on "Install from ZIP", select the downloaded qraven.zip file and click on "Install".

.. image:: https://user-images.githubusercontent.com/98601298/170999288-1d8db5dc-5709-4139-8aff-412dc76eb1c2.png
  :width: 600

.. note::
   The plugin will look for an update each time QGIS is started. If it finds one, you will have a small notification at the bottom of the plugin window.
