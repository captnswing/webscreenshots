var casper = require('casper').create({
    verbose: false,
    logLevel: "info",
    waitTimeout: 40000,
    timeout: 40000,
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:33.0) Gecko/20100101 Firefox/33.0'
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

casper.then(function () {
    this.echo('rendering from file ' + htmlfile);
    this.page.content = fs.read(htmlfile);
});

casper.then(function () {
    this.viewport(1280, 800);
    this.evaluate(function () {
        document.body.style.backgroundColor = '#fff';
    });
});

casper.then(function () {
    this.echo('capturing to file ' + jpgfile);
    this.capture(jpgfile, undefined, {
        format: 'jpg',
        quality: 98
    });
});

casper.run();
