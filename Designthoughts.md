### evaluation of screenshot tools

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

* [casper.js](http://casperjs.org/)
* [phantom.js](http://phantomjs.org/)
* [ghost.py](http://jeanphix.me/Ghost.py/)
* [phantompy](https://github.com/niwibe/phantompy)
* [python-webkit2png](https://github.com/AdamN/python-webkit2png)
* [webkit2png](http://www.paulhammond.org/webkit2png)
* [khtml2png](http://khtml2png.sourceforge.net)
* [cutycapt](http://cutycapt.sourceforge.net)
* [pywebshot](https://github.com/coderholic/PyWebShot)
* [wkhtmltopdf](http://code.google.com/p/wkhtmltopdf/)
* [htmlshots](https://github.com/w3p/htmlshots)

##### webservices:

not really relevant for this project

* [node-urlshot](http://node-urlshot.herokuapp.com), example with [svt.se](http://node-urlshot.herokuapp.com/?url=http://svt.se/&viewport=1280x900&format=jpg)
* [thumbalizr](http://www.thumbalizr.com/)
* [thumbalizr alternatives](http://www.moreofit.com/similar-to/www.thumbalizr.com/Top_10_Sites_Like_Thumbalizr/)
* loads of others

### S3 Bucket setup

* world readable
* writeable only by custom IAM user with custom policy
* 1825 days expiration for files, files will be deleted afterwards
* cloudfront enabled
* nginx as proxy

### idea: nicer select boxes

use django forms?

* http://ivaynberg.github.io/select2/select2-latest.html
* https://github.com/applegrew/django-select2
* http://www.samsung.com/se/support/main/supportMain.do?supportIaCode=10003#
* http://codereview.stackexchange.com/questions/824/looking-for-improvements-on-my-jquery-ui-tagging-widget

### idea: mashup / integration with other projects

* [pageonex.com](http://pageonex.com/)
* [newsdiffs](https://github.com/ecprice/newsdiffs)

### queue thoughts

* http://python-rq.org
* https://github.com/pricingassistant/rq-dashboard
* http://tavendo.com/blog/post/is-crossbar-the-future-of-python-web-apps/
* http://www.reddit.com/r/Python/comments/27d0km/is_crossbario_the_future_of_python_web_apps/
* http://blog.crocodoc.com/post/48703468992/process-managers-the-good-the-bad-and-the-ugly
* https://news.ycombinator.com/item?id=5596750
* http://kentonv.github.io/capnproto/

