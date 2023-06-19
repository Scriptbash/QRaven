from qgis.PyQt.QtWidgets import *

def add_chemical(self):
    table = self.dlg.table_geochem  # Get the custom geochemical table
    currentRow = table.rowCount()  # Get the number of rows the table has
    table.insertRow(currentRow)  # Inserts a new row below the last row
    combo_proc = QComboBox()
    combo_proc.addItems(proc)
    combo_alg = QComboBox()
    #combo_alg.addItems(decay_alg)
    txt_proc_name = QLineEdit()
    combo_constit1 = QComboBox()
    combo_constit1.setEditable(True)
    combo_constit2 = QComboBox()
    combo_constit2.setEditable(True)
    combo_constit2.setEnabled(False)
    combo_compart = QComboBox()
    combo_compart.setEditable(True)

    table.setCellWidget(currentRow, 0, combo_proc)  # Sets the new combobox in the first column and in the new row
    table.setCellWidget(currentRow, 1, combo_alg)
    table.setCellWidget(currentRow, 2, txt_proc_name)
    table.setCellWidget(currentRow, 3, combo_constit1)
    table.setCellWidget(currentRow, 4, combo_constit2)
    table.setCellWidget(currentRow, 5, combo_compart)

    combo_proc.currentIndexChanged.connect(lambda: set_algorithms(self, currentRow))

def set_algorithms(self, row):
    table = self.dlg.table_geochem
    combo_proc = table.cellWidget(row, 0)
    combo_alg = table.cellWidget(row, 1)
    combo_alg.clear()
    combo_constit2 = table.cellWidget(row, 4)

    proc = combo_proc.currentText()

    if proc == 'Decay':
        combo_alg.addItems(decay_alg)
        combo_constit2.setEnabled(False)
    elif proc == 'Equilibrium':
        combo_alg.addItems(equilibrium_alg)
        combo_constit2.setEnabled(True)
    elif proc == 'Transformation':
        combo_alg.addItems(transformation_alg)
        combo_constit2.setEnabled(True)

def remove_chemical(self):
    table = self.dlg.table_geochem
    selectedRow = table.currentRow()
    table.removeRow(selectedRow)

def get_geochem(self):
    table = self.dlg.table_geochem
    rows = table.rowCount()
    cols = table.columnCount()
    processes = []
    for row in range(rows):
        tmp_processes = []
        for col in range(cols):
            current_Widget = table.cellWidget(row, col)
            if isinstance(current_Widget, QComboBox):
                if current_Widget.isEnabled():
                    tmp_processes.append(current_Widget.currentText())
                else:
                    tmp_processes.append('')

            elif isinstance(current_Widget, QLineEdit):
                tmp_processes.append(current_Widget.text())
        processes.append(tmp_processes)

    return processes



proc = ['', 'Decay', 'Equilibrium', 'Transformation']
decay_alg = ['DECAY_BASIC', 'DECAY_ZEROORDER', 'DECAY_LINEAR', 'DECAY_DENITRIF']
equilibrium_alg = ['EQUIL_FIXED_RATIO', 'EQUIL_LINEAR', 'EQUIL_LINEAR_SORPTION']
transformation_alg = ['TRANS_LINEAR', 'TRANS_NONLINEAR']
