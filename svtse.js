var page = require('webpage').create();
page.viewportSize = { width: 1280, height: 720 };
page.open('http://www.svt.se', function (status) {
    if (status !== 'success') {
        console.log('Unable to access the network!');
    } else {
        page.evaluate(function () {
            var body = document.body;
            body.style.backgroundColor = '#fff';
            //body.querySelector('div#title-block').style.display = 'none';
            //body.querySelector('form#edition-picker-form').parentElement.parentElement.style.display = 'none';
        });
        page.render('svtse.png');
    }
    phantom.exit();
});
