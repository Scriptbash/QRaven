# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QRaven

 A QGIS plugin to help generate input files for Raven
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2022-03-22
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Francis Lapointe
        email                : francis.lapointe5@usherbrooke.ca
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import *
#from PyQt5 import QFileDialog
# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .qraven_dialog import QRavenDialog

import os.path
from sys import platform
import subprocess
from subprocess import Popen, PIPE

class QRaven:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'QRaven_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&QRaven')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('QRaven', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/qraven/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Generate Raven input files'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&QRaven'),
                action)
            self.iface.removeToolBarIcon(action)

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = QRavenDialog()

        #-------------Raven RVI-------------#
        #If the checkbox is checked/unchecked, enables/disables the associated widget
        self.dlg.chk_duration.stateChanged.connect(self.toggleWidget)
        self.dlg.chk_runname.stateChanged.connect(self.toggleWidget)
        self.dlg.chk_outputdir.stateChanged.connect(self.toggleWidget)
        self.dlg.chk_outputinterval.stateChanged.connect(self.toggleWidget)
        self.dlg.chk_wateryear.stateChanged.connect(self.toggleWidget)

        #Calls the function to enable/disable the spinbox for the soilmodel
        self.dlg.combo_soilmod.activated.connect(self.toggleSoilModel)
        self.dlg.combo_interpo.activated.connect(self.toggleInterpolation)

        #Calls the function to browse the computer for an output folder
        self.dlg.btn_outputdir.clicked.connect(self.browseDirectory)
     
        #Calls the function to write the RVI file
        self.dlg.btn_write.clicked.connect(self.writeRVI)
        #----------------------------------------#

        #-------------BasinMaker RVH-------------#
        
        #Calls the function that toggles the proper widgets depending on the mode chosen
        self.dlg.buttonGroup.buttonToggled.connect(self.toggleWidget)   #Define project spatial extent
        self.dlg.buttonGroup_2.buttonToggled.connect(self.toggleWidget)  #Delineate routing structure without lakes
        self.dlg.file_lakes.fileChanged.connect(self.toggleWidget)  #Add lake and obs control points
        self.dlg.chk_epsgcode.stateChanged.connect(self.toggleWidget)   #Enables/disables the 
        self.dlg.file_bankfullwidth.fileChanged.connect(self.toggleWidget)  #Add lake and obs control points
        self.dlg.file_landuserast.fileChanged.connect(self.toggleWidget)  #Add lake and obs control points

        
        
        #Calls the function to start the docker container
        self.dlg.btn_dockerrun.clicked.connect(self.dockerinit)
        #Calls the function to remove the docker container
        self.dlg.btn_dockerrm.clicked.connect(self.dockerdelete)

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()

        #----------------------------------------#

        # See if OK was pressed
        if result:
            # May remove completely this and keep only a close button in the GUI
            pass
    
    #This function enables and disables widgets based on their checkboxes/radiobutton state
    def toggleWidget(self):
        widget = self.dlg.sender()
        if widget.objectName() == 'chk_duration':
            if self.dlg.chk_duration.isChecked():
                self.dlg.date_enddate.setEnabled(False)
                self.dlg.spin_duration.setEnabled(True)
            else:
                self.dlg.date_enddate.setEnabled(True)
                self.dlg.spin_duration.setEnabled(False) 
        elif widget.objectName() == 'chk_runname':
            if self.dlg.chk_runname.isChecked():
                self.dlg.txt_runname.setEnabled(True)
            else:
                self.dlg.txt_runname.setEnabled(False)
        elif widget.objectName() == 'chk_outputdir':
            if self.dlg.chk_outputdir.isChecked():
                self.dlg.file_outputdir.setEnabled(True)
            else:
                self.dlg.file_outputdir.setEnabled(False)        
        elif widget.objectName() == 'chk_outputinterval':
            if self.dlg.chk_outputinterval.isChecked():
                self.dlg.spin_outinterval.setEnabled(True)
            else:
                self.dlg.spin_outinterval.setEnabled(False) 
        elif widget.objectName() == 'chk_wateryear':
            if self.dlg.chk_wateryear.isChecked():
                self.dlg.spin_wateryear.setEnabled(True)
            else:
                self.dlg.spin_wateryear.setEnabled(False) 
        #Conditions for the BasinMaker RVH section below
        elif widget.objectName() == 'buttonGroup':  #buttonGroup is the group of radiobuttons for the mode of define project spatial extent
            if self.dlg.rb_modehybasin.isChecked(): #If the selected mode is using_hybasin
                self.dlg.file_hybasin.setEnabled(True)
                self.dlg.spin_hybasin.setEnabled(True)
                self.dlg.txt_outletlat.setEnabled(False)
                self.dlg.txt_outletlon.setEnabled(False)
                self.dlg.file_providedply.setEnabled(False)
                self.dlg.spin_buffer.setEnabled(True)
            elif self.dlg.rb_outletpt.isChecked():  #Mode is using_outlet_pt
                self.dlg.file_hybasin.setEnabled(False)
                self.dlg.spin_hybasin.setEnabled(False)
                self.dlg.txt_outletlat.setEnabled(True)
                self.dlg.txt_outletlon.setEnabled(True)
                self.dlg.file_providedply.setEnabled(False)
                self.dlg.spin_buffer.setEnabled(False)
            elif self.dlg.rb_providedply.isChecked():   #Mode is using_provided_ply
                self.dlg.file_hybasin.setEnabled(False)
                self.dlg.spin_hybasin.setEnabled(False)
                self.dlg.txt_outletlat.setEnabled(False)
                self.dlg.txt_outletlon.setEnabled(False)
                self.dlg.file_providedply.setEnabled(True)
                self.dlg.spin_buffer.setEnabled(True)
            else:
                self.dlg.file_hybasin.setEnabled(False) #Mode is using_dem
                self.dlg.spin_hybasin.setEnabled(False)
                self.dlg.txt_outletlat.setEnabled(False)
                self.dlg.txt_outletlon.setEnabled(False)
                self.dlg.file_providedply.setEnabled(False)
                self.dlg.spin_buffer.setEnabled(False)
        elif widget.objectName() == 'buttonGroup_2':  #buttonGroup_2 is the group of radiobuttons for the mode of delineate routing structure w/o lakes
            if self.dlg.rb_fdr.isChecked(): #mode is using_fdr
                self.dlg.file_fdr.setEnabled(True)
            else:
                self.dlg.file_fdr.setEnabled(False) #Mode is using_dem
        elif widget.objectName() == 'file_lakes':   #Add lake and obs control point
            if self.dlg.file_lakes.filePath() != '':    #If there is a layer for Lakes, enable the required fields
                self.dlg.txt_lakeid.setEnabled(True)
                self.dlg.txt_laketype.setEnabled(True)
                self.dlg.txt_lakevol.setEnabled(True)
                self.dlg.txt_lakeavgdepth.setEnabled(True)
                self.dlg.txt_lakearea.setEnabled(True)
                self.dlg.spin_conlakearea.setEnabled(True)
                self.dlg.spin_nonconlakearea.setEnabled(True)
            else:   #If the layer is removed or there's no layer, disable the fields
                self.dlg.txt_lakeid.setEnabled(False)
                self.dlg.txt_laketype.setEnabled(False)
                self.dlg.txt_lakevol.setEnabled(False)
                self.dlg.txt_lakeavgdepth.setEnabled(False)
                self.dlg.txt_lakearea.setEnabled(False)
                self.dlg.spin_conlakearea.setEnabled(False)
                self.dlg.spin_nonconlakearea.setEnabled(False)
        elif widget.objectName() == 'chk_epsgcode':
            if self.dlg.chk_epsgcode.isChecked():
                self.dlg.txt_epsgcode.setEnabled(True)
            else:
                self.dlg.txt_epsgcode.setEnabled(False)
        elif widget.objectName() == 'file_bankfullwidth':   #Add hydrology related attributes
            if self.dlg.file_bankfullwidth.filePath() != '':    #If there is a layer for bankfull width, enable the required fields
                self.dlg.txt_bankfullwidth.setEnabled(True)
                self.dlg.txt_bankfulldepth.setEnabled(True)
                self.dlg.txt_bankfulldischarge.setEnabled(True)
                self.dlg.txt_bankfulldrainarea.setEnabled(True)
                self.dlg.spin_kcoef.setEnabled(False)
                self.dlg.spin_ccoef.setEnabled(False)

            else:   #If the layer is removed or there's no layer, disable the fields
                self.dlg.txt_bankfullwidth.setEnabled(False)
                self.dlg.txt_bankfulldepth.setEnabled(False)
                self.dlg.txt_bankfulldischarge.setEnabled(False)
                self.dlg.txt_bankfulldrainarea.setEnabled(False)
                self.dlg.spin_kcoef.setEnabled(True)
                self.dlg.spin_ccoef.setEnabled(True)

        elif widget.objectName() == 'file_landuserast':   #Add hydrology related attributes
            if self.dlg.file_landuserast.filePath() != '':    #If there is a layer for landuse (raster), enable the required fields
                self.dlg.file_landusemanning.setEnabled(True)
            else:   #If the layer is removed or there's no layer, disable the fields
                self.dlg.file_landusemanning.setEnabled(False) 
              

    #This function enables and disables the spinbox next to the SoilModel combobox depending on the selected value of the combobox
    def toggleSoilModel(self):
        if self.dlg.combo_soilmod.currentText().lower() == "soil_multilayer":
            self.dlg.spin_soilmod.setEnabled(True)
        else:
            self.dlg.spin_soilmod.setEnabled(False)

    #This function enables and disables the line edit next to the InterpolationMethod is INTERP_FROM_FILE.
    def toggleInterpolation(self):
        if self.dlg.combo_interpo.currentText().lower() == "interp_from_file":
            self.dlg.txt_interpofile.setEnabled(True)
        else:
            self.dlg.txt_interpofile.setEnabled(False)

    #This function opens a file explorer to select an output folder
    def browseDirectory(self):
        dir = str(QFileDialog.getExistingDirectory(None, "Select Directory"))
        self.dlg.txt_outputdir.setText(dir)
        
    #This function writes all the parameters entered by the user into the RVI file
    def writeRVI(self):
        paramDict = self.getParams()
        customOutputList = self.getCustomOutput()
        #print(paramDict)
        outputdir = self.dlg.txt_outputdir.text()
        modelName = self.dlg.txt_modname.text()
        print(outputdir)
        try:
            if computerOS == "linux" or computerOS == "macos":  #Adds a slash or backslash to the path depending on which os is being used
                pathToFolder = outputdir+'/'+modelName
            else:
                pathToFolder = outputdir+'\\'+modelName
            #Creates the RVI file with the name and path provided
            with open(pathToFolder+".rvi","w") as rvi:
                #Writes the parameters from the dictionary
                for key, value in paramDict.items():
                    if value != '' and value != "checked":
                        rvi.write(f":{key:<30}  {value}\n")
                    elif value == "checked":   #This writes the optional I/O which don't have an argument (so only the key is written)
                        rvi.write(f":{key:<30}\n")
                #Writes the custom output
                count = 0
                rvi.write("{:<33}".format(":CustomOutput"))
                for output in customOutputList:
                    if count == 4:
                        count = 0
                        if output == ' ':
                            count+=1
                            pass
                        else:
                            rvi.write("\n{:<33}".format(":CustomOutput")+output+" ")
                            count+=1
                    else:
                        if output == ' ':
                            count+=1
                            pass
                        else:
                            rvi.write(output + " ")
                            count+=1

            #!!!Must add a message push in qgis to let the user know!!!
            print("RVI file written successfully")
        except Exception as e:
            print("Unable to write the RVI file")
            print(e)

    #This function gathers all the RVI parameters entered by the user and return them into a dictionary
    def getParams(self):
        #Get the start date
        startDateTmp = self.dlg.date_startdate.dateTime()
        startDate = str(startDateTmp.toPyDateTime())
        #Get the end date or duration
        if self.dlg.chk_duration.isChecked():
            keyDuration = "Duration" 
            duration = str(self.dlg.spin_duration.value())
        else:
            keyDuration = "EndDate"
            endDateTmp = self.dlg.date_enddate.dateTime()
            duration = str(endDateTmp.toPyDateTime())
            #Must not forget to add condition in the dictionary
        #Get the time step
        timeStepTmp = self.dlg.date_timestep.time()
        timeStep = str(timeStepTmp.toPyTime())
        #Get soil model
        if self.dlg.combo_soilmod.currentText().lower() == "soil_multilayer":
            soilMod = self.dlg.combo_soilmod.currentText() + ' ' + str(self.dlg.spin_soilmod.value())
        else:
            soilMod = self.dlg.combo_soilmod.currentText()
        #Get Define HRU groups
        defHRUGroups = self.dlg.txt_defhru.toPlainText()
        #Get catchment route
        catchment = self.dlg.combo_catchment.currentText()
        #Get routing
        routing = self.dlg.combo_routing.currentText()
        #Get method
        method= self.dlg.combo_method.currentText()   
        #Get interpolation method
        if self.dlg.combo_interpo.currentText().lower() == "interp_from_file":
            interpolation = self.dlg.combo_interpo.currentText() + ' ' + self.dlg.txt_interpofile.text()
        else:
            interpolation = self.dlg.combo_interpo.currentText()
        #Get evaporation
        evaporation = self.dlg.combo_evapo.currentText()     
        #Get rain snow fraction
        rainsnowfract = self.dlg.combo_rainsnowfrac.currentText()
        #Get OW_Evaporation
        owevapo = self.dlg.combo_owevapo.currentText()
        #Get OroPrecipCorrect
        oroprecip = self.dlg.combo_oroprecip.currentText()
        #Get OroTempCorrect
        orotemp = self.dlg.combo_orotemp.currentText()
        #Get OroPetCorrect
        oropet = self.dlg.combo_oropet.currentText()
        #Get CloudCoverMethod
        cloudcover = self.dlg.combo_cloudcover.currentText()
        #Get AirPressureMethod
        airpressure = self.dlg.combo_airpressure.currentText()
        #Get PotentionMelt
        potmelt = self.dlg.combo_potentialmelt.currentText()
        #Get MonthlyInterpolationMethod
        monthlyinterpo = self.dlg.combo_monthlyinterpo.currentText()
        #Get LakeStorage
        lakestorage = self.dlg.combo_lakestorage.currentText()
        #Get SWRadiationMethod
        swradiation = self.dlg.combo_swradation.currentText()
        #Get SWCanopyCorrect
        swcanopy = self.dlg.combo_swcanopy.currentText()
        #Get SWCloudCorrect
        swcloud = self.dlg.combo_swcloud.currentText()
        #Get LWRadiationMethod
        lwradiation = self.dlg.combo_lwradation.currentText()
        #Get WindSpeedMethod
        windspeed = self.dlg.combo_windspeed.currentText()
        #Get RelativeHumidityMethod
        relhumidity = self.dlg.combo_relhumidity.currentText()
        #Get PrecipIceptFract
        precipicept = self.dlg.combo_precipicept.currentText()
        #Get RechargeMethod
        recharge = self.dlg.combo_recharge.currentText()
        #Get SubdailyMethod
        subdaily = self.dlg.combo_subdaily.currentText()
        #Get Calendar
        calendar = self.dlg.combo_calendar.currentText()
        #Get all the option IO commands
        if self.dlg.chk_runname.isChecked():
            runname = self.dlg.txt_runname.text()
        else:
            runname = ''
        if self.dlg.chk_outputdir.isChecked():
            fileoutputdir = self.dlg.file_outputdir.filePath() 
        else:
            fileoutputdir = ''
        if self.dlg.chk_outputinterval.isChecked():
            outputinterval = self.dlg.spin_outinterval.value()
        else:
            outputinterval = ''
        if self.dlg.chk_rvptemplate.isChecked():
            rvptemplate = "checked"
        else:
            rvptemplate = ''
        if self.dlg.chk_writemassbal.isChecked():
            writemassbal = "checked"
        else:
            writemassbal = ''
        if self.dlg.chk_endpause.isChecked():
            endpause = "checked"
        else:
            endpause = ''
        if self.dlg.chk_writeforcingfunc.isChecked():
            writeforcing = "checked"
        else:
            writeforcing = ''
        if self.dlg.chk_debugmode.isChecked():
            debugmode = "checked"
        else:
            debugmode = ''
        if self.dlg.chk_silentmode.isChecked():
            silentmode = "checked"
        else:
            silentmode = ''
        if self.dlg.chk_writedemand.isChecked():
            writedemand = "checked"
        else:
            writedemand = ''
        if self.dlg.chk_writeenergy.isChecked():
            writeenergy = "checked"
        else:
            writeenergy = ''
        if self.dlg.chk_writeexausmb.isChecked():
            writeexausmb = "checked"
        else:
            writeexausmb = ''
        if self.dlg.chk_writeensim.isChecked():
            writeensim = "checked"
        else:
            writeensim = ''
        if self.dlg.chk_suppressoutput.isChecked():
            suppressoutput = "checked"
        else:
            suppressoutput = ''
        if self.dlg.chk_snaphydro.isChecked():
            snaphydro = "checked"
        else:
            snaphydro = ''
        if self.dlg.chk_wateryear.isChecked():
            wateryear = self.dlg.spin_wateryear.value()
        else:
            wateryear = ''
        
        #Writes the selected evaluation metrics
        if not self.dlg.list_evalmetrics.selectedItems(): 
            evalmetrics = ''            #If nothing is selected, assign empty text to the variable to avoid crash
        else:
            firstloop = True
            for item in self.dlg.list_evalmetrics.selectedItems():
                if firstloop != False:
                    evalmetrics = item.text()
                    firstloop = False
                else:
                    evalmetrics= evalmetrics + ', ' + item.text()
        evalmetrics = evalmetrics.replace(',',' ')  #Removes the commas between the metrics

        #Create the dictionary
        paramsDict = { 
            "Calendar"                   : calendar,
            "StartDate"                  : startDate,
            keyDuration                  : duration,
            "TimeStep"                   : timeStep,
            "SoilModel"                  : soilMod,
            "DefineHRUGroups"            : defHRUGroups,
            "CatchmentRoute"             : catchment,
            "Routing"                    : routing,
            "Method"                     : method,
            "InterpolationMethod"        : interpolation,
            "Evaporation"                : evaporation,
            "RainSnowFraction"           : rainsnowfract,
            "OW_Evaporation"             : owevapo,
            "OroPrecipCorrect"           : oroprecip,
            "OroTempCorrect"             : orotemp,
            "OroPetCorrect"              : oropet,
            "CloudCoverMethod"           : cloudcover,
            "AirPressureMethod"          : airpressure,
            "PotentialMelt"              : potmelt,
            "MonthlyInterpolationMethod" : monthlyinterpo,
            "LakeStorage"                : lakestorage,
            "SWRadiationMEthod"          : swradiation,
            "SWCanopyCorrect"            : swcanopy,
            "SWCloudCorrect"             : swcloud,
            "LWRadationMethod"           : lwradiation,
            "WindSpeedMethod"            : windspeed,
            "RelativeHumidityMethod"     : relhumidity,
            "PrecipIceptFract"           : precipicept,
            "RechargeMethod"             : recharge,
            "SubdailyMethod"             : subdaily,
            "RunName"                    : runname,
            "OutputDirectory"            : fileoutputdir,
            "OutputInterval"             : outputinterval,
            "CreateRVPTemplate"          : rvptemplate,
            "WaterYearStartMonth"        : wateryear,
            "WriteMassBalanceFile"       : writemassbal,
            "writeForcingFunctions"      : writeforcing,
            "EndPause"                   : endpause,
            "DebugMode"                  : debugmode,
            "SilentMode"                 : silentmode,
            "WriteDemandFile"            : writedemand,
            "WriteEnergyStorage"         : writeenergy,
            "WriteExhaustiveMB"          : writeexausmb,
            "WriteEnsimFormat"           : writeensim,
            "SuppressOutput"             : suppressoutput,
            "SnapshotHydrograph"         : snaphydro,
            "EvaluationMetrics"          : evalmetrics
        }

        return paramsDict

    #This function fetches the custom output widgets' values and returns them into a list
    def getCustomOutput(self):
        customOutputList = []
        #Loop through all the Custom Ouput widgets in order to get their values and add them to a list
        for i in range(self.dlg.gridLayout.count()):
            if isinstance(self.dlg.gridLayout.itemAt(i).widget(),QComboBox):    #Get the combobox values
                if self.dlg.gridLayout.itemAt(i).widget().currentText() != '':
                    #print(self.dlg.gridLayout.itemAt(i).widget().currentText())
                    customOutputList.append(self.dlg.gridLayout.itemAt(i).widget().currentText())
                else: 
                    customOutputList.append(" ")
            else:
                if self.dlg.gridLayout.itemAt(i).widget().text() != '': #Get the line edit values
                    #print(self.dlg.gridLayout.itemAt(i).widget().text())
                    customOutputList.append(self.dlg.gridLayout.itemAt(i).widget().text())
                else: 
                    customOutputList.append(" ")

        return customOutputList
        #!!!!MISSING QUARTILES OPTION IN THE GUI!!!

    #This function sets up the scriptbash/basinmaker docker container. Pulls, starts and sets the python path
    def dockerinit(self):
        pythonpaths = [
                        "export PYTHONPATH=$PYTHONPATH:'/usr/lib/grass78/etc/python'",
                        "export PYTHONPATH=$PYTHONPATH:'/usr/share/qgis/python/plugins'",
                        "export PYTHONPATH=$PYTHONPATH:'/usr/share/qgis/python'",
                        "Xvfb :99 -screen 0 640x480x8 -nolisten tcp &"
                    ] 
        
        paramsDict = self.getRVHparams()
        self.exportRVHparams(paramsDict)
        # try:
        #     print("pulling")
        #     cmd='docker', 'pull', 'scriptbash/basinmaker'
        #     process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        #     while True:
        #         output = process.stdout.readline()
        #         if output == b'':
        #             break
        #         if output:
        #             #test = str(output.strip())
        #             #self.dlg.txt_console.appendPlainText(test)
        #             print(output.strip())
        #     rc = process.poll()
        #     print("went out of the loop")
        # except Exception as e:
        #     print(e)

        #!!!Missing the docker run command, export python paths, xvfb to fake a display!!!
      
    #This function fully removes the container, as well as the image to free up space
    def dockerdelete(self):
        try:
            #self.dlg.txt_console.appendPlainText("Making sure the container is stopped > docker stop bmaker")
            os.system("docker stop bmaker")
            #self.dlg.txt_console.appendPlainText("Successfully stopped the containter")
            #self.dlg.txt_console.appendPlainText("Removing the docker container > docker rm bmaker")
            os.system("docker rm bmaker")
            #self.dlg.txt_console.appendPlainText("Successfully removed the container > docker rmi scriptbash/basinmaker")
            #self.dlg.txt_console.appendPlainText("Removing the image")
            os.system("docker rmi scriptbash/basinmaker")
            print("container stopped and removed")
            #self.dlg.txt_console.appendPlainText("Successfully removed the image. Everything was removed.")
        except Exception as e:
            #self.dlg.txt_console.appendPlainText("An error occured while attempting to remove the container and image. Please remove them manually.")
            print("An error occured while attempting to remove the docker container and image")
            print(e)


    def getRVHparams(self):

        pathdem = self.dlg.file_dem.filePath()
        pathlandusepoly = self.dlg.file_landusepoly.filePath()
        pathlanduserast = self.dlg.file_landuserast.filePath()
        pathlakes = self.dlg.file_lakes.filePath()
        if pathlakes == '': #Since the lakes are optional, assign a value so the parameter is still written. 
            pathlakes = '#' #This allows to make a check in the create_RVH.py
        pathbankfull = self.dlg.file_bankfullwidth.filePath()
        pathsoil = self.dlg.file_soil.filePath()
        pathpointsinterest = self.dlg.file_pointsinterest.filePath()
        maxmemory = self.dlg.spin_ram.value()

        if self.dlg.rb_modedem.isChecked():
            extentMode = "using_dem"
            path_hybasin = ''
            hybasinid = ''
            bufferdistance = ''
            outletlat = ''
            outletlon = ''
            path_providedpoly = ''
        elif self.dlg.rb_modehybasin.isChecked():
            extentMode = "using_hybasin"
            path_hybasin = self.dlg.file_hybasin.filePath()
            hybasinid   = str(self.dlg.spin_hybasin.value())
            bufferdistance = str(self.dlg.spin_buffer.value())
            outletlat = ''
            outletlon = ''
            path_providedpoly = ''
        elif self.dlg.rb_outletpt.isChecked():
            extentMode = "using_outlet_pt"
            outletlat = self.dlg.txt_outletlat.text()
            outletlon = self.dlg.txt_outletlon.text()
            path_hybasin = ''
            hybasinid = ''
            bufferdistance = ''
            path_providedpoly = ''
        elif self.dlg.rb_providedply.isChecked():
            extentMode = "using_provided_ply"
            path_providedpoly = self.dlg.file_providedply.filePath()
            bufferdistance = str(self.dlg.spin_buffer.value())
            path_hybasin = ''
            hybasinid = ''
            outletlat = ''
            outletlon = ''
        
        if self.dlg.file_lakes.filePath:
            lakeid = self.dlg.txt_lakeid.text()
            laketype = self.dlg.txt_laketype.text()
            lakevol = self.dlg.txt_lakevol.text()
            lakeavgdepth = self.dlg.txt_lakeavgdepth.text()
            lakearea = self.dlg.txt_lakearea.text()
            connectedlake = self.dlg.spin_conlakearea.value()
            nonconnectedlake = self.dlg.spin_nonconlakearea.value()
        else:
            lakeid = ''
            laketype = ''
            lakevol = ''
            lakeavgdepth = ''
            lakearea = ''
            connectedlake = ''
            nonconnectedlake = ''

        poiid = self.dlg.txt_poiid.text()
        poiname = self.dlg.txt_poiname.text()
        poidrainarea = self.dlg.txt_poidrainarea.text()
        poisource = self.dlg.txt_poisource.text()

        if self.dlg.chk_epsgcode.isChecked():
            epsgcode = self.dlg.txt_epsgcode.text()
        else:
            epsgcode = ''


        if self.dlg.file_bankfullwidth.filePath():
            bankfullwidth = self.dlg.txt_bankfullwidth.text()
            bankfulldepth = self.dlg.txt_bankfulldepth.text()
            bankfulldischarge = self.dlg.txt_bankfulldischarge.text()
            bankfulldrainage = self.dlg.txt_bankfulldrainarea.text()
            kcoef = ''
            ccoef = ''
        else:
            bankfullwidth = ''
            bankfulldepth = ''
            bankfulldischarge = ''
            bankfulldrainage = ''
            kcoef = str(self.dlg.spin_kcoef.value())
            ccoef = str(self.dlg.spin_ccoef.value())

        if self.dlg.file_landuserast.filePath():
            landusemanning = self.dlg.file_landusemanning.filePath()
        else:
            landusemanning = ''
        
        facthreshold = self.dlg.spin_facthreshold.value()

        if self.dlg.rb_fdr.isChecked():
            delineatemode = "using_fdr"
            pathfdr = self.dlg.file_fdr.filePath()
        elif self.dlg.rb_dem.isChecked():
            delineatemode = "using_dem"
            pathfdr = ''

        params = {
            "pathdem"               : pathdem,
            "pathlandusepoly"       : pathlandusepoly,
            "pathlanduserast"       : pathlanduserast,
            "pathlakes"             : pathlakes,
            "pathbankfull"          : pathbankfull,
            "pathsoil"              : pathsoil,
            "pathpointsinterest"    : pathpointsinterest,
            "maxmemory"             : maxmemory,
            "extentmode"            : extentMode,
            "pathhybasin"           : path_hybasin,
            "hybasinid"             : hybasinid,
            "bufferdistance"        : bufferdistance,
            "outletlat"             : outletlat,
            "outletlon"             : outletlon,
            "path_providedpoly"     : path_providedpoly,
            "lakeid"                : lakeid,
            "laketype"              : laketype,
            "lakevol"               : lakevol,
            "lakeavgdepth"          : lakeavgdepth,
            "lakearea"              : lakearea,
            "connectedlake"         : connectedlake,
            "nonconnectedlake"      : nonconnectedlake,
            "poiid"                 : poiid,
            "poiname"               : poiname,
            "poidrainarea"          : poidrainarea,
            "poisource"             : poisource,
            "epsgcode"              : epsgcode,
            "bankfullwidth"         : bankfullwidth,
            "bankfulldepth"         : bankfulldepth,
            "bankfulldischarge"     : bankfulldischarge,
            "bankfulldrainage"      : bankfulldrainage,
            "kcoef"                 : kcoef,
            "ccoef"                 : ccoef,
            "landusemanning"        : landusemanning,
            "facthreshold"          : facthreshold,
            "delineatemode"         : delineatemode,
            "pathfdr"               : pathfdr
        }
        return params

    def exportRVHparams(self,paramDict):
        outputdir = self.dlg.file_outputfolder.filePath()
        try:
            if computerOS == "linux" or computerOS == "macos":  #Adds a slash or backslash to the path depending on which os is being used
                pathToFolder = outputdir+'/'+ "parameters"
            else:
                pathToFolder = outputdir+'\\'+ "parameters"
            #Creates the rvh parameters file with path provided
            with open(pathToFolder+".txt","w") as file:
                #Writes the parameters from the dictionary
                for key, value in paramDict.items():
                    if value != '':
                        file.write(f"{key:<30}  {value}\n")
            print("Successfully exported the RVH parameters")
        except Exception as e:
            print("Could not export the BasinMaker parameters")
            print(e)
#This function return the user's operating system. Mainly used to put slashes and backslashes accordingly in paths            
def checkOS():
    if platform == "linux" or platform == "linux2":
        return "linux"
    elif platform == "darwin":
        return "macos"
    elif platform == "win32":
        return "windows"
computerOS = checkOS()
