FROM ubuntu:14.04
MAINTAINER Frank Hoffsümmer "frank.hoffsummer@gmail.com"
ENV DEBIAN_FRONTEND noninteractive

# ---------
# MULTIVERSE
# ---------
RUN apt-get update
RUN apt-get install -y --no-install-recommends software-properties-common curl unzip
RUN apt-add-repository multiverse
RUN apt-get update

# ---------
# MS CORE FONTS
# ---------
# https://en.wikipedia.org/wiki/Core_fonts_for_the_Web
# from http://askubuntu.com/a/25614
RUN echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" | debconf-set-selections
RUN apt-get install -y --no-install-recommends fontconfig ttf-mscorefonts-installer
ADD localfonts.conf /etc/fonts/local.conf
RUN fc-cache -f -v

WORKDIR /opt

# ---------
# PHANTOMJS
# ---------
ENV PHANTOMJS_VERSION "phantomjs-2.1.1-linux-x86_64"
RUN curl -OLs https://bitbucket.org/ariya/phantomjs/downloads/${PHANTOMJS_VERSION}.tar.bz2 &&\
    bzcat ${PHANTOMJS_VERSION}.tar.bz2 | tar xf - &&\
    ln -s ${PHANTOMJS_VERSION} phantomjs &&\
    rm ${PHANTOMJS_VERSION}.tar.bz2

# ---------
# CASPERJS
# ---------
ENV CASPERJS_VERSION "casperjs-1.1.3"
RUN curl -Ls https://codeload.github.com/casperjs/casperjs/zip/1.1.3 -o ${CASPERJS_VERSION}.zip &&\
    unzip ${CASPERJS_VERSION}.zip &&\
    ln -s ${CASPERJS_VERSION} casperjs &&\
    rm ${CASPERJS_VERSION}.zip

ENTRYPOINT ["/opt/phantomjs/bin/phantomjs"]
