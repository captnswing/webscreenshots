FROM python:2.7

ENV DEBIAN_FRONTEND noninteractive
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

RUN sed -i "/^# deb .* multiverse$/ s/^# //" /etc/apt/sources.list \
    && apt-get -y update \
    && apt-get install -y unzip libfreetype6 fontconfig

RUN curl -LO http://ftp.de.debian.org/debian/pool/contrib/m/msttcorefonts/ttf-mscorefonts-installer_3.6_all.deb \
    && apt-get install -y xfonts-utils wget cabextract \
    && apt-get install -f -y \
    && dpkg -i ttf-mscorefonts-installer_3.6_all.deb \
    && rm ttf-mscorefonts-installer_3.6_all.deb

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

ADD provisioning/localfonts.conf /etc/fonts/local.conf
RUN fc-cache -f -v

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
EXPOSE 8000

#RUN casperjs screencapture_casperjs.js http://svt.se svt.jpg
#RUN ls -l /usr/share/fonts/truetype/msttcorefonts/
#RUN fc-match "Helvetica Neue"
#RUN fc-match Georgia
#CMD ["/bin/bash"]
