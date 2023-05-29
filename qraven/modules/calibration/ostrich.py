from qgis.gui import QgsFileWidget
from qgis.PyQt.QtWidgets import *
from ..PyRavenR import readRavenParams, readRVPtemplate, getDefaultParamValue
from pathlib import Path
from os import path


class Ostrich:
    def __init__(self):
        pass

    def add_file_pair(self, dlg):
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
        table = dlg.table_filepairs
        selected_row = table.currentRow()
        table.removeRow(selected_row)

    def load_parameters(self, dlg):
        script_dir = Path(__file__).parent.parent.parent
        raven_parameters_file = path.join(script_dir, "ext_data/RavenParameters.dat")
        rvn_rvp_params = readRavenParams(raven_parameters_file)  # Gathers all rvp params
        # print(rvn_rvp_params)
        params_name_list = [i[0] for i in rvn_rvp_params]   # List with all rvp params name

        file_pairs = self.get_file_pairs(dlg)
        table = dlg.table_ost_params

        self.clear_table(table)

        for pairs in file_pairs:
            template = pairs[0]
            rvp_template_params = readRVPtemplate(template)

        for line in rvp_template_params:
            # for col in line:
            for param in params_name_list:
                if param in line:
                    chk_params = QCheckBox()
                    chk_params.setChecked(True)
                    lbl_params = QLabel()
                    lbl_params.setText(param)
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

        for param in params:
            current_row = table.rowCount()  # Get the number of rows the table has
            table.insertRow(current_row)  # Inserts a new row below the last row
            lbl_param = QLabel()
            lbl_param.setText(param)

            table.setCellWidget(current_row, 0, lbl_param)
        table.resizeColumnsToContents()

    def get_params(self, dlg):
        table = dlg.table_ost_params
        rows = table.rowCount()
        params = []
        for row in range(rows):
            checkbox = table.cellWidget(row, 0)
            param = table.cellWidget(row, 1)
            if checkbox.isChecked():
                params.append(param.text())
            else:
                pass

        return params

    def export_params(self, dlg):
        pass

    def clear_table(self, table):
        while table.rowCount() > 0:
            table.removeRow(0)
