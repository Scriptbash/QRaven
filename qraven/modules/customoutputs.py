from qgis.PyQt.QtWidgets import *

def addoutput(self):

    table = self.dlg.table_customoutputs #Get the custom outputs table
    currentRow = table.rowCount()   #Get the number of rows the table has
    table.insertRow(currentRow) #Inserts a new row below the last row
    combo_time = QComboBox() 
    combo_stat = QComboBox()
    combo_eval = QComboBox() 
    combo_option = QComboBox()  
    
    combo_variable1 = QComboBox()
    combo_variable1.setEditable(True)
    combo_variable2 = QComboBox()
    combo_variable2.setEditable(True)
    combo_variable2.setEnabled(False)
    
    spin_min = QDoubleSpinBox()
    spin_max = QDoubleSpinBox()
    spin_bin = QDoubleSpinBox()

    txt_filename = QLineEdit()
   
    spin_min.setEnabled(False)
    spin_bin.setEnabled(False)
    spin_max.setEnabled(False)
    #spin_min.setDecimals(1)
    

    timeperiod = ['DAILY','MONTHLY','YEARLY','WATER_YEARLY','CONTINUOUS']
    statistic = ['AVERAGE','MINIMUM','MAXIMUM','RANGE','MEDIAN','QUARTILES','HISTOGRAM']
    evaluation = ['BY_BASIN','BY_HRU','BY_HRU_GROUP','BY_SB_GROUP','ENTIRE_WATERSHED']
    variable = ['','SURFACE_WATER','ATMOSPHERE','ATMOS_PRECIP','PONDED_WATER','GROUNDWATER','CANOPY','CANOPY_SNOW','SNOW',
                'SNOW_LIQ','GLACIER','GLACIER_ICE','CONVOLUTION','SNOW_TEMP','COLD_CONTENT','SOIL_TEMP','CANOPY_TEMP',
                'SURFACE_WATER_TEMP','SNOW_DEPTH','PERMAFROST_DEPTH','SNOW_COVER','SNOW_AGE','SNOW_ALBEDO','CUM_INFIL','CUM_SNOWMELT',
                'CONSTITUENT','PRECIP','SNOW_FRAC','SNOWFALL','RAINFALL','RECHARGE','TEMP_AVE','WIND_VEL','PET','OW_PET','POTENTIAL_MELT',
               ]
    variable.sort()
    option = ['','From:','To:','Between:']

    combo_time.addItems(timeperiod)
    combo_stat.addItems(statistic)
    combo_eval.addItems(evaluation)
    combo_option.addItems(option)
    combo_variable1.addItems(variable)
    combo_variable2.addItems(variable)

    table.setCellWidget(currentRow, 0, combo_time)  #Sets the new combobox in the first column and in the new row
    table.setCellWidget(currentRow, 1, combo_stat)
    table.setCellWidget(currentRow, 2, spin_min)
    table.setCellWidget(currentRow, 3, spin_max)
    table.setCellWidget(currentRow, 4, spin_bin)
    table.setCellWidget(currentRow, 5, combo_option)
    table.setCellWidget(currentRow, 6, combo_variable1)
    table.setCellWidget(currentRow, 7, combo_variable2)
    table.setCellWidget(currentRow, 8, combo_eval)
    table.setCellWidget(currentRow, 9, txt_filename)

    table.resizeColumnsToContents() #Resizes the width of the column automatically

    combo_stat.currentIndexChanged.connect(lambda:toggleHistogram(self,currentRow))
    combo_option.currentIndexChanged.connect(lambda:toggleVariable(self,currentRow))

def removeoutput(self):
    table = self.dlg.table_customoutputs
    selectedRow = table.currentRow()
    table.removeRow(selectedRow)


def toggleHistogram(self,row):
    table = self.dlg.table_customoutputs
    combo_stat = table.cellWidget(row,1)
    spin_min = table.cellWidget(row,2)
    spin_max = table.cellWidget(row,3)
    spin_bin = table.cellWidget(row,4)

    if combo_stat.currentText() == 'HISTOGRAM':
        spin_min.setEnabled(True)
        spin_max.setEnabled(True)
        spin_bin.setEnabled(True)
    else:
        spin_min.setEnabled(False)
        spin_max.setEnabled(False)
        spin_bin.setEnabled(False)
    
def toggleVariable(self,row):
    table = self.dlg.table_customoutputs
    combo_option = table.cellWidget(row,5)
    combo_variable2 = table.cellWidget(row,7)

    if combo_option.currentText() == 'Between:':
        combo_variable2.setEnabled(True)
    else:
        combo_variable2.setEnabled(False)

def getOutputs(self):

    table = self.dlg.table_customoutputs
    rows = table.rowCount()
    cols = table.columnCount()
    outputs = []
    for row in range(rows):
        tmpoutput = []
        for col in range(cols):
            currentWidget = table.cellWidget(row,col)
            if isinstance(currentWidget, QComboBox):
                if currentWidget.isEnabled():
                    if col == 7:
                        tmpoutput.append('.And. ' + currentWidget.currentText())
                    else:
                        tmpoutput.append(currentWidget.currentText())
                else:
                    tmpoutput.append('')
    
            elif isinstance(currentWidget, QDoubleSpinBox):
                if currentWidget.isEnabled():
                    tmpoutput.append("{:.1f}".format(currentWidget.value()))
                else:
                    tmpoutput.append('')
            elif isinstance(currentWidget, QLineEdit):
                if currentWidget.text() !='':
                    tmpoutput.append(currentWidget.text())
                else:
                    tmpoutput.append('')
        outputs.append(tmpoutput) 
    return outputs