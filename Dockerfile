ARG ARCH=
FROM ${ARCH}ubuntu:jammy
#FROM arm64v8/ubuntu:jammy
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
        qgis qgis-plugin-grass \
        grass-gui \
        grass-dev \
        saga \
        pip \
        xvfb \
        mpich \
        netcdf-bin \
    && localedef -i en_US -f UTF-8 en_US.UTF-8 \
    && python3 -m pip install https://github.com/dustming/basinmaker/archive/master.zip \
        simpledbf \
        grass_session \
        joblib \
        pandas \
        scipy \
        argparse \
        geopandas \
        netCDF4 \
        GDAL \
        numpy \
    && echo "export GISBASE='/usr/lib/grass78'" >> ~/.bashrc \
    && echo "export QGIS_PREFIX_PATH='/usr'" >> ~/.bashrc \
    && echo "export PYTHONPATH=\$PYTHONPATH:'/usr/lib/grass78/etc/python'" >> ~/.bashrc \
    && echo "export PYTHONPATH=\$PYTHONPATH:'/usr/share/qgis/python/plugins'" >> ~/.bashrc \
    && echo "export PYTHONPATH=\$PYTHONPATH:'/usr/share/qgis/python'" >> ~/.bashrc \
    && source /root/.bashrc \
    && mkdir -p ~/BasinMaker/Data/{bkf_width,DEM,extent_poly,flow_direction,hybasin,lakes,landuse,soil,stations} \
    && mkdir -p ~/Gridweights/Data \
    && mkdir -p ~/Raven \
    && mkdir -p ~/Ostrich \
    && cd ~/BasinMaker \
    && wget https://raw.githubusercontent.com/Scriptbash/QRaven/main/create_RVH.py \
    && cd ~/Gridweights \
    && wget https://raw.githubusercontent.com/julemai/GridWeightsGenerator/main/derive_grid_weights.py \
    && cd ~/Raven \
    && wget https://github.com/Scriptbash/QRaven/raw/main/Executables/Linux/Raven.exe \
    && chmod +x Raven.exe \
    && cd ~/Ostrich \
    && wget https://github.com/Scriptbash/QRaven/raw/main/Executables/Linux/OstrichMPI \
    && chmod +x OstrichMPI \
    && grass -c EPSG:4326 ~/grass_tmp --text --exec g.extension r.clip\
    && grass -c EPSG:4326 ~/grass_tmp2 --text --exec g.extension r.accumulate \
    && grass -c EPSG:4326 ~/grass_tmp3 --text --exec g.extension r.stream.basins \
    && grass -c EPSG:4326 ~/grass_tmp4 --text --exec g.extension r.stream.snap \
    && exit

