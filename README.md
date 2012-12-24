# Skärmdumpar av webbplatser

Grundidé / Krav:

1. spara regelbunden PNG snapshots och tumnaglar av valfria webbsidor och lagra de på S3
    - använd celerybeat för att varje 5:e minut gå igenom en lista av förkonfigurerade url:er
    - för varje url, spara ned hela sidan som hel PNG och tumnagel.
    - ladda upp PNG och tumnagel till S3

2. skapa en webbapplikation som tillåtar lätt utforskning av lagrade snapshots
    - surfa på url http://appserver/svt.se/nyheter ger tillbaka senaste snapshot
    - surfa på url http://appserver/svt.se/nyheter/2012-11-27/12.23/ mappar mot snapshot som tagits närmast i tid

## Utforskning 27 Nov 2012

Google sök efter olika alternativ som finns

- [www.paulhammond.org/webkit2png](http://www.paulhammond.org/webkit2png)
- [www.corpocrat.com/2008/08/26/capturing-a-screenshot-of-a-website](http://corpocrat.com/2008/08/26/capturing-a-screenshot-of-a-website)
- [news.ycombinator.com/item?id=1256381](http://news.ycombinator.com/item?id=1256381)

## Utforskning 12 Dec 2012

- There's thumbalizr
- http://www.moreofit.com/similar-to/www.thumbalizr.com/Top_10_Sites_Like_Thumbalizr/
- There's phantom.js. that's it. proxy + linux (EC2) support

## S3 Bucket

    - world readable
    - 90 days expiration for files
    - cloudfront enabled
    - custom IAM user with custom policy

## UX mockups

    - http://www.artrage.com/artrage-demos.html
    - http://pencil.evolus.vn/Features.html
    - http://uxpin.com/
    - https://moqups.com/#!/

## run celery workers and flower with supervisor

    # start supervisord, starts celery & flower automatically
    supervisor

    # check logs
    supervisorctl tail celeryd

    # stop celery & flower
    supervisorctl stop celeryd
    supervisorctl stop flower

    # stop supervisord
    kill -HUP `cat /tmp/supervisord.pid`

## Heroku

following https://devcenter.heroku.com/articles/python

curl -O http://assets.heroku.com/heroku-toolbelt/heroku-toolbelt.pkg
sudo installer -pkg heroku-toolbelt.pkg -target '/'
heroku login

### posgresql

sudo mkdir -p /opt/local/var/db/postgresql92/defaultdb
sudo chown postgres:postgres /opt/local/var/db/postgresql92/defaultdb
sudo su postgres -c '/opt/local/lib/postgresql92/bin/initdb -D /opt/local/var/db/postgresql92/defaultdb'
/opt/local/lib/postgresql92/bin/postgres -D /opt/local/var/db/postgresql92/defaultdb
/opt/local/lib/postgresql92/bin/pg_ctl -D /opt/local/var/db/postgresql92/defaultdb -l logfile start

### install virtualbox

curl -O http://dlc.sun.com.edgesuite.net/virtualbox/4.2.6/VirtualBox-4.2.6-82870-OSX.dmg
sudo installer -target '/' -pkg /Volumes/VirtualBox/VirtualBox.pkg
diskutil eject /Volumes/VirtualBox
rm VirtualBox-4.2.6-82870-OSX.dmg

### postgresql
sudo mkdir -p /opt/local/var/db/postgresql92/defaultdb
sudo chown postgres:postgres /opt/local/var/db/postgresql92/defaultdb
sudo su postgres -c '/opt/local/lib/postgresql92/bin/initdb -D /opt/local/var/db/postgresql92/defaultdb'
/opt/local/lib/postgresql92/bin/postgres -D /opt/local/var/db/postgresql92/defaultdb
/opt/local/lib/postgresql92/bin/pg_ctl -D /opt/local/var/db/postgresql92/defaultdb -l logfile start

### install rvm & ruby

curl -L https://get.rvm.io | bash -s stable --ruby
rvm --default use 1.9.3

### install vagrant

gem install vagrant
sudo ln -s /usr/bin/llvm-gcc-4.2 /usr/bin/gcc-4.2
vagrant box add lucid64 http://files.vagrantup.com/lucid32.box

### install chef tool

gem install foodcritic
gem install berkshelf
