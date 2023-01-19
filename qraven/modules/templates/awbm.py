from ..hydrologicproc import addprocess
#This method loads a AWBM template into the GUI
def loadAwbm(self):
    try:
        table = self.dlg.table_hydroprocess #Get the hydrological processes table

        #Sets the model parameters 
        self.dlg.combo_method.setCurrentText("ORDERED_SERIES")
        self.dlg.combo_routing.setCurrentText("ROUTE_NONE")
        self.dlg.combo_catchment.setCurrentText("ROUTE_DUMP")

        self.dlg.combo_evapo.setCurrentText("PET_HAMON")
        self.dlg.combo_rainsnowfrac.setCurrentText("RAINSNOW_THRESHOLD")
        self.dlg.combo_potentialmelt.setCurrentText("POTMELT_DEGREE_DAY")
        self.dlg.combo_precipicept.setCurrentText("PRECIP_ICEPT_NONE")
        self.dlg.combo_cloudcover.setCurrentText("CLOUDCOV_NONE")
        self.dlg.combo_lwradation.setCurrentText("LW_RAD_NONE")
        self.dlg.combo_swradation.setCurrentText("SW_RAD_NONE")

        self.dlg.combo_soilmod.setCurrentText("SOIL_MULTILAYER")
        self.dlg.spin_soilmod.setValue(4)

        #Sets the hydrological processes
        for i in range(5):
            addprocess(self)

        combo_proc = table.cellWidget(0,0)
        combo_proc.setCurrentText("Precipitation")
        combo_alg = table.cellWidget(0,1)
        combo_alg.setCurrentText("PRECIP_RAVEN")
        combo_from = table.cellWidget(0,2)
        combo_from.setCurrentText("ATMOS_PRECIP")
        combo_to = table.cellWidget(0,3)
        combo_to.setCurrentText("MULTIPLE")

        combo_proc = table.cellWidget(1,0)
        combo_proc.setCurrentText("SnowBalance")
        combo_alg = table.cellWidget(1,1)
        combo_alg.setCurrentText("SNOBAL_SIMPLE_MELT")
        combo_from = table.cellWidget(1,2)
        combo_from.setCurrentText("SNOW")
        combo_to = table.cellWidget(1,3)
        combo_to.setCurrentText("PONDED_WATER")

        combo_proc = table.cellWidget(2,0)
        combo_proc.setCurrentText("Infiltration")
        combo_alg = table.cellWidget(2,1)
        combo_alg.setCurrentText("INF_ABWM")
        combo_from = table.cellWidget(2,2)
        combo_from.setCurrentText("PONDED_WATER")
        combo_to = table.cellWidget(2,3)
        combo_to.setCurrentText("MULTIPLE")
        
        combo_proc = table.cellWidget(3,0)
        combo_proc.setCurrentText("SoilEvaporation")
        combo_alg = table.cellWidget(3,1)
        combo_alg.setCurrentText("SOILEVAP_ABWM")
        combo_from = table.cellWidget(3,2)
        combo_from.setCurrentText("MULTIPLE")
        combo_to = table.cellWidget(3,3)
        combo_to.setCurrentText("ATMOSPHERE")

        combo_proc = table.cellWidget(4,0)
        combo_proc.setCurrentText("Baseflow")
        combo_alg = table.cellWidget(4,1)
        combo_alg.setCurrentText("BASE_LINEAR")
        combo_from = table.cellWidget(4,2)
        combo_from.setCurrentText("SOIL[3]")
        combo_to = table.cellWidget(4,3)
        combo_to.setCurrentText("SURFACE_WATER")


        table.resizeColumnsToContents() #Resizes the width of the column automatically
        
        print("AWBM template loaded.")
        self.iface.messageBar().pushSuccess("Success", "Loaded AWBM template successfully")
    except Exception as e:
        print('An error occured while loading AWBM template.')
        print(e)  