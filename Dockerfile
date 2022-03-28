FROM ubuntu:jammy
ENV LANG=en_EN.UTF-8 \
    DEBIAN_FRONTEND=noninteractive \
    DISPLAY=:99 
RUN apt-get update \
    && apt-get install --no-install-suggests --allow-unauthenticated -y \
        gnupg \
        ca-certificates \
        software-properties-common \
        wget \
        locales \
    && localedef -i en_US -f UTF-8 en_US.UTF-8 \
    && wget -qO - https://qgis.org/downloads/qgis-2021.gpg.key | gpg --no-default-keyring --keyring gnupg-ring:/etc/apt/trusted.gpg.d/qgis-archive.gpg --import \
    && chmod a+r /etc/apt/trusted.gpg.d/qgis-archive.gpg \
    && add-apt-repository "deb https://qgis.org/ubuntu $(lsb_release -c -s) main" \
    && apt-get update \
    && apt-get install -y qgis qgis-plugin-grass \
    && apt install -y grass-gui \
    && apt install -y grass-dev \
    && apt install -y pip \
    && apt install xvfb \
    && python3 -m pip install https://github.com/dustming/basinmaker/archive/refs/tags/v2.2.6.zip \
    && python3 -m pip install simpledbf grass_session \
    && python3 -m pip install joblib \
    && python3 -m pip install grass_session \
    && python3 -m pip install pandas \
    && echo "export GISBASE='/usr/lib/grass78'" >> ~/.bashrc \
    && echo "export QGIS_PREFIX_PATH='/usr'" >> ~/.bashrc \
    && grass -c ~/grass_tmp --text --exec g.extension r.clip\
    && grass -c ~/grass_tmp2 --text --exec g.extension r.accumulate \
    && grass -c ~/grass_tmp3 --text --exec g.extension r.stream.basins \
    && grass -c ~/grass_tmp4 --text --exec g.extension r.stream.snap \
    && exit

