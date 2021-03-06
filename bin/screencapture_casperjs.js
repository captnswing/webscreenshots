var casper = require('casper').create({
    verbose: true,
    logLevel: "info"
});

var url = casper.cli.args[0];
var filename = casper.cli.args[1];

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

casper.start(url, function () {
    this.viewport(1440, 900);
    this.evaluate(function () {
        document.body.style.backgroundColor = '#fff';
    });
    this.capture(filename, undefined, {
        format: 'jpg',
        quality: 95
    });
});

casper.run();
