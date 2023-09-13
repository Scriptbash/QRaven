from ..utilities import download_request, extract_archive


class SoilTypeDownload:

    def cansis(self, dlg, output):
        url = 'https://sis.agr.gc.ca/cansis/nsdb/slc/v2.2/slc_v2r2_canada.zip'
        dlg.lbl_progressbar.setText('Downloading soil layer')
        output += '/soil.zip'
        download_request(self, url, output)
        dlg.lbl_progressbar.setText('Extracting...')
        extract_archive(output)