from ..hydrologicproc import addprocess

#This method loads a template of HBV-Light into the GUI
def loadHbvlight(self):
    try:
        table = self.dlg.table_hydroprocess #Get the hydrological processes table

        #Sets the model parameters 
        self.dlg.combo_method.setCurrentText("ORDERED_SERIES")
        self.dlg.combo_routing.setCurrentText("ROUTE_NONE")
        self.dlg.combo_catchment.setCurrentText("ROUTE_TRI_CONVOLUTION")
        self.dlg.combo_evapo.setCurrentText("PET_DATA")
        self.dlg.combo_rainsnowfrac.setCurrentText("RAINSNOW_HBV")
        self.dlg.combo_potentialmelt.setCurrentText("POTMELT_DEGREE_DAY")
        self.dlg.combo_orotemp.setCurrentText("OROCORR_HBV")
        self.dlg.combo_oroprecip.setCurrentText("OROCORR_HBV")
        self.dlg.combo_oropet.setCurrentText("OROCORR_HBV")
        self.dlg.combo_cloudcover.setCurrentText("CLOUDCOV_NONE")
        self.dlg.combo_precipicept.setCurrentText("PRECIP_ICEPT_USER")

        self.dlg.combo_soilmod.setCurrentText("SOIL_MULTILAYER")
        self.dlg.spin_soilmod.setValue(3)

        #Sets the hydrological processes
        for i in range(12):
            addprocess(self)
        
        combo_proc = table.cellWidget(0,0)
        combo_proc.setCurrentText("SnowRefreeze")
        combo_alg = table.cellWidget(0,1)
        combo_alg.setCurrentText("FREEZE_DEGREE_DAY")
        combo_from = table.cellWidget(0,2)
        combo_from.setCurrentText("SNOW_LIQ")
        combo_to = table.cellWidget(0,4)
        combo_to.setCurrentText("SNOW")
    
        combo_proc = table.cellWidget(1,0)
        combo_proc.setCurrentText("Precipitation")
        combo_alg = table.cellWidget(1,1)
        combo_alg.setCurrentText("PRECIP_RAVEN")
        combo_from = table.cellWidget(1,2)
        combo_from.setCurrentText("ATMOS_PRECIP")
        combo_to = table.cellWidget(1,4)
        combo_to.setCurrentText("MULTIPLE")

        combo_proc = table.cellWidget(2,0)
        combo_proc.setCurrentText("SnowBalance")
        combo_alg = table.cellWidget(2,1)
        combo_alg.setCurrentText("SNOBAL_SIMPLE_MELT")
        combo_from = table.cellWidget(2,2)
        combo_from.setCurrentText("SNOW")
        combo_to = table.cellWidget(2,4)
        combo_to.setCurrentText("SNOW_LIQ")

        combo_proc = table.cellWidget(3,0)
        combo_proc.setCurrentText("Overflow")
        combo_alg = table.cellWidget(3,1)
        combo_alg.setCurrentText("RAVEN_DEFAULT")
        combo_from = table.cellWidget(3,2)
        combo_from.setCurrentText("SNOW_LIQ")
        combo_to = table.cellWidget(3,4)
        combo_to.setCurrentText("PONDED_WATER")

        combo_proc = table.cellWidget(4,0)
        combo_proc.setCurrentText("Infiltration")
        combo_alg = table.cellWidget(4,1)
        combo_alg.setCurrentText("INF_HBV")
        combo_from = table.cellWidget(4,2)
        combo_from.setCurrentText("PONDED_WATER")
        combo_to = table.cellWidget(4,4)
        combo_to.setCurrentText("MULTIPLE")

        combo_proc = table.cellWidget(5,0)
        combo_proc.setCurrentText("Flush")
        combo_alg = table.cellWidget(5,1)
        combo_alg.setCurrentText("RAVEN_DEFAULT")
        combo_from = table.cellWidget(5,2)
        combo_from.setCurrentText("SURFACE_WATER")
        combo_to = table.cellWidget(5,4)
        combo_to.setCurrentText("SOIL[1]")

        combo_proc = table.cellWidget(6,0)
        combo_proc.setCurrentText("SoilEvaporation")
        combo_alg = table.cellWidget(6,1)
        combo_alg.setCurrentText("SOILEVAP_HBV")
        combo_from = table.cellWidget(6,2)
        combo_from.setCurrentText("SOIL[0]")
        combo_to = table.cellWidget(6,4)
        combo_to.setCurrentText("ATMOSPHERE")

        combo_proc = table.cellWidget(7,0)
        combo_proc.setCurrentText("CapillaryRise")
        combo_alg = table.cellWidget(7,1)
        combo_alg.setCurrentText("CRISE_HBV")
        combo_from = table.cellWidget(7,2)
        combo_from.setCurrentText("SOIL[1]")
        combo_to = table.cellWidget(7,4)
        combo_to.setCurrentText("SOIL[0]")

        combo_proc = table.cellWidget(8,0)
        combo_proc.setCurrentText("Percolation")
        combo_alg = table.cellWidget(8,1)
        combo_alg.setCurrentText("PERC_CONSTANT")
        combo_from = table.cellWidget(8,2)
        combo_from.setCurrentText("SOIL[1]")
        combo_to = table.cellWidget(8,4)
        combo_to.setCurrentText("SOIL[2]")

        combo_proc = table.cellWidget(9,0)
        combo_proc.setCurrentText("Baseflow")
        combo_alg = table.cellWidget(9,1)
        combo_alg.setCurrentText("BASE_POWER_LAW")
        combo_from = table.cellWidget(9,2)
        combo_from.setCurrentText("SOIL[1]")
        combo_to = table.cellWidget(9,4)
        combo_to.setCurrentText("SURFACE_WATER")

        combo_proc = table.cellWidget(10,0)
        combo_proc.setCurrentText("Baseflow")
        combo_alg = table.cellWidget(10,1)
        combo_alg.setCurrentText("BASE_THRESH_POWER")
        combo_from = table.cellWidget(10,2)
        combo_from.setCurrentText("SOIL[1]")
        combo_to = table.cellWidget(10,4)
        combo_to.setCurrentText("SURFACE_WATER")

        combo_proc = table.cellWidget(11,0)
        combo_proc.setCurrentText("Baseflow")
        combo_alg = table.cellWidget(11,1)
        combo_alg.setCurrentText("BASE_LINEAR")
        combo_from = table.cellWidget(11,2)
        combo_from.setCurrentText("SOIL[2]")
        combo_to = table.cellWidget(11,4)
        combo_to.setCurrentText("SURFACE_WATER")

        table.resizeColumnsToContents() #Resizes the width of the column automatically
        
        print("HBV-Light template loaded.")
        self.iface.messageBar().pushSuccess("Success", "Loaded HBV-Light template successfully")
    except Exception as e:
        print('An error occured while loading HBV-Light template.')
        print(e)        