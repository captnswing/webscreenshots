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

[webkit2png](http://www.paulhammond.org/webkit2png) verkar klart vettigast.

## Utforskning 12 Dec 2012

- There's phantom.js
- There's thumbalizr
- http://www.moreofit.com/similar-to/www.thumbalizr.com/Top_10_Sites_Like_Thumbalizr/

## SVT Proxy

Det visar sig svårt att göra proxy anpassning till webkit2png

- [github.com/paulhammond/webkit2png/blob/master/webkit2png#L136](https://github.com/paulhammond/webkit2png/blob/master/webkit2png#L136)
- [stackoverflow.com/questions/5885169/how-to-deal-with-proxy-setting-in-uiwebview](http://stackoverflow.com/questions/5885169/how-to-deal-with-proxy-setting-in-uiwebview)

Fyra alternativ

1. Betala @ph för proxy feature [twitter.com/captnswing/status/273482881123352576](https://twitter.com/captnswing/status/273482881123352576)
2. hyr os x miljö i moln [stackoverflow.com/questions/7308039/do-on-demand-mac-os-x-cloud-services-exist-comparable-to-amazons-ec2-on-demand](http://stackoverflow.com/questions/7308039/do-on-demand-mac-os-x-cloud-services-exist-comparable-to-amazons-ec2-on-demand)
3. övertyga T&U att låta en mac server kommer åt internet utan proxy
4. testa python-webkit2png

## Implementation ideas

- install celery
- celerybeat to save screenshots of all configured pages every 5min
- submits celery task to transfer resulting png files to s3 via boto

## S3 Bucket

    - world readable
    - 90 days expiration for files
    - cloudfront enabled
    - http://shrub.appspot.com/svti-webscreenshots/2012/12/02/
    - http://docs.amazonwebservices.com/AmazonS3/latest/API/RESTBucketGET.html

## UX mockups

    - http://www.artrage.com/artrage-demos.html
    - http://pencil.evolus.vn/Features.html
    - http://uxpin.com/
    - https://moqups.com/#!/

## Install celery

    pip install celery-with-redis flower
    pip install django docutils
    pip install supervisor
    pip install boto pil

## Install redis

[reistiago.wordpress.com/2011/07/23/installing-on-redis-mac-os-x](http://reistiago.wordpress.com/2011/07/23/installing-on-redis-mac-os-x/)

    curl -O http://redis.googlecode.com/files/redis-2.6.5.tar.gz
    tar xfz redis-2.6.5.tar.gz
    cd redis-2.6.5
    sudo make install
    sudo vi /Library/LaunchDaemons/org.redis.redis-server.plist
_____

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
     "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>Label</key>
        <string>org.redis.redis-server</string>
        <key>Program</key>
        <string>/usr/local/bin/redis-server</string>
        <key>ProgramArguments</key>
        <array>
                <string>redis-server</string>
        </array>
        <key>RunAtLoad</key>
        <true/>
        <key>KeepAlive</key>
        <true/>
        <key>StandardErrorPath</key>
        <string>/var/log/redis/output.log</string>
        <key>StandardOutPath</key>
        <string>/var/log/redis/output.log</string>
    </dict>
    </plist>

_____

    sudo mkdir /var/log/redis
    sudo launchctl load /Library/LaunchDaemons/org.redis.redis-server.plist
    sudo launchctl start org.redis.redis-server
    psa redis

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

