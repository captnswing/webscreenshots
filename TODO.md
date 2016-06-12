### evaluation of screenshot tools

**************
**************
http://stackoverflow.com/a/15699761
https://dzone.com/articles/python-testing-phantomjs
http://toddhayton.com/2015/02/03/scraping-with-python-selenium-and-phantomjs/
**************
**************
https://www.caktusgroup.com/blog/2014/06/23/scheduling-tasks-celery/
https://github.com/aosabook/500lines/tree/master/crawler
https://news.ycombinator.com/item?id=11887230


##### requirements:

* headless
* runs on virtualized linux (Vagrant, VMWare ESX, EC2, GCE)
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

### S3 Bucket setup

* world readable
* writeable only by custom IAM user with custom policy
* 1825 days expiration for files, files will be deleted afterwards
* cloudfront enabled
* nginx as proxy
* http://charlesleifer.com/blog/nginx-a-caching-thumbnailing-reverse-proxying-image-server-/
* https://news.ycombinator.com/item?id=11128569
* http://docs.aws.amazon.com/lambda/latest/dg/with-s3-example.html
* https://github.com/mentum/lambdaws#using-large-external-libraries

### idea: nicer select boxes

use django forms?

* http://ivaynberg.github.io/select2/select2-latest.html
* http://github.com/applegrew/django-select2
* http://www.samsung.com/se/support/main/supportMain.do?supportIaCode=10003#
* http://codereview.stackexchange.com/questions/824/looking-for-improvements-on-my-jquery-ui-tagging-widget

### idea: mashup / integration with other projects

* [pageonex.com](http://pageonex.com/)
* [newsdiffs](https://github.com/ecprice/newsdiffs)

### celery

* http://www.syncano.com/configuring-running-django-celery-docker-containers-pt-1/
* https://denibertovic.com/posts/celery-best-practices/
* http://wiredcraft.com/posts/2015/02/04/3-gotchas-for-celery.html
* https://registry.hub.docker.com/search?q=rabbitmq

### better apis

* https://github.com/breenmachine/httpscreenshot
* http://gilliam.github.io/
* http://www.django-rest-framework.org/tutorial/1-serialization/
* http://tastypieapi.org/

### queue thoughts

* http://huey.readthedocs.org/en/latest/getting-started.html
* CELERYD_POOL = 'gevent': http://celery.readthedocs.org/en/latest/userguide/workers.html
* http://aws.amazon.com/lambda/
* http://aws.amazon.com/documentation/swf/
* http://aws.amazon.com/documentation/sqs/
* http://python-rq.org
* https://github.com/pricingassistant/rq-dashboard
* http://tavendo.com/blog/post/is-crossbar-the-future-of-python-web-apps/
* http://www.reddit.com/r/Python/comments/27d0km/is_crossbario_the_future_of_python_web_apps/
* http://blog.crocodoc.com/post/48703468992/process-managers-the-good-the-bad-and-the-ugly
* https://news.ycombinator.com/item?id=5596750
* http://kentonv.github.io/capnproto/

### async requests

* http://docs.python-requests.org/en/latest/user/advanced/#blocking-or-non-blocking
* https://github.com/kennethreitz/grequests

###

* http://www.informit.com/articles/article.aspx?p=2320938
* http://www.toptal.com/python/beginners-guide-to-concurrency-and-parallelism-in-python
* https://diff.io/
* https://github.com/google/fonts/
* 
