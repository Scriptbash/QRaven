#This method reset the RVI section to the default values
def resetGUI(self):
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