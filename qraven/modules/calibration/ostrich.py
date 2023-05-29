from qgis.gui import QgsFileWidget


class Ostrich:
    def __init__(self):
        pass

    def add_file_pair(self, dlg):
        table = dlg.table_filepairs  # Get the file pairs table
        current_row = table.rowCount()  # Get the number of rows the table has
        table.insertRow(current_row)  # Inserts a new row below the last row
        template_file = QgsFileWidget()
        template_file.setStorageMode(QgsFileWidget.GetDirectory)
        model_input_file = QgsFileWidget()
        model_input_file.setStorageMode(QgsFileWidget.GetDirectory)

        table.setCellWidget(current_row, 0, template_file)
        table.setCellWidget(current_row, 1, model_input_file)

        table.resizeColumnsToContents()

    def remove_file_pair(self, dlg):
        table = dlg.table_filepairs
        selected_row = table.currentRow()
        table.removeRow(selected_row)

    def export_params(self, dlg):
        pass
