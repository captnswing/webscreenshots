# Take regular screenshots of preconfigured websites

##### Design ideas:

* save screenshots of configured websites in regular intervals as PNG or JPEG.
* allow for configuration of websites through easy web interface
* allow the easy comparison and exploration of the save screenshots for arbitrary times and time ranges
    - surfa på url http://appserver/svt.se/nyheter ger tillbaka senaste snapshot
    - surfa på url http://appserver/svt.se/nyheter/2012-11-27/12.23/ mappar mot snapshot som tagits närmast i tid

##### Implementation ideas:

* använd celerybeat för att varje 5:e minut gå igenom en lista av förkonfigurerade url:er
* för varje url, spara ned hela sidan som hel PNG och tumnagel.
* ladda upp PNG och tumnagel till S3
* 

### research for screenshot solutions

##### requirements:

* headless
* runs on virtualized linux (Vagrant, VMWare ESX, EC2)
* supports html5 & css3 & javascript & flash
* makes nice screenshots (fonts)
* optionally: supports http proxy

##### articles:

* [skookum.com/blog/dynamic-screenshots-on-the-server-with-phantomjs/](http://skookum.com/blog/dynamic-screenshots-on-the-server-with-phantomjs/)
* [corpocrat.com/2008/08/26/capturing-a-screenshot-of-a-website](http://corpocrat.com/2008/08/26/capturing-a-screenshot-of-a-website)
* [news.ycombinator.com/item?id=1256381](http://news.ycombinator.com/item?id=1256381)
* [gfdsa.gfdsa.org/2012/08/making-web-pages-screenshots-with-webkit2png-flash-included](http://gfdsa.gfdsa.org/2012/08/making-web-pages-screenshots-with-webkit2png-flash-included)
* [coderholic.com/pywebshot-generate-website-thumbnails-using-python/](http://www.coderholic.com/pywebshot-generate-website-thumbnails-using-python/)
* [blogs.uni-osnabrueck.de/rotapken/2008/12/03/create-screenshots-of-a-web-page-using-python-and-qtwebkit/](http://www.blogs.uni-osnabrueck.de/rotapken/2008/12/03/create-screenshots-of-a-web-page-using-python-and-qtwebkit/)

##### alternatives:

* [khtml2png](http://khtml2png.sourceforge.net)
* [python-webkit2png](https://github.com/AdamN/python-webkit2png)
* [webkit2png](http://www.paulhammond.org/webkit2png)
* [cutycapt](http://cutycapt.sourceforge.net)
* [pywebshot](https://github.com/coderholic/PyWebShot)
* [phantom.js](http://phantomjs.org/)
* [wkhtmltopdf](http://code.google.com/p/wkhtmltopdf/)
* [htmlshots](https://github.com/w3p/htmlshots)

##### webservices:

* [node-urlshot](http://node-urlshot.herokuapp.com), example with [svt.se](http://node-urlshot.herokuapp.com/?url=http://svt.se/&viewport=1280x900&format=jpg)
* [thumbalizr](http://www.thumbalizr.com/)
* [thumbalizr alternatives](http://www.moreofit.com/similar-to/www.thumbalizr.com/Top_10_Sites_Like_Thumbalizr/)
* loads of others

### S3 Bucket

    - world readable
    - 90 days expiration for files
    - cloudfront enabled
    - custom IAM user with custom policy

### run celery workers and flower with supervisor

    # start supervisord, starts celery & flower automatically
    supervisor

    # check logs
    supervisorctl tail celeryd

    # stop celery & flower
    supervisorctl stop celeryd
    supervisorctl stop flower

    # stop supervisord
    kill -HUP `cat /tmp/supervisord.pid`

### Heroku

following https://devcenter.heroku.com/articles/python
    
    curl -O http://assets.heroku.com/heroku-toolbelt/heroku-toolbelt.pkg
    sudo installer -pkg heroku-toolbelt.pkg -target '/'
    heroku login

### install virtualbox

    curl -O http://dlc.sun.com.edgesuite.net/virtualbox/4.2.6/VirtualBox-4.2.6-82870-OSX.dmg
    hdid VirtualBox-4.2.6-82870-OSX.dmg
    sudo installer -target '/' -pkg /Volumes/VirtualBox/VirtualBox.pkg
    diskutil eject /Volumes/VirtualBox
    rm VirtualBox-4.2.6-82870-OSX.dmg

### install rvm & ruby

    curl -L https://get.rvm.io | bash -s stable --ruby
    rvm --default use 1.9.3

### install vagrant &

    gem install vagrant
    vagrant box add precise64 http://files.vagrantup.com/precise64.box

### install chef tools

    sudo ln -s /usr/bin/llvm-gcc-4.2 /usr/bin/gcc-4.2
    gem install bundler yajl-ruby nokogiri
    gem install ffi -v 1.0.11
    gem install net-ssh net-ssh-multi fog highline
    gem install knife-ec2 knife-solo
