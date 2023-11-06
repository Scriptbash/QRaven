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
from .datascrapers.geomet import StreamFlow
import shutil
import os


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
            #self.download_streamflow()
            #self.load_model()
            #self.download_daymet_data()
            #self.download_gis_data()
            #self.run_basin_maker()
            #self.run_gridweights()
            #self.create_main_rvt_file()
            #self.run_raven()
            if self.dlg.rd_calibration_yes.isChecked():
                self.run_ostrich()

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
            make_folder(model_folder + '/output')
            print('Created ' + model_folder)

        make_folder(output + '/ncfiles')
        print('Created temporary folder' + output + '/ncfile')
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

    def download_streamflow(self):
        output = self.dlg.file_thunder_output.filePath()
        output = output + '/BasinMaker/Data/gauges'
        make_folder(output)
        StreamFlow(self.dlg).get_hydro_data(self.selected_structures)

    def download_daymet_data(self):
        input_polygon = self.dlg.file_thunder_polygon.filePath()
        output = self.dlg.file_thunder_output.filePath()
        start_date = self.dlg.date_thunder_start.date()
        end_date = self.dlg.date_thunder_end.date()

        self.dlg.file_daymet_output.setFilePath(output + '/ncfiles')
        self.dlg.file_daymet_polygon.setFilePath(input_polygon)
        self.dlg.date_daymet_start_date.setDate(start_date)
        self.dlg.date_daymet_end_date.setDate(end_date)
        item = self.dlg.list_daymet_variables.item(0)
        item.setSelected(True)
        item = self.dlg.list_daymet_variables.item(1)
        item.setSelected(True)
        item = self.dlg.list_daymet_variables.item(2)
        item.setSelected(True)
        self.dlg.chk_daymet_insert_nan.setChecked(True)
        self.dlg.chk_daymet_merge.setChecked(True)
        self.dlg.chk_daymet_fill_values.setChecked(True)
        self.dlg.btn_download_daymet.click()
        for structure in self.selected_structures:
            make_folder(output + '/' + structure + '/forcing')
            shutil.copy(output + '/ncfiles/prcp_merged.nc', output + '/' + structure + '/forcing/prcp.nc')
            shutil.copy(output + '/ncfiles/tmin_merged.nc', output + '/' + structure + '/forcing/tmin.nc')
            shutil.copy(output + '/ncfiles/tmax_merged.nc', output + '/' + structure + '/forcing/tmax.nc')
        shutil.rmtree(output + '/ncfiles')



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
        self.dlg.btn_dockerrun.click()
        files_to_copy = ['channel_properties.rvp', 'Lakes.rvh', model_name + '.rvh']
        for file in files_to_copy:
            for structure in self.selected_structures:
                shutil.copy(basin_maker_path + '/Output/OIH_Output/network_after_gen_hrus/RavenInput/' + file,
                            output_folder + '/' + structure + '/' + file)

    def run_gridweights(self):
        # todo Get subbasin ID from the hru shp file
        output = self.dlg.file_thunder_output.filePath()
        basinmaker_output = self.dlg.file_thunder_output.filePath() + \
                            '/BasinMaker/Output/OIH_Output/network_after_gen_hrus/finalcat_info.shp'
        self.dlg.file_netcdf.setFilePath(output + '/' + self.selected_structures[0] + '/forcing/tmin_merged.nc')
        self.dlg.txt_dimlon.setText('x')
        self.dlg.txt_dimlat.setText('y')
        self.dlg.txt_varlon.setText('lon')
        self.dlg.txt_varlat.setText('lat')
        self.dlg.file_hrus.setFilePath(basinmaker_output)
        self.dlg.rb_subbasinid.setChecked(True)
        self.dlg.txt_gridid.setText('0000')
        self.dlg.file_outputgridweight.setFilePath(output + '/gridweights.txt')
        self.dlg.btn_rungridweight.click()

        for structure in self.selected_structures:
            try:
                shutil.copy(output + '/gridweights.txt', output + '/' + structure + '/forcing/gridweights.txt')
            except FileExistsError:
                os.remove(output + '/' + structure + '/forcing/gridweights.txt')
                shutil.copy(output + '/gridweights.txt', output + '/' + structure + '/forcing/gridweights.txt')
        os.remove(output + '/gridweights.txt')

    def create_main_rvt_file(self):
        output = self.dlg.file_thunder_output.filePath()
        model_name = self.dlg.txt_thunder_model_name.text()
        forcing_vars = [['precipitation', 'PRECIP', 'prcp'],
                        ['min_temp', 'TEMP_MIN', 'tmin'],
                        ['max_temp', 'TEMP_MAX', 'tmax']]
        for structure in self.selected_structures:
            output_path = output + '/' + structure + '/' + model_name + '.rvt'
            stations = []
            for file in os.listdir(output + '/' + structure):
                if file.endswith(".rvt"):
                    stations.append(file)
            with open(output_path, 'w') as rvt:
                for variable in forcing_vars:
                    rvt.write(':GriddedForcing\t\t' + variable[0])
                    rvt.write('\n\t:ForcingType\t' + variable[1])
                    rvt.write('\n\t:FileNameNC\tforcing/' + variable[2] + '.nc')
                    rvt.write('\n\t:VarNameNC\t' + variable[2])
                    rvt.write('\n\t:DimNamesNC\tlon lat time')
                    rvt.write('\n\t:RedirectToFile\tgridweights.txt')
                    rvt.write('\n:EndGriddedForcing\n\n')
                for station in stations:
                    rvt.write('\n:RedirectToFile\t' + station)

    def run_raven(self):
        output = self.dlg.file_thunder_output.filePath()
        for structure in self.selected_structures:
            output_path = output + '/' + structure + '/output'
            self.dlg.file_runinputdir.setFilePath(output + '/' + structure)
            self.dlg.file_runoutputdir.setFilePath(output_path)
            self.dlg.btn_runraven.click()  # Run Raven once to generate an .rvp template
            self.dlg.btn_overwrite_rvp.click()  # Remove the :CreateRVPTemplate command
            self.dlg.btn_fillrvptemplate.click()  # Fill the rvp template file
            self.dlg.btn_runraven.click()  # Run the simulation

    def run_ostrich(self):

        # Get OSTRICH settings
        ostrich_mode = self.dlg.combo_ostrichexe_mode.currentText()
        raven_mode = self.dlg.combo_ravenexe_mode.currentText()

        # Set basic config
        self.dlg.combo_ost_exe.setCurrentText('QRaven generated')
        self.dlg.file_ost_exe.setFilePath('Raven.exe')
        self.dlg.combo_programtype.setCurrentText('DDS')
        self.dlg.txt_ost_modelsubdir.setText('processor_')
        self.dlg.combo_ost_objfunc.setCurrentText('gcop')
        self.dlg.file_ost_preservebestmod.setFilePath('')
        self.dlg.combo_ost_preservebestmodoutput.setCurrentText('yes')
        self.dlg.combo_ost_warmstart.setCurrentText('no')
        self.dlg.spin_ost_numdigits.setValue(6)
        self.dlg.combo_telescopingstrat.setCurrentText('none')
        self.dlg.txt_ost_randomseed.setText('')
        self.dlg.combo_ost_onobserror.setCurrentText('quit')
        self.dlg.combo_ost_checksensitivities.setCurrentText('no')
        self.dlg.combo_ost_supermuse.setCurrentText('no')
        self.dlg.combo_ost_caching.setCurrentText('no')
        self.dlg.spin_ost_boxcoxtrans.setValue(1.00)
        self.dlg.txt_ost_modoutputredirection.setText('OstExeOut.txt')

        output = self.dlg.file_thunder_output.filePath()
        model_name = self.dlg.txt_thunder_model_name.text()

        for structure in self.selected_structures:
            model_files_path = output + '/' + structure + '/' + model_name

            # Define the executable script for each model
            self.dlg.file_ost_exe.setFilePath(output + '/' + structure + '/qrvn_launch_raven.sh')

            # Clear the file pairs, response and tied response variables tables
            while self.dlg.table_filepairs.rowCount() > 0:
                self.dlg.table_filepairs.removeRow(0)
            while self.dlg.table_ost_resp_var.rowCount() > 0:
                self.dlg.table_ost_resp_var.removeRow(0)
            while self.dlg.table_ost_tied_resp_var.rowCount() > 0:
                self.dlg.table_ost_tied_resp_var.removeRow(0)

            # Set the file pairs
            self.dlg.btn_add_filepair.click()
            template_file = self.dlg.table_filepairs.cellWidget(0, 0)
            template_file.setFilePath(model_files_path + '.rvp_temp.rvp')
            model_file = self.dlg.table_filepairs.cellWidget(0, 1)
            model_file.setFilePath(model_files_path + '.rvp')

            # Load parameters to calibrate
            self.dlg.btn_ost_load_params.click()
            self.dlg.btn_ost_select_all.click()
            self.dlg.btn_ost_refresh_vals.click()

            # Add response variables
            diagnostics_file = output + '/' + structure + '/output/Diagnostics.csv'
            self.dlg.btn_ost_add_resp_var.click()
            self.dlg.table_ost_resp_var.cellWidget(0, 0).setText('KGE')
            self.dlg.table_ost_resp_var.cellWidget(0, 1).setFilePath(diagnostics_file)

            # Load algorithm settings
            self.dlg.btn_ost_alg_refresh.click()
            self.dlg.btn_ost_obj_refresh.click()

            # Write OSTRICH input file
            self.dlg.file_ost_output.setFilePath(output + '/' + structure + '/ostIn.txt')
            self.dlg.btn_ost_write.click()

            # Run OSTRICH
            self.dlg.file_ost_input.setFilePath(output + '/' + structure + '/ostIn.txt')
            self.dlg.btn_ost_run.click()
