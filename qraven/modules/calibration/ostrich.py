from qgis.gui import QgsFileWidget
from qgis.PyQt.QtWidgets import *
from ..PyRavenR import readRavenParams, readRVPtemplate
from pathlib import Path
from os import path
from sys import platform
import subprocess

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
        response_vars = self.get_response_var(dlg)
        gcop_settings = self.get_gcop_settings(dlg)
        algorithm_settings = self.get_algorithm_settings(dlg)
        self.create_rvp_template(dlg, int_params, real_params)
        with open(output_file, 'w') as ostin:

            # Write header
            ostin.write("#".ljust(74, '=')+"#"
                          "\n# Generated by QRaven".ljust(76) + "#" +
                          "\n# Please report any issues on https://github.com/Scriptbash/QRaven/issues #\n" +
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
                        ostin.write(value.ljust(15))
                ostin.write('\nEndParams\n')

            if int_params:
                # Write integer calibration parameters
                ostin.write('\nBeginIntegerParams')
                for line in int_params:
                    ostin.write('\n ')
                    for value in line:
                        ostin.write(value.ljust(15))
                ostin.write('\nEndIntegerParams\n')

            if response_vars:
                ostin.write('\nBeginResponseVars')
                for line in response_vars:
                    ostin.write('\n ')
                    for value in line:
                        ostin.write(str(value).ljust(20))
                ostin.write('\nEndResponseVars\n')

            if gcop_settings:
                ostin.write('\nBeginGCOP')
                for line in gcop_settings:
                    ostin.write('\n ')
                    for value in line:
                        ostin.write(str(value).ljust(20))
                ostin.write('\nEndGCOP\n')

            if algorithm_settings:
                algorithm = dlg.combo_programtype.currentText()
                if algorithm == 'BisectionAlgorithm':
                    tag = 'BisectionAlg'
                elif algorithm == 'Fletcher-Reeves':
                    tag = 'FletchReevesAlg'
                elif algorithm == 'Levenberg-Marquardt' or algorithm == 'GML-MS':
                    tag = 'LevMar'
                elif algorithm == 'GridAlgorithm':
                    tag = 'GridAlg'
                elif algorithm == 'Powell':
                    tag = 'PowellAlg'
                elif algorithm == 'Steepest-Descent':
                    tag = 'SteepDescAlg'
                elif algorithm == 'ParticleSwarm':
                    tag = 'ParticleSwarm'
                elif algorithm == 'APPSO':
                    tag = 'APPSO'
                elif algorithm == 'BEERS':
                    tag = 'BEERS'
                elif algorithm == 'BinaryGeneticAlgorithm' or algorithm == 'GeneticAlgorithm':
                    tag = 'GeneticAlg'
                elif algorithm == 'SimulatedAnnealing' or algorithm == 'DiscreteSimulatedAnnealing' or \
                        algorithm == 'VanderbiltSimulatedAnnealing':
                    tag = 'SimulatedAlg'
                elif algorithm == 'DDS':
                    tag = 'DDSAlg'
                elif algorithm == 'ParallelDDS':
                    tag = 'ParallelDDSAlg'
                elif algorithm == 'DiscreteDDS':
                    tag = 'DiscreteDDSAlg'
                elif algorithm == 'ShuffledComplexEvolution':
                    tag = 'SCEUA'
                elif algorithm == 'SamplingAlgorithm':
                    tag = 'SamplingAlg'
                elif algorithm == 'DDSAU':
                    tag = '_DDSAU_Alg'
                elif algorithm == 'GLUE':
                    tag = 'GLUE'
                elif algorithm == 'MetropolisSampler':
                    tag = 'MetropolisSampler'
                elif algorithm == 'RejectionSampler':
                    tag = 'RejectionSampler'
                elif algorithm == 'PADDS':
                    tag = 'PADDSAlg'
                elif algorithm == 'ParaPADDS':
                    tag = 'ParallelPADDSAlg'
                elif algorithm == 'SMOOTH':
                    tag = 'SMOOTH'

                ostin.write('\nBegin' + tag)
                for line in algorithm_settings:
                    ostin.write('\n ')
                    for value in line:
                        if value == 'UseParamValues':
                            pass
                        else:
                            ostin.write(str(value).ljust(30))
                ostin.write('\nEnd' + tag + '\n')
        if dlg.combo_ost_exe.currentText() == 'QRaven generated':
            self.generate_model_executable_script(dlg)

    def get_basic_config_params(self, dlg):

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

    def create_rvp_template(self, dlg, int_params, real_params):
        file_pairs = self.get_file_pairs(dlg)
        rvp_file = file_pairs[0][1]
        rvp_template_file = file_pairs[0][0]
        params = int_params + real_params
        count_param = 1
        index = []

        with open(rvp_file, 'r') as rvp:
            data = rvp.readlines()
            with open(rvp_template_file, 'w') as tpl_rvp:
                for line in data:
                    line = line.split()
                    # Remove commas from item
                    cleaned_line = [word.rstrip(',') for word in line]
                    # Skip empty lines
                    if not cleaned_line:
                        tpl_rvp.write('\n')
                        continue
                    # We just skip this row if it's the units line
                    if cleaned_line[0] == ':Units':
                        for word in line:
                            tpl_rvp.write(' ' + word)
                        tpl_rvp.write('\n')
                        continue
                    # We reached an attribute tag. We check if a param we want to calibrate is in the tag.
                    # If yes, we add the index to a list
                    elif ':Attributes' in cleaned_line or ':Parameters' in cleaned_line:
                        for word in line:
                            tpl_rvp.write(' ' + word)
                        tpl_rvp.write('\n')
                        index = []
                        for param in params:
                            if param[0] in cleaned_line:
                                index.append([count_param, cleaned_line.index(param[0])])
                                count_param += 1
                            else:
                                pass
                    elif ':GlobalParameter' in cleaned_line:
                        for param in params:
                            if param[0] in cleaned_line:
                                line[2] = 'param_x' + str(count_param)
                                count_param += 1
                        for word in line:
                            tpl_rvp.write(word + ' ')
                        tpl_rvp.write('\n')
                    elif len(line) == 1:  # If the length of the list is only 1, there's a chance it's an :End tag
                        check_end_tag = [word for word in line if ':End' in word]
                        if check_end_tag:
                            index = []  # An :End tag was found, reset the index list and proceed to the next line
                            for word in line:
                                tpl_rvp.write(word)
                            tpl_rvp.write('\n')
                            continue
                        else:
                            for word in line:
                                tpl_rvp.write(word)
                            tpl_rvp.write('\n')
                    else:
                        if index:   # If the index list exists, replace the parameters value until another tag is read
                            for i in index:
                                line[i[1]] = 'param_x' + str(i[0]) + ', '
                            for word in line:
                                tpl_rvp.write(' ' + word)
                            tpl_rvp.write('\n')
                        else:
                            for word in line:
                                tpl_rvp.write(word + ' ')
                            tpl_rvp.write('\n')

    def add_response_variable(self, dlg):
        table = dlg.table_ost_resp_var
        current_row = table.rowCount()  # Get the number of rows the table has
        table.insertRow(current_row)  # Inserts a new row below the last row

        var_name = QLineEdit()
        filename = QgsFileWidget()
        filename.setStorageMode(QgsFileWidget.GetFile)
        key = QLineEdit()
        key.setText('OST_NULL')
        line = QSpinBox()
        line.setMaximum(99999)
        line.setMinimum(0)
        line.setValue(1)
        col = QSpinBox()
        col.setMaximum(99999)
        col.setMinimum(0)
        col.setValue(3)
        token = QLineEdit()
        token.setText(',')
        augmented = QCheckBox()

        table.setCellWidget(current_row, 0, var_name)
        table.setCellWidget(current_row, 1, filename)
        table.setCellWidget(current_row, 2, key)
        table.setCellWidget(current_row, 3, line)
        table.setCellWidget(current_row, 4, col)
        table.setCellWidget(current_row, 5, token)
        table.setCellWidget(current_row, 6, augmented)

        table.resizeColumnsToContents()

    def remove_response_variable(self, dlg):
        table = dlg.table_ost_resp_var
        selected_row = table.currentRow()
        table.removeRow(selected_row)

    def get_response_var(self, dlg):
        table = dlg.table_ost_resp_var
        rows = table.rowCount()
        cols = table.columnCount()
        response_vars = []

        for row in range(rows):
            tmp_response_vars = []
            for col in range(cols):
                current_widget = table.cellWidget(row, col)
                if isinstance(current_widget, QLineEdit):
                    if col == 5:    # It's the token column, must be between ' '
                        tmp_response_vars.append("'" + current_widget.text() + "'")
                    else:
                        tmp_response_vars.append(current_widget.text())
                elif isinstance(current_widget, QgsFileWidget):
                    file = path.basename(current_widget.filePath())
                    tmp_response_vars.append(file + ' ; ')
                elif isinstance(current_widget, QSpinBox):
                    tmp_response_vars.append(current_widget.value())
                elif isinstance(current_widget, QCheckBox):
                    if current_widget.isChecked():
                        tmp_response_vars.append('yes')
                    else:
                        tmp_response_vars.append('no')
            response_vars.append(tmp_response_vars)

        return response_vars

    def set_algorithm_settings(self, dlg):
        bisectionalg = {'MaxOuterIterations': 50,
                        'MaxInnerIterations': 20
                        }
        levmar = {'InitialLambda': 10.00,
                  'LambdaScaleFactor': 1.10,
                  'MoveLimit': 0.10,
                  'AlgorithmConvergenceValue': 0.0001,
                  'LambdaPhiRatio': 0.30,
                  'LambdaRelReduction': 0.01,
                  'MaxLambdas': 10,
                  'MaxIterations': 30
                  }
        levmar2 = {'InitialLambda': 10.00,
                   'LambdaScaleFactor': 1.10,
                   'MoveLimit': 0.10,
                   'AlgorithmConvergenceValue': 0.0001,
                   'LambdaPhiRatio': 0.30,
                   'LambdaRelReduction': 0.01,
                   'MaxLambdas': 10,
                   'MaxIterations': 30,
                   'NumMultiStarts': 1
                   }
        gridalg = {'Dimensions': None,
                   'EvalsPerIter': 1000
                   }
        steepdescalg = {'ConvergenceVal': 0.000001,
                        'MaxIterations': 20
                        }
        appso = {'SwarmSize': 20,
                 'NumGenerations': 50,
                 'ConstrictionFactor': 1.00,
                 'CognitiveParam': 2.00,
                 'SocialParam': 2.00,
                 'InertiaWeight': 1.2,
                 'InertiaReductionRate': 0.10
                 }
        beers = {'NumSamples': 25}
        simulatedalg = {'NumInitialTrials': 100,
                        'TemperatureScaleFactor': 0.90,
                        'OuterIterations': 20,
                        'InnerIterations': 10,
                        'ConvergenceVal': 0.001,
                        'FinalTemperature': None,
                        'TransitionMethod': ['Gauss', 'Uniform']
                        }
        ddsalg = {'PerturbationValue': 0.2,
                  'MaxIterations': 100,
                  'UseParamValues': ['UseRandomParamValues', 'UseInitialParamValues']
                  }
        sceua = {'Budget': 1000,
                 'LoopStagnationCriteria': 5,
                 'PctChangeCriteria': 0.01,
                 'PopConvCriteria': 0.001,
                 'NumComplexes': 3,
                 'NumPointsPerComplex': 19,
                 'NumPointsPerSubComplex': 10,
                 'NumEvolutionSteps': 19,
                 'MinNumberOfComplexes': 3,
                 'UseInitialPoint': ['no', 'yes']
                 }
        fletchreevesalg = {'ConvergenceVal': 0.000001,
                           'MaxStalls': 3,
                           'MaxIterations': 20
                           }
        powellalg = {'ConvergenceVal': 0.000001,
                     'MaxIterations': 20
                     }
        particleswarm = {'SwarmSize': 20,
                         'NumGenerations': 50,
                         'ConstrictionFactor': 1.00,
                         'CognitiveParam': 2.00,
                         'SocialParam': 2.00,
                         'InertiaWeight': 1.2,
                         'InertiaReductionRate': 0.10,
                         'InitPopulationMethod': ['random', 'LHS', 'QuadTree'],
                         'ConvergenceVal': 0.0001
                         }
        geneticalg = {'ParallelMethod': ['synchronous', 'asynchronous'],
                      'InitPopulationMethod': ['random', 'LHS', 'QuadTree'],
                      'PopulationSize': 50,
                      'MutationRate': 0.05,
                      'Survivors': 1,
                      'NumGenerations': 10,
                      'ConvergenceVal': 0.0001
                      }
        samplingalg = {'MaxEvaluations': 100}
        ddsau = {'PerturbationValue': 0.2,
                 'NumSearches': 25,
                 'MinItersPerSearch': 30,
                 'MaxItersPerSearch': 70,
                 'ParallelSearches': ['no', 'yes'],
                 'Threshold': 1000,
                 'Randomize': ['no', 'yes'],
                 'ReviseAU': ['no', 'yes']
                 }
        metropolissampler = {'SamplesPerIter': 10,
                             'NumDesired': 10,
                             'BurnInSamples': 0,
                             'MaxSamples': 100,
                             'LikelihoodType': ['Stedinger', 'Beven'],
                             'ShapingFactor': 0.5,  # Only if Beven!!!
                             'TelescopeRate': 0
                             }
        glue = {'SamplesPerIter': 10,
                'NumBehavioral': 10,
                'MaxSamples': 100,
                'Threshold': 1000
                }
        rejectionsample = {'SamplesPerIter': 10,
                           'NumDesired': 10,
                           'BurnInSamples': 0,
                           'MaxSamples': 100,
                           'LikelihoodType': ['Stedinger', 'Beven'],
                           'ShapingFactor': 0.5,  # Only if Beven!!!
                           'TelescopeRate': 0,
                           'MinWSSE': 1000000000000
                           }
        padds = {'PerturbationValue': 0.2,
                 'MaxIterations': 50,
                 'SelectionMetric': ['ExactHyperVolumeContribution', 'Random', 'CrowdingDistance',
                                     'EstimatedHyperVolumeContribution']
                 }
        smooth = {'SamplesPerIter': 20,
                  'NumIterations': 50
                  }
        algorithms = {'GeneticAlgorithm': geneticalg,
                      'BinaryGeneticAlgorithm': geneticalg,
                      'ShuffledComplexEvolution': sceua,
                      'BisectionAlgorithm': bisectionalg,
                      'SamplingAlgorithm': samplingalg,
                      'ParticleSwarm': particleswarm,
                      'APPSO': appso,
                      'PSO-GML':'',
                      'SimulatedAnnealing': simulatedalg,
                      'DiscreteSimulatedAnnealing': simulatedalg,
                      'VanderbiltSimulatedAnnealing': simulatedalg,
                      'Levenberg-Marquardt': levmar,
                      'GML-MS': levmar2,
                      'Powell': powellalg,
                      'Steepest-Descent': steepdescalg,
                      'Fletcher-Reeves ': fletchreevesalg,
                      'RegressionStatistics':'',
                      'Jacobian':'',
                      'Hessian':'',
                      'Gradient':'',
                      'ModelEvaluation':'',
                      'GridAlgorithm': gridalg,
                      'DDS': ddsalg,
                      'DDSAU': ddsau,
                      'ParallelDDS': ddsalg,
                      'DiscreteDDS': ddsalg,
                      'GLUE': glue,
                      'RejectionSampler': rejectionsample,
                      'MetropolisSampler': metropolissampler,
                      'SMOOTH': smooth,
                      'PADDS': padds,
                      'ParaPADDS': padds,
                      'BEERS': beers,
                      }

        table_program_type = dlg.table_ost_algorithm
        selected_program_type = dlg.combo_programtype.currentText()
        parameters = algorithms[selected_program_type]

        while table_program_type.rowCount() > 0:
            table_program_type.removeRow(0)

        for key, value in parameters.items():
            current_row = table_program_type.rowCount()  # Get the number of rows the table has
            table_program_type.insertRow(current_row)  # Inserts a new row below the last row
            parameter_widget = QLabel()
            parameter_widget.setText(key)

            if isinstance(value, list):
                value_widget = QComboBox()
                value_widget.addItems(value)
            else:
                value_widget = QLineEdit()
                value_widget.setText(str(value))

            table_program_type.setCellWidget(current_row, 0, parameter_widget)
            table_program_type.setCellWidget(current_row, 1, value_widget)

        table_program_type.resizeColumnsToContents()


    def set_objective_function_settings(self, dlg):
        gcop = {'CostFunction': None,
                'PenaltyFunction': ['MPM', 'APM', 'EPM']
                }
        table_objective_function = dlg.table_ost_function
        selected_objective_function = dlg.combo_ost_objfunc.currentText()
        table_response_vars = dlg.table_ost_resp_var
        table_tied_response_vars = dlg.table_ost_tied_resp_var

        rows_response_vars = table_response_vars.rowCount()
        rows_tied_response_vars = table_tied_response_vars.rowCount()

        if rows_response_vars > 0 or rows_tied_response_vars > 0:
            response_vars = []
            for row in range(rows_response_vars):
                current_widget = table_response_vars.cellWidget(row, 0)
                if isinstance(current_widget, QLineEdit):
                    response_vars.append(current_widget.text())
            for row in range(rows_tied_response_vars):
                current_widget = table_tied_response_vars.cellWidget(row, 0)
                if isinstance(current_widget, QLineEdit):
                    response_vars.append(current_widget.text())
        else:
            return

        while table_objective_function.rowCount() > 0:
            table_objective_function.removeRow(0)

        if selected_objective_function == 'gcop':
            for variable in response_vars:  # Must use the response var!!!
                if not variable:
                    continue
                current_row = table_objective_function.rowCount()  # Get the number of rows the table has
                table_objective_function.insertRow(current_row)  # Inserts a new row below the last row
                parameter_widget = QLabel()
                parameter_widget.setText('CostFunction')
                value_widget = QLabel()
                value_widget.setText(variable)
                chk_selected = QCheckBox()
                chk_selected.setChecked(True)
                table_objective_function.setCellWidget(current_row, 0, parameter_widget)
                table_objective_function.setCellWidget(current_row, 1, value_widget)
                table_objective_function.setCellWidget(current_row, 2, chk_selected)
            current_row = table_objective_function.rowCount()
            table_objective_function.insertRow(current_row)
            penalty_widget = QLabel('PenaltyFunction')
            table_objective_function.setCellWidget(current_row, 0, penalty_widget)
            penalty_widget = QComboBox()
            penalty_widget.addItems(gcop['PenaltyFunction'])
            table_objective_function.setCellWidget(current_row, 1, penalty_widget)
            empty_widget = QLabel()
            table_objective_function.setCellWidget(current_row, 2, empty_widget)

            table_objective_function.resizeColumnsToContents()

    def get_gcop_settings(self, dlg):
        table = dlg.table_ost_function
        rows = table.rowCount()
        cols = table.columnCount()
        gcop_settings = []

        for row in range(rows):
            tmp_settings = []
            for col in range(cols):
                current_widget = table.cellWidget(row, col)
                if isinstance(current_widget, QLabel):
                    tmp_settings.append(current_widget.text())
                elif isinstance(current_widget, QComboBox):
                    tmp_settings.append(current_widget.currentText())
                elif isinstance(current_widget, QCheckBox):
                    if current_widget.isChecked():
                        gcop_settings.append(tmp_settings)
                    else:
                        pass
            if tmp_settings[0] == 'PenaltyFunction':
                gcop_settings.append(tmp_settings)
        return gcop_settings

    def get_algorithm_settings(self, dlg):
        table = dlg.table_ost_algorithm
        rows = table.rowCount()
        cols = table.columnCount()
        tmp_algorithm_settings = []

        for row in range(rows):
            tmp_settings = []
            for col in range(cols):
                current_widget = table.cellWidget(row, col)
                if isinstance(current_widget, QLabel):
                    tmp_settings.append(current_widget.text())
                elif isinstance(current_widget, QLineEdit):
                    tmp_settings.append(current_widget.text())
                elif isinstance(current_widget, QComboBox):
                    tmp_settings.append(current_widget.currentText())
            tmp_algorithm_settings.append(tmp_settings)

        algorithm_settings = []
        remove_next = False
        # Skips the "ShapingFactor" parameter if the LikelihoodType is Stedinger
        for row in tmp_algorithm_settings:
            if remove_next:
                remove_next = False
                continue
            if 'Stedinger' in row:
                remove_next = True
            algorithm_settings.append(row)

        return algorithm_settings

    def generate_model_executable_script(self, dlg):
        raven_mode = dlg.combo_ravenexe_mode.currentText()
        ostrich_mode = dlg.combo_ostrichexe_mode.currentText()
        extra_dirs = self.get_extra_dir(dlg)
        file_pairs = self.get_file_pairs(dlg)
        output_file = dlg.file_ost_exe.filePath()

        # Set the proper Raven execution command
        if ostrich_mode == 'Container':
            raven_path = 'Raven.exe'
        else:
            if raven_mode == 'Executable':
                raven_path = dlg.file_ravenexe.filePath()
            elif raven_mode == 'Flatpak':
                raven_path = 'flatpak run ca.uwaterloo.Raven'
            else:
                raven_path = 'Raven.exe'

        # Get an extra directory if one exists
        if extra_dirs:
            extra_dir = extra_dirs[0]
        else:
            extra_dir = ''

        # Get the file name of a pair in hopes it's the model name
        if file_pairs:
            model_name = path.splitext(path.basename(file_pairs[0][1]))[0]
        else:
            model_name = 'model_name'

        # Making sure the proper extension is used and generate the script
        file_path, extension = path.splitext(output_file)
        if platform == "linux" or platform == "linux2" or platform == 'darwin':
            if extension != '.sh':
                file_path += '.sh'
            else:
                file_path += extension

            # Write a bash script and make it executable
            with open(file_path, 'w') as script:
                script.write('#!/bin/bash\n\n')
                script.write('set -e\n')
                if extra_dir:
                    script.write('cd ' + extra_dir + '\n')
                script.write(raven_path + ' ' + model_name + ' -o output/\n')
                script.write('exit 0')
            subprocess.run(['chmod', '+x', file_path])

        elif platform == "win32":
            if extension != '.bat':
                file_path += '.bat'
            else:
                file_path += extension

            # Write a batch script and make it executable
            with open(file_path, 'w') as script:
                script.write('@echo off\n\n')
                if extra_dir:
                    script.write('cd ' + extra_dir + '\n')
                script.write(raven_path + ' ' + model_name + ' -o output/')
            subprocess.run(['attrib', '+x', file_path])

        print('Script generated.')
