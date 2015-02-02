FROM python:2.7 # debian jessie

ENV DEBIAN_FRONTEND noninteractive

RUN sed -i 's|main$|main contrib|g' /etc/apt/sources.list \
    && apt-get -y update \
    && apt-get -y install libfreetype6-dev libfontconfig1-dev libicu-dev libfreetype6-dev libpng12-dev \
                          libwebp-dev libjpeg-dev ttf-mscorefonts-installer unzip \
    && apt-get -y autoremove

RUN curl -LO https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-1.9.8-linux-x86_64.tar.bz2 \
    && bzcat phantomjs-1.9.8-linux-x86_64.tar.bz2 | tar xf - \
    && mv phantomjs-1.9.8-linux-x86_64 /opt/phantomjs-1.9.8 \
    && ln -s /opt/phantomjs-1.9.8 /opt/phantomjs \
    && ln -s /opt/phantomjs/bin/phantomjs /usr/local/bin/phantomjs \
    && rm phantomjs-1.9.8-linux-x86_64.tar.bz2

RUN curl -L https://github.com/n1k0/casperjs/zipball/1.1-beta3 -o casperjs-1.1-beta3.zip \
    && unzip casperjs-1.1-beta3.zip \
    && mv n1k0-casperjs-* /opt/casperjs-1.1-beta3 \
    && ln -s /opt/casperjs-1.1-beta3 /opt/casperjs \
    && ln -s /opt/casperjs/bin/casperjs /usr/local/bin/casperjs \
    && rm casperjs-1.1-beta3.zip

ADD localfonts.conf /etc/fonts/local.conf
RUN fc-cache -f -v

RUN mkdir /code
WORKDIR /code
ADD . /code/

RUN pip install -r requirements.txt
