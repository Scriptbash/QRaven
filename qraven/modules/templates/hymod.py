from ..hydrologicproc import addprocess

#This method loads a template of HYMOD into the GUI
def loadHymod(self):
    try:
        table = self.dlg.table_hydroprocess #Get the hydrological processes table

        #Sets the model parameters 
        self.dlg.combo_method.setCurrentText("ORDERED_SERIES")
        self.dlg.combo_potentialmelt.setCurrentText("POTMELT_DEGREE_DAY")
        self.dlg.combo_rainsnowfrac.setCurrentText("RAINSNOW_THRESHOLD")
        self.dlg.combo_evapo.setCurrentText("PET_HAMON")
        self.dlg.combo_owevapo.setCurrentText("PET_HAMON")
        self.dlg.combo_catchment.setCurrentText("ROUTE_RESERVOIR_SERIES")
        self.dlg.combo_routing.setCurrentText("ROUTE_NONE")
        self.dlg.combo_swradation.setCurrentText("SW_RAD_NONE")
        self.dlg.combo_lwradation.setCurrentText("LW_RAD_NONE")
        self.dlg.combo_cloudcover.setCurrentText("CLOUDCOV_NONE")
        self.dlg.combo_precipicept.setCurrentText("PRECIP_ICEPT_NONE")
        self.dlg.combo_soilmod.setCurrentText("SOIL_TWO_LAYER")

        #Sets the hydrological processes
        for i in range(6):
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
        combo_alg.setCurrentText("INF_PDM")
        combo_from = table.cellWidget(2,2)
        combo_from.setCurrentText("PONDED_WATER")
        combo_to = table.cellWidget(2,3)
        combo_to.setCurrentText("MULTIPLE")

        combo_proc = table.cellWidget(3,0)
        combo_proc.setCurrentText("Flush")
        combo_alg = table.cellWidget(3,1)
        combo_alg.setCurrentText("RAVEN_DEFAULT")
        combo_from = table.cellWidget(3,2)
        combo_from.setCurrentText("SURFACE_WATER")
        combo_to = table.cellWidget(3,3)
        combo_to.setCurrentText("SOIL[1]")
        chk_mixingrate = table.cellWidget(3,8)
        chk_mixingrate.setChecked(True)
        spin_pct = table.cellWidget(3,9)
        spin_pct.setValue(0.5)

        combo_proc = table.cellWidget(4,0)
        combo_proc.setCurrentText("SoilEvaporation")
        combo_alg = table.cellWidget(4,1)
        combo_alg.setCurrentText("SOILEVAP_PDM")
        combo_from = table.cellWidget(4,2)
        combo_from.setCurrentText("SOIL[0]")
        combo_to = table.cellWidget(4,3)
        combo_to.setCurrentText("ATMOSPHERE")

        combo_proc = table.cellWidget(5,0)
        combo_proc.setCurrentText("Baseflow")
        combo_alg = table.cellWidget(5,1)
        combo_alg.setCurrentText("BASE_LINEAR")
        combo_from = table.cellWidget(5,2)
        combo_from.setCurrentText("SOIL[1]")
        combo_to = table.cellWidget(5,3)
        combo_to.setCurrentText("SURFACE_WATER")

        table.resizeColumnsToContents() #Resizes the width of the column automatically
        
        print("HYMOD template loaded.")
        self.iface.messageBar().pushSuccess("Success", "Loaded HYMOD template successfully")
    except Exception as e:
        print('An error occured while loading HYMOD template.')
        print(e)