FROM python:2.7

ENV DEBIAN_FRONTEND noninteractive
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

RUN sed -i "/^# deb .* multiverse$/ s/^# //" /etc/apt/sources.list \
    && apt-get -y update \
    && apt-get install -y unzip libfreetype6 fontconfig mlocate

RUN curl -LO http://ftp.de.debian.org/debian/pool/contrib/m/msttcorefonts/ttf-mscorefonts-installer_3.6_all.deb \
    && apt-get install -y xfonts-utils wget cabextract \
    && apt-get install -f -y \
    && dpkg -i ttf-mscorefonts-installer_3.6_all.deb \
    && rm ttf-mscorefonts-installer_3.6_all.deb
    && updatedb

RUN curl -LO https://dl.dropbox.com/u/435971/posts/2012-12-27/localfonts.conf \
    && mv localfonts.conf /etc/fonts/local.conf \
    && fc-cache -f -v

RUN curl -LO https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-1.9.8-linux-x86_64.tar.bz2 \
    && bzcat phantomjs-1.9.8-linux-x86_64.tar.bz2 | tar xf - \
    && mv phantomjs-1.9.8-linux-x86_64 /opt \
    && ln -s /opt/phantomjs-1.9.8-linux-x86_64 /opt/phantomjs \
    && ln -s /opt/phantomjs/bin/phantomjs /usr/local/bin/phantomjs \
    && rm phantomjs-1.9.8-linux-x86_64.tar.bz2

RUN curl -L https://github.com/n1k0/casperjs/zipball/1.1-beta3 -o casperjs-1.1-beta3.zip \
    && unzip casperjs-1.1-beta3.zip \
    && mv n1k0-casperjs-* /opt/casperjs-1.1-beta3 \
    && ln -s /opt/casperjs-1.1-beta3 /opt/casperjs \
    && ln -s /opt/casperjs/bin/casperjs /usr/local/bin/casperjs \
    && rm casperjs-1.1-beta3.zip

RUN mkdir /code
WORKDIR /code

#RUN casperjs screencapture_casperjs.js http://svt.se svt.jpg
#RUN ls -l /usr/share/fonts/truetype/msttcorefonts/
#RUN fc-match "Helvetica Neue"
#RUN fc-match Georgia

CMD ["/bin/bash"]
