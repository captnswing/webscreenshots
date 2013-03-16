function getbaseurl(chosendate, chosenWidth) {
    var wsimages_url = wsimages_path;
    if (!(typeof chosenWidth === 'undefined')) {
        wsimages_url += '/' + chosenWidth + 'x' + chosenWidth;
    }
    var curr_year = chosendate.getFullYear();
    var curr_month = chosendate.getMonth() + 1; //Months are zero based
    var curr_date = chosendate.getDate();
    return [wsimages_url, curr_year, addZero(curr_month), addZero(curr_date), ''].join('/');
}

function geturl(chosenDate, chosenSite, chosenExt, chosenWidth) {
    if ((typeof chosenDate === 'undefined') || (typeof chosenSite === 'undefined')) {
        return [];
    }
    var myurl;
    myurl = getbaseurl(chosenDate, chosenWidth);
    myurl += chosenSite.replace('/', '|') + '/' + addZero(chosenDate.getHours()) + '.' + addZero(chosenDate.getMinutes());
    if (typeof chosenExt !== 'undefined') {
        myurl += '-' + chosenExt;
    }
    myurl += '.jpg';
    return myurl;
}

function getimgtd(chosenTime, chosenSite, chosenWidth) {
    //  <td class="aftonbladet.se">
    //      <a href="http://d2np6cnk6s6ggj.cloudfront.net/2013/01/06/aftonbladet.se/17.00-top.jpg">
    //          <img width="250px" src="http://d2np6cnk6s6ggj.cloudfront.net/2013/01/06/aftonbladet.se/17.00-thumb.jpg" />
    //      </a>
    // </td>
    var thumb_url = geturl(chosenTime, chosenSite, "thumb", chosenWidth);
    var full_url = geturl(chosenTime, chosenSite, "top");
    //var full_url = geturl(chosenTime, chosenSite, "thumb");
    var imgtitle = chosenSite + ' ' + chosenTime;
    var tdstring = "<td class='" + chosenSite + "'>";
    tdstring += "<a class='wsimage' title='" + imgtitle + "' href='" + full_url + "'>";
    tdstring += "<img width='" + chosenWidth + "' src='" + thumb_url + "' />";
    tdstring += "</a></td>";
    return tdstring;
}

function getminuterange(chosenHour) {
    var minutes = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55];
    var isoffhours = $.inArray(chosenHour.getHours(), offhours) > -1
    if (isoffhours) {
        minutes = [0];
    }
    if (isCurrentHour(chosenHour)) {
        // chosenHour is current hour
        var thismin = parseInt(new Date().getMinutes()) - 1; // give us a 1min break
        var factor = parseInt(thismin / 5) + 1;
        minutes = range(5, factor * 5, 5);
    }
    minutes = minutes.reverse();
    var visibleminutes = [];
    $.each(minutes, function (i, minute) {
        chosenHour.setMinutes(minute);
        visibleminutes.push(new Date(chosenHour.getTime()));
    });
    return visibleminutes;
}

function getmorehours(timestamp, numberofhours) {
    // create startDate object from timestamp
    var startDate = new Date(parseInt(timestamp));
    startDate.setHours(startDate.getHours(), 0, 0, 0);
    // create targetDate from startDate
    var targetDate = new Date(startDate.getTime());
    targetDate.adjust('hours', numberofhours);
    var visiblehours = [];
    startDate.each(targetDate, 'hours', 1, function (currentDate, currentStep, thisDate) {
        var newdate = new Date(currentDate.getTime());
        // set minutes, seconds and milliseconds to 0
        newdate.setMinutes(0, 0, 0);
        // add new date object to array
        visiblehours.push(newdate);
    });
    // skip first element in array and return
    return visiblehours.slice(1, visiblehours.length);
}

function gethourrange(chosenDate) {
    // returns default hour range for which rows are displayd
    var primetime = 20;
    var showlasthours = 9;
    var visiblehours = [];
    var startDate = new Date(chosenDate.getTime());
    if (isCurrentDay(chosenDate)) {
        // chosenDate is today
        // set hour range to last 9 hours
        startDate.adjust('hours', -1 * showlasthours);
        var currentHour = new Date(chosenDate.getTime());
        currentHour.adjust('minutes', -1); // give us a 1min break
        chosenDate.setHours(currentHour.getHours(), 0, 0, 0);
    } else {
        // chosenDate is not today
        // set hour range from (primetime-showlasthours) to primetime
        startDate.setHours(primetime - showlasthours, 0, 0, 0);
        chosenDate.setHours(primetime, 0, 0, 0);
    }
    // iterate over date interval, in 1 hour steps
    chosenDate.each(startDate, 'hours', 1, function (currentDate, currentStep, thisDate) {
        var newdate = new Date(currentDate.getTime());
        // set minutes, seconds and milliseconds to 0
        newdate.setMinutes(0, 0, 0);
        // add new date object to array
        visiblehours.push(newdate);
    });
    return visiblehours;
}

function getrows(chosenMoments, chosenSites, chosenWidth) {
    var allrows = [];
    $.each(chosenMoments, function (i, currentHour) {
        var curr_hour = addZero(currentHour.getHours()) + "." + addZero(currentHour.getMinutes());
        // set tr id to epoch milliseconds
        var rowid = currentHour.getTime();
        var myrow = "<tr id='" + rowid + "'>";
        myrow += "<td>";
        var cmpdate = new Date(currentHour.getTime());
        var hourstring = "kl&nbsp;" + curr_hour;
        var buttonclasses = "btn btn-small disabled";
        var isnotoffhour = ($.inArray(currentHour.getHours(), offhours) == -1);
        var isfullhour = (currentHour.getMinutes() == 0);
        if (isfullhour && isnotoffhour) {
            buttonclasses = "hour btn btn-small btn-success";
        }
        myrow += "<button class='" + buttonclasses + "' type='button'>" + hourstring + "</button>";
        myrow += "</td>";
        $.each(chosenSites, function (i, site) {
            myrow += getimgtd(currentHour, site, chosenWidth);
        });
        allrows.push(myrow);
    });
    return allrows;
}
