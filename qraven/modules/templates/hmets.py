from ..hydrologicproc import addprocess

#This method loads a template of HMETS into the GUI
def loadHmets(self):
    try:
        table = self.dlg.table_hydroprocess #Get the hydrological processes table

        #Sets the model parameters 
        self.dlg.combo_potentialmelt.setCurrentText("POTMELT_HMETS")
        self.dlg.combo_rainsnowfrac.setCurrentText("RAINSNOW_DATA")
        self.dlg.combo_evapo.setCurrentText("PET_OUDIN")
        self.dlg.combo_catchment.setCurrentText("ROUTE_DUMP")
        self.dlg.combo_routing.setCurrentText("ROUTE_NONE")
        self.dlg.combo_soilmod.setCurrentText("SOIL_TWO_LAYER")

        #Sets the hydrological processes
        for i in range(11):
            addprocess(self)
        
        combo_proc = table.cellWidget(0,0)
        combo_proc.setCurrentText("SnowBalance")
        combo_alg = table.cellWidget(0,1)
        combo_alg.setCurrentText("SNOBAL_HMETS")
        combo_from = table.cellWidget(0,2)
        combo_from.setCurrentText("MULTIPLE")
        combo_to = table.cellWidget(0,4)
        combo_to.setCurrentText("MULTIPLE")
    
        combo_proc = table.cellWidget(1,0)
        combo_proc.setCurrentText("Precipitation")
        combo_alg = table.cellWidget(1,1)
        combo_alg.setCurrentText("RAVEN_DEFAULT")
        combo_from = table.cellWidget(1,2)
        combo_from.setCurrentText("ATMOS_PRECIP")
        combo_to = table.cellWidget(1,4)
        combo_to.setCurrentText("MULTIPLE")

        combo_proc = table.cellWidget(2,0)
        combo_proc.setCurrentText("Infiltration")
        combo_alg = table.cellWidget(2,1)
        combo_alg.setCurrentText("INF_HMETS")
        combo_from = table.cellWidget(2,2)
        combo_from.setCurrentText("PONDED_WATER")
        combo_to = table.cellWidget(2,4)
        combo_to.setCurrentText("MULTIPLE")

        combo_proc = table.cellWidget(3,0)
        combo_proc.setCurrentText("Overflow")
        combo_alg = table.cellWidget(3,1)
        combo_alg.setCurrentText("OVERFLOW_RAVEN")
        combo_from = table.cellWidget(3,2)
        combo_from.setCurrentText("SOIL[0]")
        combo_to = table.cellWidget(3,4)
        combo_to.setCurrentText("CONVOLUTION[1]")

        combo_proc = table.cellWidget(4,0)
        combo_proc.setCurrentText("Baseflow")
        combo_alg = table.cellWidget(4,1)
        combo_alg.setCurrentText("BASE_LINEAR")
        combo_from = table.cellWidget(4,2)
        combo_from.setCurrentText("SOIL[0]")
        combo_to = table.cellWidget(4,4)
        combo_to.setCurrentText("SURFACE_WATER")

        combo_proc = table.cellWidget(5,0)
        combo_proc.setCurrentText("Percolation")
        combo_alg = table.cellWidget(5,1)
        combo_alg.setCurrentText("PERC_LINEAR")
        combo_from = table.cellWidget(5,2)
        combo_from.setCurrentText("SOIL[0]")
        combo_to = table.cellWidget(5,4)
        combo_to.setCurrentText("SOIL[1]")

        combo_proc = table.cellWidget(6,0)
        combo_proc.setCurrentText("Overflow")
        combo_alg = table.cellWidget(6,1)
        combo_alg.setCurrentText("OVERFLOW_RAVEN")
        combo_from = table.cellWidget(6,2)
        combo_from.setCurrentText("SOIL[1]")
        combo_to = table.cellWidget(6,4)
        combo_to.setCurrentText("CONVOLUTION[1]")

        combo_proc = table.cellWidget(7,0)
        combo_proc.setCurrentText("SoilEvaporation")
        combo_alg = table.cellWidget(7,1)
        combo_alg.setCurrentText("SOILEVAP_ALL")
        combo_from = table.cellWidget(7,2)
        combo_from.setCurrentText("SOIL[0]")
        combo_to = table.cellWidget(7,4)
        combo_to.setCurrentText("ATMOSPHERE")

        combo_proc = table.cellWidget(8,0)
        combo_proc.setCurrentText("Convolve")
        combo_alg = table.cellWidget(8,1)
        combo_alg.setCurrentText("CONVOL_GAMMA")
        combo_from = table.cellWidget(8,2)
        combo_from.setCurrentText("CONVOLUTION[0]")
        combo_to = table.cellWidget(8,4)
        combo_to.setCurrentText("SURFACE_WATER")

        combo_proc = table.cellWidget(9,0)
        combo_proc.setCurrentText("Convolve")
        combo_alg = table.cellWidget(9,1)
        combo_alg.setCurrentText("CONVOL_GAMMA_2")
        combo_from = table.cellWidget(9,2)
        combo_from.setCurrentText("CONVOLUTION[1]")
        combo_to = table.cellWidget(9,4)
        combo_to.setCurrentText("SURFACE_WATER")

        combo_proc = table.cellWidget(10,0)
        combo_proc.setCurrentText("Baseflow")
        combo_alg = table.cellWidget(10,1)
        combo_alg.setCurrentText("BASE_LINEAR")
        combo_from = table.cellWidget(10,2)
        combo_from.setCurrentText("SOIL[1]")
        combo_to = table.cellWidget(10,4)
        combo_to.setCurrentText("SURFACE_WATER")

        table.resizeColumnsToContents() #Resizes the width of the column automatically
        
        print("HMETS template loaded.")
        self.iface.messageBar().pushSuccess("Success", "Loaded HMETS template successfully")
    except Exception as e:
        print('An error occured while loading HMETS template.')
        print(e)