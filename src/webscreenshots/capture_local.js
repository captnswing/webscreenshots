var casper = require('casper').create({
    verbose: true,
    logLevel: "info",
    waitTimeout: 40000,
    timeout: 40000,
    pageSettings: {
        loadPlugins: true,
        loadImages: true,
        javascriptEnabled: true
    },
    viewportSize: {width: 1280, height: 800}
});

//https://gist.github.com/nhoizey/4060568
var fs = require('fs');
if (casper.cli.args.length < 1) {
    casper
        .echo("Usage:\n$ casperjs capture_local.js <htmlfiles>")
        .exit(1)
    ;
} else {
    var htmlfiles = casper.cli.args.filter(function (f) {
        return /.*\.html/.test(f);
    });
}

// TODO: insert <base> tag into <head>
// http://stackoverflow.com/a/589845/41404

casper.userAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:20.0) Gecko/20100101 Firefox/20.0');

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

casper.each(htmlfiles, function (casper, htmlfile) {
    casper.start('file:////Users/hoffsummer/Development/webscreenshots/src/webscreenshots/' + htmlfile, function () {
        this.echo('capturing file ' + htmlfile);
        this.viewport(1280, 800);
        this.evaluate(function () {
            document.body.style.backgroundColor = '#fff';
        });
        this.capture(htmlfile+'.png');
    });
});

casper.run();
