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

* [phantom.js](http://phantomjs.org/)
* [casper.js](http://casperjs.org/)
* [ghost.py](http://jeanphix.me/Ghost.py/)
* [python-webkit2png](https://github.com/AdamN/python-webkit2png)
* [webkit2png](http://www.paulhammond.org/webkit2png)
* [khtml2png](http://khtml2png.sourceforge.net)
* [cutycapt](http://cutycapt.sourceforge.net)
* [pywebshot](https://github.com/coderholic/PyWebShot)
* [wkhtmltopdf](http://code.google.com/p/wkhtmltopdf/)
* [htmlshots](https://github.com/w3p/htmlshots)

##### webservices:

* [node-urlshot](http://node-urlshot.herokuapp.com), example with [svt.se](http://node-urlshot.herokuapp.com/?url=http://svt.se/&viewport=1280x900&format=jpg)
* [thumbalizr](http://www.thumbalizr.com/)
* [thumbalizr alternatives](http://www.moreofit.com/similar-to/www.thumbalizr.com/Top_10_Sites_Like_Thumbalizr/)
* loads of others

### S3 Bucket

    - world readable
    - 1825 days expiration for files
    - cloudfront enabled
    - custom IAM user with custom policy

### nicer select boxes

* http://ivaynberg.github.io/select2/select2-latest.html
* http://www.samsung.com/se/support/main/supportMain.do?supportIaCode=10003#
* http://codereview.stackexchange.com/questions/824/looking-for-improvements-on-my-jquery-ui-tagging-widget

