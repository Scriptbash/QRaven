<p align="center">
<img alt="QRaven" src= "https://user-images.githubusercontent.com/98601298/206937821-d1d04252-11ac-4094-974f-fda63e1f4cca.png" width="300">
</p>

<h3 align="center">A QGIS Plugin to help generate input files for Raven</h3>

<p align="center">

<a href="https://github.com/Scriptbash/QRaven/releases">
    <img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/Scriptbash/QRaven?display_name=tag">
</a>
<a href='https://qraven.readthedocs.io/en/latest/?badge=latest'>
    <img src='https://readthedocs.org/projects/qraven/badge/?version=latest' alt='Documentation Status' />
</a>
<a href="https://github.com/Scriptbash/QRaven/commits/main">
    <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/Scriptbash/Qraven">
</a>
</p>

---




## Description
<p align="justify">
QRaven aims to simplify the creation of the input files for the Raven hydrological modelling framework. It allows the user to choose all the options for the primary input file (.rvi) and it automates the setup, as well as the use of the BasinMaker python library for the HRU/Basin definition file (.rvh). It can run models, draw hydrographs and open RavenView using the default web browser. QRaven can also automatically fill the classed parameter input file (.rvp) using default values and it can generate grid weights blocks using the GridWeightGenerator script.

</p>

## Get started
<p align ="justify">
To get started, head over to the QRaven <a href='https://qraven.readthedocs.io'>documentation page</a>.
<p>

## Contribute
<p align ="justify">
If you want to get involved with QRaven's development, please read the <a href="https://qraven.readthedocs.io/en/latest/contribute.html">contribution guide.</a>
</p>

## Credits
<p align ="justify">
<ul>
<li>The BasinMaker tools used in the plugins are developped by Ming and its official website can be found at : http://hydrology.uwaterloo.ca/basinmaker </li>
<li> The GridWeights Generator is made by Julie and the script can be found at : https://github.com/julemai/GridWeightsGenerator </li>
<li>The Auto fill rvp template feature is heavily based on RavenR's rvn_rvp_fill_template function by Robert Chlumsky : https://github.com/rchlumsk/RavenR/blob/master/R/rvn_rvp_fill_template.R </li>
</ul>
</p>

## Help
<p align ="justify">
If you run into any issue, have a question or feedback while using QRaven, please open an issue here : https://github.com/Scriptbash/QRaven/issues
</p>
