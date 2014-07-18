var casper = require('casper').create({
    verbose: true,
    logLevel: "info"
});

var url = casper.cli.args[0];
var filename = casper.cli.args[1];

casper.userAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36');

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
    this.viewport(1280, 800);
    this.evaluate(function () {
        document.body.style.backgroundColor = '#fff';
    });
    this.capture(filename);
});

casper.run();
