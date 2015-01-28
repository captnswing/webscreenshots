var casper = require('casper').create({
    verbose: false,
    logLevel: "debug",
    pageSettings: {
        loadImages: true,
        loadPlugins: true,
        userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:33.0) Gecko/20100101 Firefox/33.0'
    },
    waitTimeout: 20000,
    timeout: 20000
});

if (casper.cli.args.length != 1) {
    casper
        .echo("Usage:\n$ casperjs capture_local.js <htmlfile>")
        .exit(1);
}

var fs = require('fs');
var htmlfile = casper.cli.args[0];
var jpgfile = htmlfile.replace('.html', '.jpg');

casper.userAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:33.0) Gecko/20100101 Firefox/33.0');

casper.on('http.status.301', function (resource) {
    this.log('Hey, this one is 301: ' + resource.url, 'warning');
});
casper.on('http.status.404', function (resource) {
    this.log('Hey, this one is 404: ' + resource.url, 'error');
    casper.exit(1);
});
casper.on('http.status.500', function (resource) {
    this.log('Hey, this one is 500: ' + resource.url, 'error');
    casper.exit(1);
});

casper.start();

// http://codeutopia.net/blog/2014/02/05/tips-for-taking-screenshots-with-phantomjs-casperjs/

var displayimages = function (il) {
    console.log(il.length);
    console.log("______");
    for (var index = 0; index < il.length; index++) {
        console.log(il[i]);
    }
};

// listening to a custom event
casper.on('page.onResourceRequested', function (e) {
    this.echo('page onResourceRequested ' + e);
});

casper.onResourceRequested = function (request) {
    console.log('Request ' + request);
};


casper.then(function () {
    this.echo('rendering from file ' + htmlfile);
    this.page.content = fs.read(htmlfile);
    this.viewport(1280, 800);
    this.evaluate(function () {
        document.body.style.backgroundColor = '#fff';
    });
    //this.debugHTML();
    //casper.waitFor(function () {
    //    return this.evaluate(function () {
    //        var images = document.getElementsByTagName('img');
    //        return Array.prototype.every.call(images, function (i) {
    //            return i.complete;
    //        });
    //    });
    //}, displayimages(document.getElementsByTagName('img')));
});


//casper.waitFor(
//    function () {
//        return this.evaluate(function () {
//            return window.imagesNotLoaded == 0;
//        });
//    },
//    function then() {
//        this.echo('capturing to file ' + jpgfile);
//        this.capture(jpgfile, undefined, {
//            format: 'jpg',
//            quality: 98
//        });
//    },
//    console.log("timeout")
//);

casper.then(function () {
    this.echo('capturing to file ' + jpgfile);
    this.capture(jpgfile, undefined, {
        format: 'jpg',
        quality: 98
    });
});

casper.run();
