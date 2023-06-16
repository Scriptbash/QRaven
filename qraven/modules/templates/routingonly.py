from ..hydrologicproc import addprocess


# This method loads a template of HBV-Light into the GUI
def load_routing_only(self):
    try:
        table = self.dlg.table_hydroprocess  # Get the hydrological processes table

        # Sets the model parameters

        self.dlg.combo_routing.setCurrentText("ROUTE_DIFFUSIVE_WAVE")
        self.dlg.combo_catchment.setCurrentText("ROUTE_GAMMA_CONVOLUTION")
        self.dlg.combo_evapo.setCurrentText("PET_NONE")
        self.dlg.combo_owevapo.setCurrentText("PET_NONE")
        self.dlg.combo_potentialmelt.setCurrentText("POTMELT_NONE")
        self.dlg.combo_precipicept.setCurrentText("PRECIP_ICEPT_NONE")

        self.dlg.combo_soilmod.setCurrentText("SOIL_ONE_LAYER")
        self.dlg.combo_swradation.setCurrentText("SW_RAD_NONE")
        # Sets the hydrological processes
        for i in range(2):
            addprocess(self)

        combo_proc = table.cellWidget(0, 0)
        combo_proc.setCurrentText("Precipitation")
        combo_alg = table.cellWidget(0, 1)
        combo_alg.setCurrentText("PRECIP_RAVEN")
        combo_from = table.cellWidget(0, 2)
        combo_from.setCurrentText("ATMOS_PRECIP")
        combo_to = table.cellWidget(0, 4)
        combo_to.setCurrentText("PONDED_WATER")

        combo_proc = table.cellWidget(1, 0)
        combo_proc.setCurrentText("Flush")
        combo_alg = table.cellWidget(1, 1)
        combo_alg.setCurrentText("RAVEN_DEFAULT")
        combo_from = table.cellWidget(1, 2)
        combo_from.setCurrentText("PONDED_WATER")
        combo_to = table.cellWidget(1, 4)
        combo_to.setCurrentText("SURFACE_WATER")

        table.resizeColumnsToContents()  # Resizes the width of the column automatically

        print("Routing-only template loaded.")
        self.iface.messageBar().pushSuccess("Success", "Loaded Routing-only template successfully")
    except Exception as e:
        print('An error occured while loading Routing-only template.')
        print(e)
