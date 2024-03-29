<p align="center">
<img alt="QRaven" src= "https://github.com/Scriptbash/QRaven/blob/main/logo_w_outline.png?raw=true" width="300">
</p>

<h3 align="center">A QGIS Plugin to help generate input files for Raven</h3>

<p align="center">

<a href="https://github.com/Scriptbash/QRaven/releases">
    <img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/Scriptbash/QRaven?display_name=tag"/>
</a>
<a href='https://qraven.readthedocs.io/en/latest/?badge=latest'>
    <img src='https://readthedocs.org/projects/qraven/badge/?version=latest' alt='Documentation Status' />
</a>
<a href="https://github.com/Scriptbash/QRaven/actions/workflows/docker-image.yml">
    <img alt="GitHub Workflow Status" src="https://github.com/Scriptbash/QRaven/actions/workflows/docker-image.yml/badge.svg">
</a>
<a href='https://hub.docker.com/r/scriptbash/qraven/tags'>
    <img alt="Docker Pulls" src="https://img.shields.io/docker/pulls/scriptbash/qraven">
</a>
</br></br>
<a href='https://ko-fi.com/A0A6ME7SJ' target='_blank'><img height='32' style='border:0px;height:32px;' src='https://storage.ko-fi.com/cdn/kofi1.png?v=3' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>

</p>

---

## Description
<p align="justify">
QRaven aims to simplify the creation of the input files for the Raven hydrological modelling framework. It allows users to generate .rvi files and use multiple tools using a graphical user interface. It also includes several features to automate and ease the setup of Raven models.
</p>

## Features overview
<ul>
<li>Generate .rvi files from templates or from scratch</li>
<li>Automate the setup and the use of the BasinMaker Python library using Podman or Docker</li>
<li>Associate NetCDF files to HRUs using the GridWeightGenerator script</li>
<li>Search hydrometric stations from the DPPHC and the Water Office</li>
<li>Download and convert hydrometric data into .rvt files</li>
<li>Create a shapefile with all the stations from which hydrometric data was downloaded</li>
<li>Download GIS data and preprocess it to be ready to be used with BasinMaker</li>
<li>Run models in a container, using Flatpak or an executable</li>
<li>Draw hydrographs</li>
<li>Open RavenView in the user's default web browser</li>
<li>Automatically fill .rvp template files</li>
</ul>

## Get started
<p align ="justify">
To get started, head over to the QRaven <a href='https://qraven.readthedocs.io'>documentation page</a>.
<p>

## Contribute
<p align ="justify">
If you want to get involved with QRaven's development, please read the <a href="https://qraven.readthedocs.io/en/latest/contribute.html">contribution guide</a>.
</p>

## Credits
<p align ="justify">
<ul>
<li>The BasinMaker tools used in the plugins are developped by Ming and its official website can be found at : http://hydrology.uwaterloo.ca/basinmaker </li>
<li> The GridWeights Generator is made by Juliane and the script can be found at : https://github.com/julemai/GridWeightsGenerator </li>
<li>The Auto fill rvp template feature is heavily based on RavenR's rvn_rvp_fill_template function by Robert Chlumsky : https://github.com/rchlumsk/RavenR/blob/master/R/rvn_rvp_fill_template.R </li>
</ul>
</p>

## Help
<p align ="justify">
If you run into any issue while using QRaven, have a question or want to share your feedback, please open an issue here : https://github.com/Scriptbash/QRaven/issues
</p>
