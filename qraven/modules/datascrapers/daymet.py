import requests
class Daymet:

    def __int__(self):
        pass

    def define_area(self):
        pass

    def get_search_criteria(self, dlg):
        output_folder = dlg.file_daymet_output.filePath()
        start_date = dlg.date_daymet_start_date.date().toPyDate()
        end_date = dlg.date_daymet_end_date.date().toPyDate()
        selected_variables = dlg.list_daymet_variables.selectedItems()
        variables = ""
        if selected_variables:
            for item in selected_variables:
                variables += item.text() + ' '
        if start_date and end_date and variables:
            dlg.lbl_daymet_error.clear()
            self.get_data(start_date, end_date, variables, output_folder)
        else:
            dlg.lbl_daymet_error.setText("At least one variable must be selected.")

    def get_data(self, start, end, var, output):
        region = "na"
        north = "36.61"
        west = "-85.37"
        east = "-81.29"
        south = "33.57"

        for variable in var.split():
            for year in range(int(start.year), int(end.year)+1):
                url = "https://thredds.daac.ornl.gov/thredds/ncss/grid/ornldaac/2129/daymet_v4_daily_" + region + "_" \
                        + variable + '_' + str(year) + ".nc?var=lat&var=lon&var=" + variable + '&north=' + north + \
                        "&west=" + west + "&east=" + east + "&south=" + south + \
                        "&disableProjSubset=on&horizStride=1&time_start=" + \
                        str(start) + "T12:00:00Z&time_end=" + str(end) + "T12:00:00Z&timeStride=1&accept=netcdf"

                with requests.get(url, stream=True) as r:
                    r.raise_for_status()
                    with open(output, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)

