from qgis.gui import QgsFileWidget
from qgis.PyQt.QtWidgets import *
from ..PyRavenR import readRavenParams, readRVPtemplate
from pathlib import Path
from os import path


class Ostrich:
    def __init__(self):
        self.param_matches = []

    def add_file_pair(self, dlg):
        # Adds a new row in the file pairs table

        table = dlg.table_filepairs  # Get the file pairs table
        current_row = table.rowCount()  # Get the number of rows the table has
        table.insertRow(current_row)  # Inserts a new row below the last row
        template_file = QgsFileWidget()
        template_file.setStorageMode(QgsFileWidget.GetFile)
        model_input_file = QgsFileWidget()
        model_input_file.setStorageMode(QgsFileWidget.GetFile)

        table.setCellWidget(current_row, 0, template_file)
        table.setCellWidget(current_row, 1, model_input_file)

        table.resizeColumnsToContents()

    def remove_file_pair(self, dlg):
        # Removes the selected row from the file pairs table

        table = dlg.table_filepairs
        selected_row = table.currentRow()
        table.removeRow(selected_row)

    def load_parameters(self, dlg):
        # Loads the parameters in the parameters selection table
        script_dir = Path(__file__).parent.parent.parent
        raven_parameters_file = path.join(script_dir, "ext_data/RavenParameters.dat")
        rvn_rvp_params = readRavenParams(raven_parameters_file)  # Gathers all possible rvp params

        file_pairs = self.get_file_pairs(dlg)   # Extracts get the file pairs (currently support only one pair)
        table = dlg.table_ost_params

        self.clear_table(table)

        # TODO finish this loop so multiple file pairs can be used without crashing
        for pairs in file_pairs:
            template = pairs[0]
            rvp_template_params = readRVPtemplate(template)  # Read the template file

        rvp_template_clean = []   # Cleans up the list so all parameters needed can match
        for line in rvp_template_params:
            for item in line:
                rvp_template_clean.append(item.strip(','))

        # Loop that matches the parameters from the template file with the RavenParameters.dat file
        self.param_matches = []
        tmp_param_matches = []  # List to keep track of parameters. Used only to avoid duplicates
        for line in rvp_template_clean:
            for param in rvn_rvp_params[1:][0:]:
                if param[0] in line and param[0].strip() != '' and param[0] not in tmp_param_matches:
                    tmp_param_matches.append(param[0])
                    self.param_matches.append(param)
                    chk_params = QCheckBox()
                    chk_params.setChecked(True)
                    lbl_params = QLabel()
                    lbl_params.setText(param[0])
                    current_row = table.rowCount()  # Get the number of rows the table has
                    table.insertRow(current_row)  # Inserts a new row below the last row
                    table.setCellWidget(current_row, 0, chk_params)
                    table.setCellWidget(current_row, 1, lbl_params)
        table.resizeColumnsToContents()

    def get_file_pairs(self, dlg):
        table = dlg.table_filepairs
        rows = table.rowCount()
        cols = table.columnCount()
        file_pairs = []
        for row in range(rows):
            tmp_pairs = []
            for col in range(cols):
                current_widget = table.cellWidget(row, col)
                if current_widget.filePath():
                    tmp_pairs.append(current_widget.filePath())
                else:
                    pass
            file_pairs.append(tmp_pairs)

        return file_pairs

    def load_calibration_values(self, dlg):
        params = self.get_params(dlg)
        table = dlg.table_ost_values

        self.clear_table(table)
        for line in params:
            current_row = table.rowCount()  # Get the number of rows the table has
            table.insertRow(current_row)  # Inserts a new row below the last row

            initial_value = line[4]
            lower_bound = line[5]
            upper_bound = line[6]

            try:
                int(initial_value)
                int(lower_bound)
                int(upper_bound)

                param_type = 'Integer'
                initial_value = int(line[4])
                lower_bound = int(line[5])
                upper_bound = int(line[6])
            except:
                param_type = 'Real'
                initial_value = float(line[4])
                lower_bound = float(line[5])
                upper_bound = float(line[6])

            lbl_param = QLabel()
            lbl_param.setText(line[0])
            combo_param_type = QComboBox()
            combo_param_type.addItems(['Integer', 'Real'])
            combo_param_type.setCurrentText(param_type)
            combo_param_type.setEnabled(False)

            txt_input = QLineEdit()
            txt_output = QLineEdit()
            txt_internal = QLineEdit()
            txt_format = QLineEdit()

            if param_type == 'Integer':
                spin_initial_val = QSpinBox()
                spin_lwr_bound = QSpinBox()
                spin_upr_bound = QSpinBox()
                txt_input.setEnabled(False)
                txt_output.setEnabled(False)
                txt_internal.setEnabled(False)
                txt_format.setEnabled(False)
            else:
                spin_initial_val = QDoubleSpinBox()
                spin_lwr_bound = QDoubleSpinBox()
                spin_upr_bound = QDoubleSpinBox()

            spin_initial_val.setMinimum(lower_bound)
            spin_initial_val.setMaximum(upper_bound)
            spin_initial_val.setValue(initial_value)

            spin_lwr_bound.setMinimum(lower_bound)
            spin_lwr_bound.setMaximum(upper_bound)
            spin_lwr_bound.setValue(lower_bound)

            spin_upr_bound.setMinimum(lower_bound)
            spin_upr_bound.setMaximum(upper_bound)
            spin_upr_bound.setValue(upper_bound)

            table.setCellWidget(current_row, 0, lbl_param)
            table.setCellWidget(current_row, 1, combo_param_type)
            table.setCellWidget(current_row, 2, spin_initial_val)
            table.setCellWidget(current_row, 3, spin_lwr_bound)
            table.setCellWidget(current_row, 4, spin_upr_bound)
            table.setCellWidget(current_row, 5, txt_input)
            table.setCellWidget(current_row, 6, txt_output)
            table.setCellWidget(current_row, 7, txt_internal)
            table.setCellWidget(current_row, 8, txt_format)

        table.resizeColumnsToContents()

    def get_params(self, dlg):
        table = dlg.table_ost_params
        rows = table.rowCount()
        params = []
        for row in range(rows):
            checkbox = table.cellWidget(row, 0)
            if checkbox.isChecked():
                params.append(self.param_matches[row])
            else:
                pass

        return params

    def export_calibration_values(self, dlg):
        table = dlg.table_ost_values
        rows = table.rowCount()
        cols = table.columnCount()
        calibration_real_values = []
        calibration_int_values = []

        for row in range(rows):
            tmp_calib_values = []
            value_type = ''
            for col in range(cols):
                current_widget = table.cellWidget(row, col)
                if isinstance(current_widget, QComboBox):
                    value_type = current_widget.currentText()
                elif isinstance(current_widget, QLineEdit):
                    if current_widget.text() != '':
                        tmp_calib_values.append(current_widget.text())
                    else:
                        tmp_calib_values.append('none')
                elif isinstance(current_widget, QSpinBox) or isinstance(current_widget, QDoubleSpinBox):
                    tmp_calib_values.append(str(current_widget.value()))
                elif isinstance(current_widget, QLabel):
                    tmp_calib_values.append(current_widget.text())
            if value_type == 'Integer':
                calibration_int_values.append(tmp_calib_values)
            else:
                calibration_real_values.append(tmp_calib_values)

        return calibration_int_values, calibration_real_values

    def clear_table(self, table):
        while table.rowCount() > 0:
            table.removeRow(0)

    def select_all(self, dlg):
        table = dlg.table_ost_params
        rows = table.rowCount()
        for row in range(rows):
            checkbox = table.cellWidget(row, 0)
            checkbox.setChecked(True)

    def unselect_all(self, dlg):
        table = dlg.table_ost_params
        rows = table.rowCount()
        for row in range(rows):
            checkbox = table.cellWidget(row, 0)
            checkbox.setChecked(False)

    def add_extra_file(self, dlg):
        table = dlg.table_extra_file  # Get the extra file table
        current_row = table.rowCount()  # Get the number of rows the table has
        table.insertRow(current_row)  # Inserts a new row below the last row
        extra_file = QgsFileWidget()
        extra_file.setStorageMode(QgsFileWidget.GetFile)

        table.setCellWidget(current_row, 0, extra_file)

        table.resizeColumnsToContents()

    def remove_extra_file(self, dlg):
        # Removes the selected row from the file pairs table

        table = dlg.table_extra_file
        selected_row = table.currentRow()
        table.removeRow(selected_row)

    def get_extra_file(self, dlg):
        table = dlg.table_extra_file
        rows = table.rowCount()
        extra_files = []
        for row in range(rows):
            current_widget = table.cellWidget(row, 0)
            if current_widget.filePath():
                file_name = path.basename(current_widget.filePath())
                extra_files.append(file_name)
            else:
                pass

        return extra_files

    def add_extra_dir(self, dlg):
        table = dlg.table_extra_dir  # Get the extra dir table
        current_row = table.rowCount()  # Get the number of rows the table has
        table.insertRow(current_row)  # Inserts a new row below the last row
        extra_dir = QgsFileWidget()
        extra_dir.setStorageMode(QgsFileWidget.GetDirectory)

        table.setCellWidget(current_row, 0, extra_dir)

        table.resizeColumnsToContents()

    def remove_extra_dir(self, dlg):
        table = dlg.table_extra_dir
        selected_row = table.currentRow()
        table.removeRow(selected_row)

    def get_extra_dir(self, dlg):
        table = dlg.table_extra_dir
        rows = table.rowCount()
        extra_dir = []
        for row in range(rows):
            current_widget = table.cellWidget(row, 0)
            if current_widget.filePath():
                dir_name = current_widget.filePath().split('/') # Needs testing on Windows!!
                extra_dir.append(dir_name[-1])
            else:
                pass

        return extra_dir

    def set_input_file(self, dlg):
        output_file = dlg.file_ost_output.filePath()
        input_file = dlg.file_ost_input

        input_file.setFilePath(output_file)

    def write_input_file(self, dlg):
        output_file = dlg.file_ost_output.filePath()
        basic_config_param = self.get_basic_config_params(dlg)
        file_pairs = self.get_file_pairs(dlg)
        extra_files = self.get_extra_file(dlg)
        extra_dir = self.get_extra_dir(dlg)
        int_params, real_params = self.export_calibration_values(dlg)

        with open(output_file,'w') as ostin:

            # Write header
            ostin.write("#".ljust(74, '=')+"#"
                          "\n# Generated by QRaven".ljust(76)+"#"+
                          "\n# Please report any issues on https://github.com/Scriptbash/QRaven/issues #\n"+
                          "#".ljust(74, '=')+"#\n\n")

            # Write basic config parameters
            for key, value in basic_config_param.items():
                if value != '':
                    ostin.write(f"{key:<30}  {value}\n")

            # Write file pairs
            if file_pairs:
                ostin.write('\nBeginFilePairs')
                for pair in file_pairs:
                    ostin.write('\n ' + path.basename(pair[0]) + ' ; ' + path.basename(pair[1]))
                ostin.write('\nEndFilePairs\n')

            if extra_files:
                ostin.write('\nBeginExtraFiles')
                for file in extra_files:
                    ostin.write('\n ' + file)
                ostin.write('\nEndExtraFiles\n')

            if extra_dir:
                ostin.write('\nBeginExtraDirs')
                for directory in extra_dir:
                    ostin.write('\n ' + directory)
                ostin.write('\nEndExtraDirs\n')

            # Write float calibration parameters
            if real_params:
                ostin.write('\nBeginParams')
                for line in real_params:
                    ostin.write('\n ')
                    for value in line:
                        ostin.write(value.ljust(20))
                ostin.write('\nEndParams\n')

            if int_params:
                # Write integer calibration parameters
                ostin.write('\nBeginIntegerParams')
                for line in int_params:
                    ostin.write('\n ')
                    for value in line:
                        ostin.write(value.ljust(20))
                ostin.write('\nEndIntegerParams\n')

    def get_basic_config_params(self,dlg):

        program_type = dlg.combo_programtype.currentText()
        model_executable = dlg.file_ost_exe.filePath() #Need to add a check for container
        model_sub_directory = dlg.txt_ost_modelsubdir.text()
        objective_function = dlg.combo_ost_objfunc.currentText()
        preserve_best_model = dlg.file_ost_preservebestmod.filePath()
        preserve_best_model_output = dlg.combo_ost_preservebestmodoutput.currentText()
        ostrich_warm_start = dlg.combo_ost_warmstart.currentText()
        number_digits_precision = str(dlg.spin_ost_numdigits.value())
        telescoping_strategy = dlg.combo_telescopingstrat.currentText()
        random_seed = dlg.txt_ost_randomseed.text()
        on_obs_error = dlg.combo_ost_onobserror.currentText()
        if on_obs_error == 'value':
            on_obs_error = str(dlg.spin_ost_onobserror.value())
        check_sensitivities = dlg.combo_ost_checksensitivities.currentText()
        super_muse = dlg.combo_ost_supermuse.currentText()
        ostrich_caching = dlg.combo_ost_caching.currentText()
        box_cox_transformation = str(dlg.spin_ost_boxcoxtrans.value())
        model_output_redirection = dlg.txt_ost_modoutputredirection.text()

        params = {
            'ProgramType':                  program_type,
            'ModelExecutable':              model_executable,
            'ModelSubdir':                  model_sub_directory,
            'ObjectiveFunction':            objective_function,
            'PreserveBestModel':            preserve_best_model,
            'PreserveBestModelOutput':      preserve_best_model_output,
            'OstrichWarmStart':             ostrich_warm_start,
            'NumDigitsOfPrecision':         number_digits_precision,
            'TelescopingStrategy':          telescoping_strategy,
            'RandomSeed':                   random_seed,
            'OnObsError':                   on_obs_error,
            'CheckSensitivities':           check_sensitivities,
            'SuperMUSE':                    super_muse,
            'OstrichCaching':               ostrich_caching,
            'BoxCoxTransformation':         box_cox_transformation,
            'ModelOutputRedirectionFile':   model_output_redirection
        }

        return params
