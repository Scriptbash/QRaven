from PyQt5.QtCore import QDateTime
#This method reset the RVI section to the default values
def partialReset(self):
    table = self.dlg.table_hydroprocess #Get the hydrological processes table
    #Deletes all the table rows
    while(table.rowCount()>0):
        table.removeRow(0)
    #Revert back all the RVI options to the default values
    self.dlg.combo_soilmod.setCurrentText("SOIL_ONE_LAYER")
    self.dlg.spin_soilmod.setValue(0)
    self.dlg.combo_catchment.setCurrentText("ROUTE_DUMP")
    self.dlg.combo_routing.setCurrentText("ROUTE_DIFFUSIVE_WAVE")
    self.dlg.combo_evapo.setCurrentText("PET_HARGREAVES_1985")

    self.dlg.combo_method.setCurrentText("")
    self.dlg.combo_interpo.setCurrentText("")
    self.dlg.combo_rainsnowfrac.setCurrentText("")
    self.dlg.combo_owevapo.setCurrentText("")
    self.dlg.combo_oroprecip.setCurrentText("")
    self.dlg.combo_orotemp.setCurrentText("")
    self.dlg.combo_oropet.setCurrentText("")
    self.dlg.combo_cloudcover.setCurrentText("")
    self.dlg.combo_airpressure.setCurrentText("")
    self.dlg.combo_potentialmelt.setCurrentText("")
    self.dlg.combo_monthlyinterpo.setCurrentText("")
    self.dlg.combo_lakestorage.setCurrentText("")
    self.dlg.txt_interpofile.clear()
    self.dlg.txt_interpofile.setEnabled(False)
    self.dlg.combo_swradation.setCurrentText("")
    self.dlg.combo_swcanopy.setCurrentText("")
    self.dlg.combo_swcloud.setCurrentText("")
    self.dlg.combo_lwradation.setCurrentText("")
    self.dlg.combo_windspeed.setCurrentText("")
    self.dlg.combo_relhumidity.setCurrentText("")
    self.dlg.combo_precipicept.setCurrentText("")
    self.dlg.combo_recharge.setCurrentText("")
    self.dlg.combo_subdaily.setCurrentText("")
    self.dlg.combo_calendar.setCurrentText("")
    self.dlg.chk_directevapo.setChecked(False)
    self.dlg.chk_snowsuppressespet.setChecked(False)
    self.dlg.chk_suppresscomppet.setChecked(False)
    self.dlg.chk_snaphydro.setChecked(False)

def fullReset(self):
    partialReset(self)
    self.dlg.file_rvioutputdir.setFilePath('')
    self.dlg.txt_modname.clear()
    time = QDateTime.fromString('2000/01/01 00:00:00', 'yyyy/MM/dd hh:mm:ss')
    self.dlg.date_startdate.setDateTime(time)
    self.dlg.date_enddate.setDateTime(time)
    self.dlg.chk_duration.setCheckState(False)
    self.dlg.spin_duration.setValue(0)
    self.dlg.spin_timestep_h.setValue(0)
    self.dlg.spin_timestep_m.setValue(0)
    self.dlg.spin_timestep_s.setValue(0)
    self.dlg.txt_defhru.clear()
    self.dlg.chk_disablehru.setCheckState(False)
    self.dlg.txt_disablehru.clear()
    self.dlg.chk_chunksize.setCheckState(False)
    self.dlg.spin_chunksize.setValue(0)
    self.dlg.chk_outputdir.setCheckState(False)
    self.dlg.file_outputdir.setFilePath('')
    self.dlg.chk_outputdump.setCheckState(False)
    self.dlg.date_outputdump.setDateTime(time)
    self.dlg.chk_outputinterval.setCheckState(False)
    self.dlg.spin_outinterval.setValue(0.00)
    self.dlg.chk_readlivefile.setCheckState(False)
    self.dlg.spin_readlivefile.setValue(0)
    self.dlg.chk_reservoirdemandalloc.setCheckState(False)
    self.dlg.chk_runname.setCheckState(False)
    self.dlg.txt_runname.clear()
    self.dlg.chk_rvcfilename.setCheckState(False)
    self.dlg.txt_rvcfilename.clear()
    self.dlg.chk_rvhfilename.setCheckState(False)
    self.dlg.txt_rvhfilename.clear()
    self.dlg.chk_rvpfilename.setCheckState(False)
    self.dlg.txt_rvpfilename.clear()
    self.dlg.chk_rvtfilename.setCheckState(False)
    self.dlg.txt_rvtfilename.clear()
    self.dlg.chk_wateryear.setCheckState(False)
    self.dlg.spin_wateryear.setValue(1)
    self.dlg.chk_assimilatestreamflow.setCheckState(False)
    self.dlg.chk_silentmode.setCheckState(False)
    self.dlg.chk_writeensim.setCheckState(False)
    self.dlg.chk_assimilatereservstage.setCheckState(False)
    self.dlg.chk_suppressoutput.setCheckState(False)
    self.dlg.chk_writeexausmb.setCheckState(False)
    self.dlg.chk_rvptemplate.setCheckState(False)
    self.dlg.chk_snaphydro.setCheckState(False)
    self.dlg.chk_writeforcingfunc.setCheckState(False)
    self.dlg.chk_debugmode.setCheckState(False)
    self.dlg.chk_usestopfile.setCheckState(False)
    self.dlg.chk_writemassbal.setCheckState(False)
    self.dlg.chk_endpause.setCheckState(False)
    self.dlg.chk_writedemand.setCheckState(False)
    self.dlg.chk_writemassloadings.setCheckState(False)
    self.dlg.chk_noisymode.setCheckState(False)
    self.dlg.chk_writeenergy.setCheckState(False)
    self.dlg.list_evalmetrics.clearSelection()
    transportTable = self.dlg.table_transport
    while(transportTable.rowCount()>0):
        transportTable.removeRow(0)
    customoutputs = self.dlg.table_customoutputs
    while(customoutputs.rowCount()>0):
        customoutputs.removeRow(0)


