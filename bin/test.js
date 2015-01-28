// adapted from https://gist.github.com/cjoudrey/1341747
var page = require('webpage').create(),
    fs = require('fs'),
    system = require('system'),
    count = 0,
    htmlFile = system.args[1],
    resourceWait = 300,
    maxRenderWait = 20000,
    forcedRenderTimeout,
    renderTimeout;

console.log(fs.workingDirectory);
page.viewportSize = {width: 1280, height: 2000};

page.onResourceRequested = function (req) {
    count += 1;
    //console.log(JSON.stringify(req, null, 4));
    //console.log('> ' + req.id + ' - ' + req.url);
    clearTimeout(renderTimeout);
};

page.onResourceReceived = function (res) {
    //console.log(JSON.stringify(res, null, 4));
    if (!res.stage || res.stage === 'end') {
        count -= 1;
        //console.log(res.id + ' ' + res.status + ' - ' + res.url);
        if (count === 0) {
            renderTimeout = setTimeout(doRender, resourceWait);
        }
    }
};

function doRender() {
    page.render(htmlFile + ".jpg", {format: 'jpeg', quality: '95'});
    console.log(htmlFile + ".jpg");
    phantom.exit();
}

page.open(htmlFile, function (status) {
    if (status !== 'success') {
        console.log("phantomjs: some error occured trying to access file: '" + htmlFile + "'");
        phantom.exit(1);
    } else {
        page.evaluate(function () {
            document.body.style.backgroundColor = '#fff';
        });
        forcedRenderTimeout = setTimeout(function () {
            console.log(count);
            doRender(htmlFile);
        }, maxRenderWait);
    }
});

