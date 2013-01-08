var system = require('system');
var url = system.args[1] + '/';
var filename = system.args[2];
var page = require('webpage').create();
page.viewportSize = { width: 1280, height: 720 };
page.open(url, function (status) {
    if (status !== 'success') {
        console.log("phantomjs: some error occured trying to access url: '" + url + "'");
        phantom.exit(1);
    } else {
        page.evaluate(function () {
            document.body.style.backgroundColor = '#fff';
        });
        page.render(filename);
        console.log(filename);
        phantom.exit();
    }
});
