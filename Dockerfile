FROM ubuntu:jammy
ENV LANG=en_EN.UTF-8 \
    LANGUAGE=en_US:en \ 
    LC_ALL=en_US.UTF-8 \
    DEBIAN_FRONTEND=noninteractive \
    DISPLAY=:99 
SHELL ["/bin/bash", "-c"]
RUN apt-get update \
    && apt-get install --no-install-suggests --allow-unauthenticated -y \
        gnupg \
        ca-certificates \
        software-properties-common \
        wget \
        locales \
    && localedef -i en_US -f UTF-8 en_US.UTF-8 \
    && apt install -y qgis qgis-plugin-grass \
    && apt install -y grass-gui \
    && apt install -y grass-dev \
    && apt install -y saga \
    && apt install -y pip \
    && apt install -y xvfb \
    && python3 -m pip install https://github.com/dustming/basinmaker/archive/master.zip \
    && python3 -m pip install simpledbf grass_session \
    && python3 -m pip install joblib \
    && python3 -m pip install grass_session \
    && python3 -m pip install pandas \
    && python3 -m pip install scipy \
    && python3 -m pip install argparse \
    && python3 -m pip install geopandas \
    && python3 -m pip install netCDF4 \
    && python3 -m pip install GDAL \
    && python3 -m pip install numpy \
    && echo "export GISBASE='/usr/lib/grass78'" >> ~/.bashrc \
    && echo "export QGIS_PREFIX_PATH='/usr'" >> ~/.bashrc \
    && echo "export PYTHONPATH=\$PYTHONPATH:'/usr/lib/grass78/etc/python'" >> ~/.bashrc \
    && echo "export PYTHONPATH=\$PYTHONPATH:'/usr/share/qgis/python/plugins'" >> ~/.bashrc \
    && echo "export PYTHONPATH=\$PYTHONPATH:'/usr/share/qgis/python'" >> ~/.bashrc \
    && source /root/.bashrc \
    && mkdir -p ~/BasinMaker/Data \
    #&& mkdir -p ~/BasinMaker/Data/{bkf_width,DEM,extent_poly,flow_direction,hybasin,lakes,landuse,soil,stations} \
    && mkdir ~/BasinMaker/Data/bkf_width \
    && mkdir ~/BasinMaker/Data/DEM \
    && mkdir ~/BasinMaker/Data/extent_poly \
    && mkdir ~/BasinMaker/Data/flow_direction \
    && mkdir ~/BasinMaker/Data/hybasin \
    && mkdir ~/BasinMaker/Data/lakes \
    && mkdir ~/BasinMaker/Data/landuse \
    && mkdir ~/BasinMaker/Data/soil \
    && mkdir ~/BasinMaker/Data/stations \
    && mkdir -p ~/Gridweights/Data \
    && cd ~/BasinMaker \
    && wget https://raw.githubusercontent.com/Scriptbash/QRaven/main/create_RVH.py \
    && cd ~/Gridweights \
    && wget https://raw.githubusercontent.com/julemai/GridWeightsGenerator/main/derive_grid_weights.py \
    && grass -c EPSG:4326 ~/grass_tmp --text --exec g.extension r.clip\
    && grass -c EPSG:4326 ~/grass_tmp2 --text --exec g.extension r.accumulate \
    && grass -c EPSG:4326 ~/grass_tmp3 --text --exec g.extension r.stream.basins \
    && grass -c EPSG:4326 ~/grass_tmp4 --text --exec g.extension r.stream.snap \
    && exit

