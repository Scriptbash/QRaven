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


class ThunderRaven:

    def __init__(self, qrvn):
        self.qrvn = qrvn
        self.dlg = self.qrvn.dlg

    def generate_model(self):
        # Todo Check if start/end date available for watershed streamflow data
        self.load_model()
        self.download_gis_data()

    def load_model(self):
        fullReset(self.qrvn)
        selected_structure = self.dlg.combo_thunder_structure.currentText()
        if selected_structure == 'AWBM':
            loadAwbm(self.qrvn)
        elif selected_structure == 'Canadian Shield':
            loadCanshield(self.qrvn)
        elif selected_structure == 'GR4J':
            loadGr4j(self.qrvn)
        elif selected_structure == 'HBV-EC':
            loadHbvec(self.qrvn)
        elif selected_structure == 'HBV-Light':
            loadHbvlight(self.qrvn)
        elif selected_structure == 'UBCWM':
            loadUbcwm(self.qrvn)
        elif selected_structure == 'HMETS':
            loadHmets(self.qrvn)
        elif selected_structure == 'MOHYSE':
            loadMohyse(self.qrvn)
        elif selected_structure == 'HYMOD':
            loadHymod(self.qrvn)
        elif selected_structure == 'HYPR':
            loadHypr(self.qrvn)
        elif selected_structure == 'Routing-only':
            load_routing_only(self.qrvn)

    def download_gis_data(self):
        self.dlg.stackedWidget.setCurrentIndex(4)
        self.dlg.sidemenu.setCurrentRow(4)
        QApplication.processEvents()
        output = self.dlg.file_thunder_output.filePath()
        input_polygon = self.dlg.file_thunder_polygon.filePath()
        output_gis = output + '/BasinMaker/Data'
        make_folder(output + '/BasinMaker')
        make_folder(output_gis)
        self.dlg.chk_download_dem.setChecked(True)
        self.dlg.chk_download_flowdir.setChecked(True)
        self.dlg.chk_download_lakes.setChecked(True)
        self.dlg.chk_download_bankfull.setChecked(True)
        self.dlg.chk_download_landuse.setChecked(True)
        self.dlg.chk_download_soil.setChecked(True)
        self.dlg.file_gis_download_output.setFilePath(output_gis)
        self.dlg.file_gis_clip_layer.setFilePath(input_polygon)
        self.dlg.btn_downloadgisdata.click()
