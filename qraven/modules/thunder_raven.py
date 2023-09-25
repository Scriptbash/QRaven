from .resetgui import fullReset, partialReset
from .templates.hmets import loadHmets
from .templates.hbvec import loadHbvec
from .templates.hbvlight import loadHbvlight
from .templates.ubcwm import loadUbcwm
from .templates.gr4j import loadGr4j
from .templates.canshield import loadCanshield
from .templates.mohyse import loadMohyse
from .templates.hypr import loadHypr
from .templates.hymod import loadHymod
from .templates.awbm import loadAwbm
#from .templates.blended import load_blended
from .templates.routingonly import load_routing_only
from .utilities import *
import shutil


class ThunderRaven:

    def __init__(self, qrvn):
        self.qrvn = qrvn
        self.dlg = self.qrvn.dlg

        model_structures = ['AWBM', 'Canadian Shield', 'GR4J', 'HBV-EC',
                            'HBV-Light', 'HMETS', 'HYMOD', 'HYPR', 'MOHYSE',
                            'UBCWM', 'Routing-only']
        # Set the model structures combobox values
        for structure in model_structures:
            self.dlg.mcombo_thunder_structure.addItemWithCheckState(structure, False)

    def generate_model(self):
        # Todo Check if start/end date available for watershed streamflow data
        status = self.check_input()
        if status == 0:
            self.prepare_environment()
            #self.load_model()
            #self.download_gis_data()
            self.run_basin_maker()

    def check_input(self):
        return_code = 0
        if not self.dlg.mcombo_thunder_structure.checkedItems():
            self.dlg.lbl_thunder_structure.setText('You must select at least one structure!')
            return_code = 1
        else:
            self.dlg.lbl_thunder_structure.clear()
        if not self.dlg.txt_thunder_model_name.text():
            self.dlg.lbl_thunder_name.setText('You must enter a name for your model!')
            return_code = 1
        else:
            self.dlg.lbl_thunder_name.clear()
        #if self.dlg.rd_thunder_use_poly.isChecked() and not self.dlg.file_thunder_polygon.filePath():
        #    self.dlg.lbl_thunder_ws_info.setText('You must select a shapefile!')
        #    return_code = 1
        #else:
        #    self.dlg.lbl_thunder_ws_info.clear()
        if not self.dlg.file_thunder_output.filePath():
            self.dlg.lbl_thunder_output.setText('You must select an output folder!')
            return_code = 1
        else:
            self.dlg.lbl_thunder_output.clear()
        return return_code

    def prepare_environment(self):
        output = self.dlg.file_thunder_output.filePath()
        self.selected_structures = self.dlg.mcombo_thunder_structure.checkedItems()

        for structure in self.selected_structures:
            model_folder = output + '/' + structure
            make_folder(model_folder)
            print('Created ' + model_folder)

        basin_maker_folder = output + '/BasinMaker'
        make_folder(basin_maker_folder + '/Data')
        print('Created ' + basin_maker_folder + '/Data')
        make_folder(basin_maker_folder + '/Output')
        print('Created ' + basin_maker_folder + 'Output')

    def load_model(self):
        for structure in self.selected_structures:
            fullReset(self.qrvn)
            if structure == 'AWBM':
                loadAwbm(self.qrvn)
            elif structure == 'Canadian Shield':
                loadCanshield(self.qrvn)
            elif structure == 'GR4J':
                loadGr4j(self.qrvn)
            elif structure == 'HBV-EC':
                loadHbvec(self.qrvn)
            elif structure == 'HBV-Light':
                loadHbvlight(self.qrvn)
            elif structure == 'UBCWM':
                loadUbcwm(self.qrvn)
            elif structure == 'HMETS':
                loadHmets(self.qrvn)
            elif structure == 'MOHYSE':
                loadMohyse(self.qrvn)
            elif structure == 'HYMOD':
                loadHymod(self.qrvn)
            elif structure == 'HYPR':
                loadHypr(self.qrvn)
            elif structure == 'Routing-only':
                load_routing_only(self.qrvn)

            model_name = self.dlg.txt_thunder_model_name.text()
            start_date = self.dlg.date_thunder_start.date()
            end_date = self.dlg.date_thunder_end.date()
            output_folder = self.dlg.file_thunder_output.filePath()

            self.dlg.txt_modname.setText(model_name)
            self.dlg.date_startdate.setDate(start_date)
            self.dlg.date_enddate.setDate(end_date)
            self.dlg.spin_timestep_h.setValue(24)
            self.dlg.chk_rvptemplate.setChecked(True)
            item = self.dlg.list_evalmetrics.item(4)
            item.setSelected(True)
            item = self.dlg.list_evalmetrics.item(9)
            item.setSelected(True)
            item = self.dlg.list_evalmetrics.item(21)
            item.setSelected(True)

            self.dlg.file_rvioutputdir.setFilePath(output_folder + '/' + structure)
            self.dlg.btn_write.click()

    def download_gis_data(self):
        self.dlg.stackedWidget.setCurrentIndex(4)
        self.dlg.sidemenu.setCurrentRow(4)
        QApplication.processEvents()
        output = self.dlg.file_thunder_output.filePath()
        input_polygon = self.dlg.file_thunder_polygon.filePath()
        output_gis = output + '/BasinMaker/Data'
        self.dlg.chk_download_dem.setChecked(True)
        self.dlg.chk_download_flowdir.setChecked(False)
        self.dlg.chk_download_lakes.setChecked(True)
        self.dlg.chk_download_bankfull.setChecked(True)
        self.dlg.chk_download_landuse.setChecked(True)
        self.dlg.chk_download_soil.setChecked(True)
        self.dlg.file_gis_download_output.setFilePath(output_gis)
        self.dlg.file_gis_clip_layer.setFilePath(input_polygon)
        self.dlg.btn_downloadgisdata.click()

    def run_basin_maker(self):
        output_folder = self.dlg.file_thunder_output.filePath()
        basin_maker_path = output_folder + '/BasinMaker'
        model_name = self.dlg.txt_thunder_model_name.text()
        self.dlg.file_outputfolder.setFilePath(basin_maker_path + '/Output')
        self.dlg.file_dem.setFilePath(basin_maker_path + '/Data/DEM/qrvn_dem.tif')
        self.dlg.file_landusepoly.setFilePath(basin_maker_path + '/Data/landuse/qrvn_landuse.shp')
        self.dlg.file_soil.setFilePath(basin_maker_path + '/Data/soil/qrvn_soil.shp')
        self.dlg.file_pointsinterest.setFilePath(basin_maker_path + '/Data/gauges/qrvn_stations.shp')
        self.dlg.file_lakes.setFilePath(basin_maker_path + '/Data/lakes/qrvn_lakes.shp')
        self.dlg.file_bankfullwidth.setFilePath(basin_maker_path + '/Data/bkf_width/qrvn_bankfull.shp')
        self.dlg.file_landuserast.setFilePath('')
        self.dlg.spin_ram.setValue(4096)
        self.dlg.rb_modedem.setChecked(True)
        self.dlg.rb_dem.setChecked(True)
        self.dlg.spin_facthreshold.setValue(9000)
        self.dlg.spin_conlakearea.setValue(0.00)
        self.dlg.spin_nonconlakearea.setValue(0.00)
        self.dlg.chk_epsgcode.setChecked(False)
        self.dlg.spin_filterconnectedlakes.setValue(0.00)
        self.dlg.spin_filternonconnectedlakes.setValue(0.00)
        self.dlg.txt_selectedlakeid.clear()
        self.dlg.spin_minsubbasinarea.setValue(0.00)
        self.dlg.file_pathlanduseinfo.setFilePath(basin_maker_path + '/Data/landuse/landuse_info.csv')
        self.dlg.file_pathsoilinfo.setFilePath(basin_maker_path + '/Data/soil/soil_info.csv')
        self.dlg.file_pathveginfo.setFilePath(basin_maker_path + '/Data/landuse/veg_info.csv')
        self.dlg.txt_modelname.setText(model_name)
        #self.dlg.btn_dockerrun.click()
        files_to_copy = ['channel_properties.rvp', 'Lakes.rvh', model_name + '.rvh']
        for file in files_to_copy:
            for structure in self.selected_structures:
                shutil.copy(basin_maker_path + '/Output/OIH_Output/network_after_gen_hrus/RavenInput/' + file,
                            output_folder + '/' + structure + '/' + file)
