from qgis.PyQt.QtWidgets import *

def addprocess(self):

    table = self.dlg.table_hydroprocess #Get the hydrologic processes table
    currentRow = table.rowCount()   #Get the number of rows the table has
    table.insertRow(currentRow) #Inserts a new row below the last row

    combo_proc = QComboBox() 
    combo_alg = QComboBox()
    combo_from = QComboBox()
    combo_from2 = QComboBox() 
    combo_from2.setEnabled(False)  
    combo_to = QComboBox()
    combo_to2 = QComboBox()
    combo_to2.setEnabled(False)
       
    chk_isconditional = QCheckBox()

    combo_basedtype = QComboBox()
    combo_comparison = QComboBox()

    txt_hrutype = QLineEdit()

    chk_mixingrate = QCheckBox()
    spin_pct = QDoubleSpinBox()

    chk_interbasin = QCheckBox()

    combo_proc.addItems(procname)   #Add a combobox in the new row with all the available processes
    combo_basedtype.setEnabled(False)
    combo_comparison.setEnabled(False)
    txt_hrutype.setEnabled(False)
    chk_mixingrate.setEnabled(False)
    spin_pct.setEnabled(False)
    spin_pct.setDecimals(1)
    chk_interbasin.setEnabled(False)
    table.setCellWidget(currentRow, 0, combo_proc)  #Sets the new combobox in the first column and in the new row
    table.setCellWidget(currentRow, 1, combo_alg)
    table.setCellWidget(currentRow, 2, combo_from)
    table.setCellWidget(currentRow, 3, combo_from2)
    table.setCellWidget(currentRow, 4, combo_to)
    table.setCellWidget(currentRow, 5, combo_to2)
    table.setCellWidget(currentRow, 6, chk_isconditional)
    table.setCellWidget(currentRow, 7, combo_basedtype)
    table.setCellWidget(currentRow, 8, combo_comparison)
    table.setCellWidget(currentRow, 9, txt_hrutype)
    table.setCellWidget(currentRow, 10, chk_mixingrate)
    table.setCellWidget(currentRow, 11, spin_pct)
    table.setCellWidget(currentRow, 12, chk_interbasin)

    table.resizeColumnsToContents() #Resizes the width of the column automatically
    combo_proc.currentIndexChanged.connect(lambda:setProcAlg(self,currentRow))  #Updates the algorithm combobox if the process changes
    chk_isconditional.stateChanged.connect(lambda:enableConditionalProc(self, currentRow))


def removeprocess(self):
        table = self.dlg.table_hydroprocess
        selectedRow = table.currentRow()
        table.removeRow(selectedRow)


def setProcAlg(self,row):
    #print('Went into the algs')
    table = self.dlg.table_hydroprocess
    
    combo_proc = table.cellWidget(row, 0)
    combo_alg = table.cellWidget(row, 1)  #Sets the new combobox in the first column and in the new row
    combo_from2 = table.cellWidget(row, 3)
    combo_to2 = table.cellWidget(row, 5)
    chk_mixingrate = table.cellWidget(row, 10)
    spin_pct = table.cellWidget(row, 11)
    chk_interbasin = table.cellWidget(row, 12)

    combo_from2.setEnabled(False)
    combo_to2.setEnabled(False)
    combo_alg.setEnabled(True)
    spin_pct.setEnabled(False)
    chk_interbasin.setChecked(False)
    chk_interbasin.setEnabled(False)
    chk_mixingrate.setChecked(False)
    chk_mixingrate.setEnabled(False)
    #currentWidget = self.dlg.sender()
    # index = self.dlg.table_hydroprocess.indexAt(currentWidget.pos())
    # widgetRow = index.row()
    combo_alg.clear()
    combo_from2.clear()
    combo_to2.clear()
    combo_alg.addItem('')

    # if isinstance(currentWidget, QComboBox):
    selectedProc = combo_proc.currentText()
    #print(selectedProc)
    if selectedProc == 'Precipitation':
        combo_alg.addItems(precipalg)
    elif selectedProc == 'CanopyEvaporation':
        combo_alg.addItems(canopevapAlg)
    elif selectedProc == 'CanopySublimation':
        combo_alg.addItems(canopysublimationAlg)
    elif selectedProc == 'SoilEvaporation':
        combo_alg.addItems(soilevapAlg)
    elif selectedProc == 'LakeEvaporation':
        combo_alg.addItems(lakeevapAlg)
    elif selectedProc == 'OpenWaterEvaporation':
        combo_alg.addItems(openwaterevapAlg)
    elif selectedProc == 'Infiltration':
        combo_alg.addItems(infiltrationAlg)
    elif selectedProc == 'Percolation':
        combo_alg.addItems(percolationAlg)
    elif selectedProc == 'CapillaryRise':
        combo_alg.addItems(cappilaryriseAlg)
    elif selectedProc == 'Baseflow':
        combo_alg.addItems(baseflowAlg)
    elif selectedProc == 'Interflow':
        combo_alg.addItems(interflowAlg)
    elif selectedProc == 'Seepage':
        combo_alg.addItems(seepageAlg)
    elif selectedProc == 'DepressionOverflow':
        combo_alg.addItems(depresoverflowAlg)
    elif selectedProc == 'LakeRelease':
        combo_alg.addItems(lakereleaseAlg)
    elif selectedProc == 'Abstraction':
        combo_alg.addItems(abstractionAlg)
    elif selectedProc == 'SnowMelt':
        combo_alg.addItems(snowmeltAlg)
    elif selectedProc == 'SnowRefreeze':
        combo_alg.addItems(snowrefreezeAlg)
    elif selectedProc == 'SnowBalance':
        combo_alg.addItems(snowbalanceAlg)
    elif selectedProc == 'SnowTempEvolve':
        combo_alg.addItems(snowtempevolveAlg)
    elif selectedProc == 'Sublimation':
        combo_alg.addItems(sublimationAlg)
    elif selectedProc == 'SnowAlbedoEvolve':
        combo_alg.addItems(snowalbedoevolveAlg)
    elif selectedProc == 'SnowSqueeze':
        combo_alg.addItems(snowsqueezeAlg)
    elif selectedProc == 'CanopyDrip':
        combo_alg.addItems(canopydripAlg)
    elif selectedProc == 'CropHeatUnitEvolve':
        combo_alg.addItems(cropheatunitevAlg)
    elif selectedProc == 'GlacierMelt':
        combo_alg.addItems(glaciermeltAlg)
    elif selectedProc == 'GlacierRelease':
        combo_alg.addItems(glacierreleaseAlg)
    elif selectedProc == 'GlacierInfiltration':
        combo_alg.addItems(glacierinfiltrationAlg)
    elif selectedProc == 'Flush':
        combo_alg.addItems(flushAlg)
        chk_mixingrate.setEnabled(True)
    elif selectedProc == 'Overflow':
        combo_alg.addItems(overflowAlg)
    elif selectedProc == 'Abstraction':
        combo_alg.addItems(abstractionAlg)
    elif selectedProc == 'Split':
        combo_to2.setEnabled(True)
        combo_alg.addItems(splitAlg)
        chk_mixingrate.setEnabled(True)
    elif selectedProc == 'Convolve':
        combo_alg.addItems(convolutionAlg)
    elif selectedProc == 'LateralFlush':
        combo_from2.setEnabled(True)
        combo_to2.setEnabled(True)
        combo_alg.addItems(lateralflushAlg)
    elif selectedProc == 'LateralEquilibrate':
        combo_alg.addItems(lateralequilibrateAlg)
        spin_pct.setEnabled(True)
        spin_pct.setSingleStep(0.1)
        spin_pct.setMaximum(1.0)
        spin_pct.setMinimum(0.0)
        spin_pct.setDecimals(1)
        chk_interbasin.setEnabled(True)
    elif selectedProc == 'ExchangeFlow':
        combo_alg.addItems(exchangeflowAlg)
    elif selectedProc == 'Recharge':
        combo_alg.addItems(rechargeAlg)
    elif selectedProc == 'BlowingSnow':
        combo_alg.addItems(blowingsnowAlg)
    elif selectedProc == 'SoilBalance':
        combo_alg.addItems(soilbalanceAlg)
    elif selectedProc == 'RedirectFlow':
        combo_alg.setEnabled(False)
        
    #table.setCellWidget(row, 1, combo_alg)
    #table.setCellWidget(row, 2, combo_from)
    #table.setCellWidget(row, 3, combo_to)
    # table.setCellWidget(row, 8, chk_mixingrate)
    # table.setCellWidget(row, 9, spin_pct)
    # table.setCellWidget(row, 10, chk_interbasin)

    table.resizeColumnsToContents()

    chk_mixingrate.stateChanged.connect(lambda:enableMixingRate(self,row))
    combo_alg.currentIndexChanged.connect(lambda:setStorage(self, selectedProc, row))   #Updates the compartments combobox if the algorithm changed
    #self.setStorage(selectedProc)   #Needed for RedirectFlow... there's probably a better way

#This method sets the combobox values for the from and to compartments based on the selected algorithm
def setStorage(self,selectedProc, row):

    table = self.dlg.table_hydroprocess #Get the hydrologic processes table

    #Clears the lists to avoid infinite duplicates
    fromPercolation.clear()
    toPercolation.clear()
    fromCapillaryRise.clear()
    toCapillaryRise.clear()
    fromBaseflow.clear()
    fromInterflow.clear()
    toSeepage.clear()
    fromExchangeflow.clear()
    toExchangeflow.clear()
    fromRecharge.clear()
    toRecharge.clear()
    fromConvolution.clear()
    tmpanyCompartment = anyCompartment.copy()
    #Loops through the number of soil layers chosen by the user. Allows to add the soil[m] to comboboxes
    if self.dlg.combo_soilmod.currentText().lower() == "soil_multilayer":
        numberSoil = int(self.dlg.spin_soilmod.value()) #Get the number of layers
    elif self.dlg.combo_soilmod.currentText().lower() == "soil_two_layer":
        numberSoil = 2
    else:
        numberSoil = 1
    for layer in range(numberSoil):
        compartment = "SOIL["+str(layer)+']'    #Create the string to append to the list
        #Append the soil[m] to the comboboxes
        fromPercolation.append(compartment)
        toPercolation.append(compartment)
        fromCapillaryRise.append(compartment)
        toCapillaryRise.append(compartment)
        fromBaseflow.append(compartment)
        fromInterflow.append(compartment)
        toSeepage.append(compartment)
        fromExchangeflow.append(compartment)
        toExchangeflow.append(compartment)            
        toRecharge.append(compartment)
        tmpanyCompartment.append(compartment)
    for layer in range(numberSoil):
        compartment = "CONVOLUTION["+str(layer)+']'
        fromConvolution.append(compartment) 
        tmpanyCompartment.append(compartment)

    tmpanyCompartment = list(dict.fromkeys(tmpanyCompartment))
    #tmpanyCompartment.sort()
    #currentWidget = self.dlg.sender()   #Get the widget that was triggered
    #index = self.dlg.table_hydroprocess.indexAt(currentWidget.pos())    #Get the index of the widget
    #widgetRow = index.row() #Get the row in which the widget is set
    # combo_from = QComboBox()    #Initialize the combobox for the from compartment
    # combo_to = QComboBox()      #Initialize the combobox for the to compartment
    combo_proc = table.cellWidget(row, 0)
    combo_alg = table.cellWidget(row, 1)
    combo_from = table.cellWidget(row, 2)
    combo_from2 = table.cellWidget(row,3)
    combo_to = table.cellWidget(row, 4)
    combo_to2 = table.cellWidget(row,5)
    combo_from.clear()
    combo_to.clear()
    combo_from2.clear()
    combo_to2.clear()
    
    
    
    #Sets the value of the compartments based on the selected algorithm
    #if isinstance(sel, QComboBox):
    
    selectedProc = combo_proc.currentText()
    selectedAlg = combo_alg.currentText()
    #hrugroups = [x.strip() for x in self.dlg.txt_defhru.toPlainText().split(',')]
    #combo_from.addItems(hrugroups)
    
    #if selectedAlg == 'RAVEN_DEFAULT':
        #combo_from.addItems(tmpanyCompartment)
        #combo_to.addItems(tmpanyCompartment)#
    if selectedAlg in precipalg and selectedProc == 'Precipitation':
        combo_from.addItems(fromPrecip)
        combo_to.addItems(toPrecip)
    elif selectedAlg in canopevapAlg:
        combo_from.addItems(fromCanevp)
        combo_to.addItems(toCanevp)
    elif selectedAlg in canopysublimationAlg:
        combo_from.addItems(fromCanopySublimation)
        combo_to.addItems(toCanopySublimation)
    elif selectedAlg in soilevapAlg:
        combo_from.addItems(fromSoilevap)
        combo_to.addItems(toSoilevap) 
    elif selectedAlg in lakeevapAlg:
        combo_from.addItems(tmpanyCompartment)
        combo_to.addItems(toLakeevap)
    elif selectedAlg in openwaterevapAlg:
        combo_from.addItems(fromOpenwaterevap)
        combo_to.addItems(toOpenwaterevap)
    elif selectedAlg in infiltrationAlg:
        if selectedAlg =='INF_UBC':
            combo_from.addItems(fromInfiltration)
            combo_to.addItems(toInfiltUBC)
        elif selectedAlg =='INF_HMETS':
            combo_from.addItems(fromInfiltration)
            combo_to.addItems(toInfiltHMETS)
        elif selectedAlg =='INF_GA_SIMPLE':
            combo_from.addItems(fromInfiltGAsimple)
            combo_to.addItems(toInfiltGAsimple)
        else:
            combo_from.addItems(fromInfiltration)
            combo_to.addItems(toInfiltration)
    elif selectedAlg in rechargeAlg and selectedProc == 'Recharge':
        combo_from.addItems(fromRecharge)
        combo_to.addItems(toRecharge)
    elif selectedAlg in percolationAlg:
        combo_from.addItems(fromPercolation)
        combo_to.addItems(toPercolation)
    elif selectedAlg in cappilaryriseAlg:
        combo_from.addItems(fromCapillaryRise)
        combo_to.addItems(toCapillaryRise)
    elif selectedAlg in baseflowAlg:
        combo_from.addItems(fromBaseflow)
        combo_to.addItems(toBaseflow)
    elif selectedAlg in interflowAlg:
        combo_from.addItems(fromInterflow)
        combo_to.addItems(toInterflow)
    elif selectedAlg in seepageAlg:
        combo_from.addItems(fromSeepage)
        combo_to.addItems(toSeepage)
    elif selectedAlg in depresoverflowAlg:
        combo_from.addItems(fromDepressOverflow)
        combo_to.addItems(toDepressOverflow)
    elif selectedAlg in lakereleaseAlg:
        combo_from.addItems(fromLakeRelease)
        combo_to.addItems(toLakeRelease)
    elif selectedAlg in abstractionAlg:
        if selectedAlg == 'ABST_PDMROF':
            combo_from.addItems(fromAbstraction)
            combo_to.addItems(toAbstractionPDMROF)
        else:
            combo_from.addItems(fromAbstraction)
            combo_to.addItems(toAbstraction)
    elif selectedAlg in snowbalanceAlg:
        if selectedAlg == 'SNOBAL_SIMPLE_MELT':
            combo_from.addItems(fromSnowbalSimple)
            combo_to.addItems(toSnowbalSimple)
        elif selectedAlg == 'SNOBAL_COLD_CONTENT':
            combo_from.addItems(fromSnowbalColdcontent)
            combo_to.addItems(toSnowbalColdcontent)
        elif selectedAlg == 'SNOBAL_HBV':
            combo_from.addItems(fromSnowbalHBV)
            combo_to.addItems(toSnowbalHBV)
        elif selectedAlg == 'SNOBAL_TWO_LAYER':
            combo_from.addItems(fromSnowbaltwolayer)
            combo_to.addItems(toSnowbaltwolayer)
        elif selectedAlg == 'SNOBAL_CEMA_NEIGE':
            combo_from.addItems(fromSnowbalCema)
            combo_to.addItems(toSnowbalCema)
        elif selectedAlg == 'SNOBAL_GAWSER':
            combo_from.addItems(fromSnowbalGawser)
            combo_to.addItems(toSnowbalGawser)
        elif selectedAlg == 'SNOBAL_HMETS':
            combo_from.addItems(fromSnowbalHMETS)
            combo_to.addItems(toSnowbalHMETS)
        elif selectedAlg == 'SNOBAL_UBCWM':
            combo_from.addItems(fromSnowbalUBCWM)
            combo_to.addItems(toSnowbalUBCWM)
    elif selectedAlg in snowtempevolveAlg:
        combo_from.addItems(fromSnowtempEvolve)
        combo_to.addItems(toSnowtempEvolve)
    elif selectedAlg in snowmeltAlg:
        combo_from.addItems(fromSnowmelt)
        combo_to.addItems(toSnowmelt)
    elif selectedAlg in snowrefreezeAlg:
        combo_from.addItems(fromSnowrefreeze)
        combo_to.addItems(tmpanyCompartment)
    elif selectedAlg in snowsqueezeAlg:
        combo_from.addItems(fromSnowsqueeze)
        combo_to.addItems(tmpanyCompartment)
    elif selectedAlg in blowingsnowAlg:
        combo_from.addItems(fromBlowingsnow)
        combo_to.addItems(toBlowingsnow)
    elif selectedAlg in snowalbedoevolveAlg:
        if selectedAlg == 'SNOALB_BAKER':
            combo_from.addItems(fromSnowalbevoBaker)
            combo_to.addItems(toSnowalbevoBaker)
        else:
            combo_from.addItems(fromSnowalbevo)
            combo_to.addItems(toSnowalbevo)
    elif selectedAlg in sublimationAlg:
        combo_from.addItems(fromSublimation)
        combo_to.addItems(toSublimation)
    elif selectedAlg in canopydripAlg:
        combo_from.addItems(fromCanopydrip)
        combo_to.addItems(toCanopydrip)
    elif selectedAlg in glaciermeltAlg:
        combo_from.addItems(fromGlaciermelt)
        if selectedAlg == 'GMELT_UBC':
            combo_to.addItems(toGlaciermeltUBC)
        else:
            combo_to.addItems(toGlaciermelt)
    elif selectedAlg in glacierreleaseAlg:
        combo_from.addItems(fromGlacierRelease)
        combo_to.addItems(toGlacierRelease)
    elif selectedAlg in glacierinfiltrationAlg:
        combo_from.addItems(fromGlacierInfiltration)
        combo_to.addItems(toGlacierInfiltration)
    elif selectedAlg in exchangeflowAlg and selectedProc == 'ExchangeFlow':
        combo_from.addItems(fromExchangeflow)
        combo_to.addItems(toExchangeflow)
    elif selectedAlg in convolutionAlg:
        combo_from.addItems(fromConvolution)
        combo_to.addItems(tmpanyCompartment)
    elif selectedAlg in cropheatunitevAlg:
        combo_from.addItems(fromCropheatunit)
        combo_to.addItems(toCropheatunit)
    elif selectedProc == 'RedirectFlow':
        #fromredirectflow = self.dlg.table_hydroprocess.cellWidget(widgetRow-1,2).currentText()
        #toredirectflow = self.dlg.table_hydroprocess.cellWidget(widgetRow-1,3).currentText()
        combo_from.addItems(tmpanyCompartment)
        combo_to.addItems(tmpanyCompartment) 
    elif selectedProc == 'LateralFlush':
            hrugroups = [x.strip() for x in self.dlg.txt_defhru.toPlainText().split(',')]
            combo_from2.addItem('')
            combo_to2.addItem('')
            combo_from2.addItems(statevariables)
            combo_to2.addItems(statevariables)
            if hrugroups[0] !='':
                combo_from.addItems(hrugroups)
                combo_to.addItems(hrugroups)
            else:
                combo_from.addItem('HRUs undefined')
                combo_to.addItem('HRUs undefined')
            
    elif selectedProc == 'Flush' or selectedProc == "Overflow" or selectedProc == 'Split' or selectedProc == 'LateralEquilibrate':
        if selectedProc == 'LateralEquilibrate':
            tmpanyCompartment.append('AllHRUs')
        elif selectedProc == 'Split':
            combo_to2.addItems(tmpanyCompartment)
        combo_from.addItems(tmpanyCompartment)
        combo_to.addItems(tmpanyCompartment)
    # table.setCellWidget(row, 2, combo_from) #Set the combobox for the from compartment
    # table.setCellWidget(row, 3, combo_to)   #Set the combobox for the to compartment
    table.resizeColumnsToContents()   #Resizes automatically the columns
    
            
def enableConditionalProc(self,row):
    
    basedtype = ['HRU_TYPE','HRU_GROUP','LAND_CLASS','VEGETATION']
    comparison = ['IS', 'IS_NOT']
    
    table = self.dlg.table_hydroprocess
  
    chk_isConditional = table.cellWidget(row, 6)
    combo_basedtype = table.cellWidget(row, 7)
    combo_comparison = table.cellWidget(row, 8)
    txt_hrutype = table.cellWidget(row, 9)

    combo_basedtype.clear()
    combo_comparison.clear()
    txt_hrutype.clear()
    if chk_isConditional.isChecked():
        combo_basedtype.addItems(basedtype)
        combo_basedtype.setEnabled(True)
        combo_comparison.addItems(comparison)
        combo_comparison.setEnabled(True)
        txt_hrutype.setEnabled(True)
    else:
        combo_basedtype.setEnabled(False)
        combo_comparison.setEnabled(False)
        txt_hrutype.setEnabled(False)
    table.resizeColumnsToContents() #Resizes the width of the column automatically

def enableMixingRate(self, row):
    table = self.dlg.table_hydroprocess
    # currentWidget = self.dlg.sender()
    # index = self.dlg.table_hydroprocess.indexAt(currentWidget.pos())
    # widgetRow = index.row()
    chk_mixingrate = table.cellWidget(row, 10)
    spin_pct = table.cellWidget(row, 11)
    
    spin_pct.setSingleStep(0.1)
    spin_pct.setMaximum(1.0)
    spin_pct.setMinimum(0.0)
    spin_pct.setDecimals(1)
    
    if chk_mixingrate.isChecked():
        spin_pct.setEnabled(True)
    else:
        spin_pct.setEnabled(False)
    #table.setCellWidget(row, 9, spin_pct)


#This method creates a list with all the hydrologic processes, which is then used to write them into the rvi file
def getHydroProcess(self):
    table = self.dlg.table_hydroprocess
    rows = table.rowCount()
    cols = table.columnCount()
    processesList = []
    for row in range(rows):
        for col in range(cols):
            currentWidget = table.cellWidget(row,col)
            if isinstance(currentWidget, QComboBox):
                if col == 3:
                    if currentWidget.currentText() != '':   #It is lateralflush and requires "To" keyword 
                        processesList.append(currentWidget.currentText()+' To ')
                else:             
                    processesList.append(currentWidget.currentText())
            elif isinstance(currentWidget, QCheckBox):
                if currentWidget.isChecked():
                    if col == 6:
                        processesList.append('condTrue')    #The checkbox is Conditional
                    elif col == 10:
                        processesList.append('mixTrue') #The checkbox is Mixing rate
                    elif col == 12:
                        #processesList.append('interbasinTrue')  #The checkbox is Interbasin
                        processesList.insert(-5,'interbasinTrue')
                else:
                    processesList.append('False')
            elif isinstance(currentWidget, QLineEdit):
                processesList.append(currentWidget.text().upper())
            elif isinstance(currentWidget, QDoubleSpinBox):
                if table.cellWidget(row,10).isChecked() or table.cellWidget(row,0).currentText() == 'LateralEquilibrate':
                    #processesList.append("{:.1f}".format(currentWidget.value()))
                    processesList.insert(-5,"{:.1f}".format(currentWidget.value()))
                else:
                    processesList.append('')
        processesList.append("NewLine")
    return processesList


#List that contains every process name
procname = ['','Baseflow','CanopyEvaporation','CanopyDrip','Infiltration',
            'Percolation','SnowMelt','SoilEvaporation','SnowBalance',
            'Sublimation','OpenWaterEvaporation','Precipitation','Interflow',
            'SnowRefreeze','Flush','CapillaryRise','LakeEvaporation','SnowSqueeze',
            'GlacierMelt','GlacierRelease','CanopySublimation',
            'Overflow','SnowAlbedoEvolve','CropHeatUnitEvolve','Abstraction','GlacierInfiltration',
            'Split','Convolve','SnowTempEvolve','DepressionOverflow','ExchangeFlow',
            'LateralFlush','Seepage','Recharge','BlowingSnow','LakeRelease','SoilBalance','LateralEquilibrate','RedirectFlow'
           ]
procname.sort() #Sorts the list ascending

#Lists with all of the Raven algorithms
baseflowAlg = ['BASE_VIC','BASE_TOPMODEL','BASE_LINEAR','BASE_LINEAR_CONSTRAIN',
               'BASE_LINEAR_ANALYTIC','BASE_POWER_LAW','BASE_CONSTANT',
               'BASE_THRESH_POWER','BASE_THRESH_STOR','BASE_GR4J'
              ]
canopevapAlg = ['CANEVP_RUTTER','CANEVP_MAXIMUM','CANEVP_ALL']
canopydripAlg = ['CANDRIP_RUTTER','CANDRIP_SLOWDRAIN']
infiltrationAlg = ['INF_GREEN_AMPT','INF_GA_SIMPLE','INF_VIC_ARNO','INF_VIC',
                   'INF_RATIONAL','INF_PRMS','INF_HBV','INF_UBC','INF_PARTITION',
                   'INF_GR4J','INF_SCS','INF_SCS_NOABSTRACTION','INF_HMETS',
                   'INF_ALL_INFILTRATES','INF_XINANXIANG','INF_PDM','INF_AWBM'
                  ]
percolationAlg = ['PERC_POWER_LAW','POWER_LAW','PERC_GAWSER','PERC_GAWSER_CONSTRAIN',
                  'PERC_PRMS','PERC_SACRAMENTO','PERC_CONSTANT','PERC_LINEAR',
                  'PERC_LINEAR_ANALYTIC','PERC_GR4J','PERC_GR4JEXCH','PERC_GR4JEXCH2','PERC_ASPEN'
                 ]
snowmeltAlg = ['MELT_POTMELT']  #Obsolete
soilevapAlg = ['SOILEVAP_VIC','SOILEVAP_TOPMODEL','SOILEVAP_SEQUEN','SOILEVAP_ROOT',
               'SOILEVAP_ROOT_CONSTRAIN','SOILEVAP_HBV','SOILEVAP_HYPR','SOILEVAP_UBC',
               'SOILEVAP_PDM','SOILEVAP_CHU','SOILEVAP_GR4J','SOILEVAP_LINEAR',
               'SOILEVAP_SACSMA','SOILEVAP_ALL','SOILEVAP_AWBM'
              ]
snowbalanceAlg = ['SNOBAL_COLD_CONTENT','SNOBAL_SIMPLE_MELT','SNOBAL_UBCWM',
                  'SNOBAL_HBV','SNOBAL_CEMA_NEIGE','SNOBAL_TWO_LAYER',
                  'SNOBAL_GAWSER','SNOBAL_CRHM_EBSM','SNOBAL_HMETS'
                 ]
sublimationAlg = ['SUBLIM_SVERDRUP','SUBLIM_KUZMIN','SUBLIM_CENTRAL_SIERRA',
                  'SUBLIM_PBSM','SUBLIM_KUCHMENT_GELFAN','SUBLIM_BULK_AERO'
                 ]
openwaterevapAlg = ['OPEN_WATER_EVAP','OPEN_WATER_RIPARIAN','OPEN_WATER_UWFS']
precipalg = ['PRECIP_RAVEN','RAVEN_DEFAULT']
interflowAlg = ['PRMS']
snowrefreezeAlg = ['FREEZE_DEGREE_DAY']
flushAlg = ['FLUSH_RAVEN','RAVEN_DEFAULT']
cappilaryriseAlg = ['CRISE_HBV']
lakeevapAlg = ['BASIC','LAKE_EVAP_BASIC']
snowsqueezeAlg = ['SQUEEZE_RAVEN']  #:SnowSqueeze SQUEEZE_RAVEN SNOW_LIQ [state_var to_index]
glaciermeltAlg = ['GMELT_HBV','GMELT_UBC','GMELT_SIMPLE_MELT']
glacierreleaseAlg = ['GRELEASE_HBV_EC','LINEAR_STORAGE','GRELEASE_LINEAR','GRELEASE_LINEAR_ANALYTIC']
canopysublimationAlg = ['SUBLIM_ALL','SUBLIM_MAXIMUM','SUBLIM_SVERDRUP',
                        'SUBLIM_KUZMIN','SUBLIM_CENTRAL_SIERRA','SUBLIM_PBSM',
                        'SUBLIM_KUCHMENT_GELFAN','SUBLIM_BULK_AERO'
                       ]
overflowAlg = ['OVERFLOW_RAVEN','RAVEN_DEFAULT']
snowalbedoevolveAlg = ['SNOALB_UBCWM','SNOALB_CRHM_ESSERY','SNOALB_BAKER']
cropheatunitevAlg = ['CHU_ONTARIO']
abstractionAlg = ['ABST_SCS','ABST_PERCENTAGE','ABST_FILL',
                  'ABST_PDMROF','ABST_UWFS'
                 ]  #:Abstraction [string method] PONDED_WATER DEPRESSION/MULTIPLE
glacierinfiltrationAlg = ["GINFIL_UBCWM"] 
splitAlg = ['RAVEN_DEFAULT']
convolutionAlg = ['CONVOL_GR4J_1','CONVOL_GR4J_2','CONVOL_GAMMA','CONVOL_GAMMA_2']
snowtempevolveAlg = ['SNOTEMP_NEWTONS']
depresoverflowAlg = ['DFLOW_THRESHPOW','DFLOW_LINEAR','DFLOW_WEIR']
exchangeflowAlg = ['RAVEN_DEFAULT']#:ExchangeFlow RAVEN_DEFAULT [state_var from] [state_var mixing_zone]
lateralflushAlg = ['RAVEN_DEFAULT'] #Interbasin
seepageAlg = ['SEEP_LINEAR']
rechargeAlg = ['RECHARGE_CONSTANT','RECHARGE_FROMFILE','RAVEN_DEFAULT',
               'RECHARGE_CONSTANT_OVERLAP','RECHARGE_DATA','RECHARGE_FLUX'
              ] #:Recharge RECHARGE_FROMFILE ATMOS_PRECIP SOIL[?]
blowingsnowAlg = ['PBSM']   #:BlowingSnow PBSM MULTIPLE MULTIPLE
lakereleaseAlg = ['LAKEREL_LINEAR']
soilbalanceAlg = ['SOILBAL_SACSMA'] #:SoilBalance SOILBAL_SACSMA MULTIPLE MULTIPLE
lateralequilibrateAlg = ['RAVEN_DEFAULT']   #Interbasin

#Lists of the compartments of each algorithm. Can easily add new compartments if new compartments are added in Raven
#Empty brackets = any soil or any convolution
fromPrecip = ["ATMOS_PRECIP","COLD_CONTENT", "SNOW_DEPTH"]
toPrecip = ["SNOW","PONDED_WATER","DEPRESSION","WETLAND","CANOPY","CANOPY_SNOW",
            "SURFACE_WATER", "ATMOSPHERE","SNOW_LIQ","SNOW_DEFICIT","NEW_SNOW",
            "COLD_CONTENT","SNOW_DEPTH","MULTIPLE",''
           ]
fromCanevp = ["CANOPY",'']
toCanevp = ["ATMOSPHERE",'']
fromCanopySublimation = ['CANOPY_SNOW','']
toCanopySublimation = ['ATMOSPHERE','']
fromSoilevap = ["SOIL[0]",'MULTIPLE','']
toSoilevap = ["ATMOSPHERE",'']
toLakeevap = ["ATMOSPHERE",'']
fromOpenwaterevap = ["DEPRESSION",'']
toOpenwaterevap = ["ATMOSPHERE",'']
fromInfiltration = ["PONDED_WATER","MULTIPLE",'']
toInfiltration = ["SOIL[0]","SURFACE_WATER","MULTIPLE",''] 
toInfiltUBC = ["SOIL[0]","SOIL[1]","SOIL[2]","SOIL[3]","SURFACE_WATER","MULTIPLE",'']
toInfiltHMETS = ["SOIL[0]","CONVOLUTION[0]","CONVOLUTION[1]",'MULTIPLE','']
fromInfiltGAsimple = ["PONDED_WATER","GA_MOISTURE_INIT",'']
toInfiltGAsimple = ["SOIL[0]","SURFACE_WATER","GA_MOISTURE_INIT","MULTIPLE",'']
fromPercolation = []
toPercolation = []
fromCapillaryRise = []
toCapillaryRise = []
fromBaseflow = []
toBaseflow = ['SURFACE_WATER','']
fromRecharge = ['ATMOS_PRECIP','']  #Need to check for other algorithms
toRecharge = []
fromSnowsqueeze = ["SNOW_LIQ",'']
toSnowsqueeze = []
fromInterflow = []
toInterflow = ['SURFACE_WATER','']
fromSeepage = ['DEPRESSION','']
toSeepage = []
fromDepressOverflow = ['DEPRESSION','']
toDepressOverflow = ['SURFACE_WATER','']
fromLakeRelease = ['LAKE_STORAGE','SURFACE_WATER','']      #!!!! THIS ONE IS INCORRECT
toLakeRelease = ['SURFACE_WATER','']
fromAbstraction = ['PONDED_WATER','']
toAbstraction = ['DEPRESSION']
toAbstractionPDMROF = ['DEPRESSION','SURFACE_WATER','']
fromSnowmelt = ['SNOW','']
toSnowmelt = ['PONDED_WATER','']
fromSnowrefreeze = ['SNOW_LIQ','']
fromSnowbalSimple = ['SNOW','']
toSnowbalSimple = ['PONDED_WATER','SNOW_LIQ','']
fromSnowbalColdcontent = ['SNOW','SNOW_LIQ',"COLD_CONTENT","ENERGY_LOSSES","MULTIPLE",'']
toSnowbalColdcontent = ['SNOW','SNOW_LIQ','SURFACE_WATER',"COLD_CONTENT","ENERGY_LOSSES","MULTIPLE",'']
fromSnowbalHBV = ['SNOW','SNOW_LIQ',"MULTIPLE",'']
toSnowbalHBV = ['SNOW_LIQ','SOIL[0]',"MULTIPLE",'']
fromSnowbaltwolayer = ['NEW_SNOW','PONDED_WATER','SNOW','SNOW_LIQ[0]','SNOW_LIQ[1]','COLD_CONTENT[0]','COLD_CONTENT[1]','SNOW_TEMP','CUM_SNOWMELT',"MULTIPLE",'']
toSnowbaltwolayer = ['SNOW','SNOW_LIQ[0]','SNOW_LIQ[1]','PONDED_WATER','COLD_CONTENT[0]','COLD_CONTENT[1]','SNOW_TEMP','CUM_SNOWMELT',"MULTIPLE",'']
fromSnowbalCema = ['SNOW','SNOW_COVER',"MULTIPLE",'']
toSnowbalCema = ['PONDED_WATER','SNOW_COVER',"MULTIPLE",'']
fromSnowbalGawser = ['SNOW','SNOW_LIQ','COLD_CONTENT',"MULTIPLE",'']
toSnowbalGawser = ['SNOW','SNOW_LIQ','COLD_CONTENT','PONDED_WATER',"MULTIPLE",'']
fromSnowbalUBCWM = ['SNOW','SNOW_LIQ','COLD_CONTENT','SNOW_COVER','CUM_SNOWMELT','SNOW_DEFICIT','MULTIPLE','']
toSnowbalUBCWM = ['SNOW','SNOW_LIQ','PONDED_WATER','COLD_CONTENT','SNOW_COVER','CUM_SNOWMELT','SNOW_DEFICIT','MULTIPLE','']
fromSnowbalHMETS = ['SNOW','SNOW_LIQ','CUM_SNOWMELT','MULTIPLE','']
toSnowbalHMETS = ['SNOW_LIQ','MULTIPLE','']
fromSnowbalCRHM = ['SNOW','SNOW_LIQ','COLD_CONTENT',"MULTIPLE",'']
toSnowbalCRHM = ['SNOW','SNOW_LIQ','CUM_SNOWMELT','PONDED_WATER',"MULTIPLE",'']
fromSnowtempEvolve = ['SNOW_TEMP','']
toSnowtempEvolve = ['SNOW_TEMP','']
fromBlowingsnow = ['SNOW','SNOW_AGE','SNOW_DEPTH','SNODRIFT_TEMP','SNOW_LIQ','']
toBlowingsnow = ['SNOW_AGE','SNOW_DEPTH','SNOW_DRIFT','SNODRIFT_TEMP','ATMOSPHERE','']
fromSublimation = ['SNOW','']
toSublimation = ['ATMOSPHERE','']
fromSnowalbevo = ['SNOW_ALBEDO','']
toSnowalbevo = ['SNOW_ALBEDO','']
fromSnowalbevoBaker = ['SNOW_ALBEDO','SNOW_AGE','']
toSnowalbevoBaker = ['SNOW_ALBEDO','SNOW_AGE','']
fromCanopydrip = ['CANOPY','']
toCanopydrip = ['PONDED_WATER','']
fromGlaciermelt = ['GLACIER_ICE','']
toGlaciermelt = ['GLACIER','']
toGlaciermeltUBC = ['GLACIER','PONDED_WATER','']   #Ponded water is not in the .dat file, but is in the template and raven source code
fromGlacierInfiltration = ['PONDED_WATER','']
toGlacierInfiltration = ['GLACIER','SOIL[2]','SOIL[3]','MULTIPLE','']
fromGlacierRelease = ['GLACIER','']
toGlacierRelease = ['SURFACE_WATER','']
fromExchangeflow = [] 
toExchangeflow = []
fromConvolution = []
fromCropheatunit = ['CROP_HEAT_UNIT','']
toCropheatunit = ['CROP_HEAT_UNIT','']
statevariables = ['SURFACE_WATER','ATMOSPHERE','ATMOS_PRECIP','PONDED_WATER','SOIL','GROUNDWATER',
                  'CANOPY','CANOPY_SNOW','TRUNK','ROOT','DEPRESSION','WETLAND','LAKE_STORAGE','SNOW',
                  'SNOW_LIQ','GLACIER','GLACIER_ICE']
statevariables.sort()

anyCompartment = list(set().union(
                                  fromPrecip,toPrecip,fromCanevp,toCanevp,fromSoilevap,toSoilevap,
                                  toLakeevap,fromOpenwaterevap,toOpenwaterevap,fromInfiltration,toInfiltration,
                                  toInfiltUBC,toInfiltHMETS,fromInfiltGAsimple,toInfiltGAsimple,toBaseflow,fromRecharge,
                                  fromSnowsqueeze,toInterflow,fromSeepage,fromDepressOverflow,toDepressOverflow,
                                  fromLakeRelease,toLakeRelease,fromAbstraction,toAbstraction,toAbstractionPDMROF,fromSnowmelt,
                                  toSnowmelt,fromSnowrefreeze,fromSnowbalSimple,toSnowbalSimple,fromSnowbalColdcontent,toSnowbalColdcontent,
                                  fromSnowbalHBV,toSnowbalHBV,fromSnowbaltwolayer,toSnowbaltwolayer,fromSnowbalCema,
                                  toSnowbalCema,fromSnowbalGawser,toSnowbalGawser,fromSnowbalUBCWM,toSnowbalUBCWM,fromSnowbalHMETS,
                                  toSnowbalHMETS,fromSnowbalCRHM,toSnowbalCRHM,fromSnowtempEvolve,toSnowtempEvolve,
                                  fromBlowingsnow,toBlowingsnow,fromSublimation,toSublimation,fromSnowalbevo,toSnowalbevo,
                                  fromSnowalbevoBaker,toSnowalbevoBaker,fromCanopydrip,toCanopydrip,fromGlaciermelt,toGlaciermelt,
                                  fromGlacierInfiltration,toGlacierInfiltration,fromGlacierRelease,toGlacierRelease,
                                  fromCropheatunit,toCropheatunit
                                  ))