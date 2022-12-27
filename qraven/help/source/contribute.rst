How to contribute to QRaven
===========================
There are many ways you can contribute to QRaven and not only by coding!

Bug reporting
-------------
Reporting bugs and problems is very important, since even though I try to test as much as possible
the plugin, I can't run into every problems possible.

If you find any possible bugs, errors, typos, please open an issue on `GitHub <https://github.com/Scriptbash/QRaven/issues>`_.

Feature requests
----------------
I'm trying to add as many useful features to make Raven models and ease
the use of Raven in general. If there is a feature you would like or think would be useful,
please submit your request by either opening an `issue <https://github.com/Scriptbash/QRaven/issues>`_
or a `discussion <https://github.com/Scriptbash/QRaven/discussions>`_.

Development
-----------
If you want to contribute to the code, by adding new features, fixing bugs, optimizing the code,
you're welcome to do so!

QRaven is written in Python and uses PyQt for the graphical user interface. Here is a small guide
on how to setup your environment :

Setting up the environment
^^^^^^^^^^^^^^^^^^^^^^^^^^
.. note::

    The folder "QRaven" is not the QGIS plugin, it is the repository name.
    The folder "qraven" is the plugin. If it is zipped, it can be installed directly in
    the QGIS extension manager.

Before starting, find where the QGIS plugins folder is.

1. Open QGIS.
2. Click on the "**Settings**" menu.
3. Hover "**User Profiles**" and click on "**Open Active Profile Folder**".
4. Go inside the "**Python**" folder, then inside "**Plugins**". 
5. Remember this path, as this is where the "qraven" folder needs to be.
6. Clone QRaven's repository.
   
    .. code-block:: console

        git clone https://github.com/Scriptbash/QRaven.git

You now have two options, either copy/paste the qraven folder into the QGIS plugins folder or create a symbolic link. 
   
I prefer to create a symlink, as it allows to:

- modify the code.
- reload the plugin.
- see the changes.

as opposed to:

- modify the code.
- copy and paste the qraven folder into the plugins folder.
- reload the plugin.
- see the changes.

1. So, to create a symlink, open a "**terminal**" or "**command prompt**" depending on your operating system.
2. Type:
    
    for Linux and MacOS

     .. code-block:: console

        ln -s <path to qraven directory> <path to qgis plugins folder>

    for Windows

     .. code-block:: console

        mklink /D <path to qraven directory> <path to qgis plugins folder>

Now that the development version of QRaven is installed in QGIS, we will install
another QGIS plugin. The plugin will allow to reload QRaven after changes are made to
it, without the need to close QGIS and reopen it.

1. In QGIS, go to the "**Plugins**" menu.
2. Click on "**Manage and Install plugins**"
3. Click on "**All**" and search for "**Plugin Reloader**"
4. Open the "**Plugin Reloader**" and set it to reload QRaven

You are now good to go! Make changes to the code, reload QRaven with the plugin reloader and submit pull requests!

Files explanation
^^^^^^^^^^^^^^^^^
Not sure where to start? No worries, here is a quick overview of the important files :

- Inside the root folder of the repository, there is **Dockerfile** and **create_RVH.py**
  
  - **Dockerfile** is the file used to create the Docker image used for BasinMaker and the GridWeights generator
  - **create_RVH.py** file is the script that lies inside the Docker container. In other words, it is the script that runs the BasinMaker functions. 

- In the "qraven" folder, you will find many important files.
  
  - **qraven.py** is the main python file used for the plugin. 
  - **qraven_dialog_base.ui** is the graphical user interface of QRaven. You can open it with QtDesigner.

- In the "modules" folder, there are several python files that are imported inside the "qraven.py" file.
