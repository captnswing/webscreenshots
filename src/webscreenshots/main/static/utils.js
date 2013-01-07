// from http://trentrichardson.com/2011/09/27/better-javascript-date-add-and-diff/
Date.prototype.adjust = function (part, amount) {
    part = part.toLowerCase();
    var map = {
        years:'FullYear',
        months:'Month',
        weeks:'Hours',
        days:'Hours',
        hours:'Hours',
        minutes:'Minutes',
        seconds:'Seconds',
        milliseconds:'Milliseconds',
        utcyears:'UTCFullYear',
        utcmonths:'UTCMonth',
        utcweeks:'UTCHours',
        utcdays:'UTCHours',
        utchours:'UTCHours',
        utcminutes:'UTCMinutes',
        utcseconds:'UTCSeconds',
        utcmilliseconds:'UTCMilliseconds'
    };
    var mapPart = map[part];
    if (part == 'weeks' || part == 'utcweeks') amount *= 168;
    if (part == 'days' || part == 'utcdays') amount *= 24;
    this['set' + mapPart](this['get' + mapPart]() + amount);
    return this;
};


// from http://trentrichardson.com/2011/09/29/looping-through-dates-with-javascript/
Date.prototype.each = function (endDate, part, step, fn, bind) {
    var fromDate = new Date(this.getTime()),
        toDate = new Date(endDate.getTime()),
        pm = fromDate <= toDate ? 1 : -1,
        i = 0;
    while ((pm === 1 && fromDate <= toDate) || (pm === -1 && fromDate >= toDate)) {
        if (fn.call(bind, fromDate, i, this) === false) break;
        i += step;
        fromDate.adjust(part, step * pm);
    }
    return this;
};


// from http://trentrichardson.com/2011/09/29/looping-through-dates-with-javascript/
Date.prototype.diff = function (date2, parts) {
    var d1 = new Date(this.getTime()),
        d2 = new Date(date2.getTime()),
        pm = d1 <= d2 ? 1 : -1,
        result = { },
        factors = { weeks:(1000 * 60 * 60 * 24 * 7), days:(1000 * 60 * 60 * 24), hours:(1000 * 60 * 60), minutes:(1000 * 60), seconds:1000, milliseconds:1 };

    if (parts === undefined)
        parts = ['years', 'months', 'weeks', 'days', 'hours', 'minutes', 'seconds', 'milliseconds'];
    else if (typeof(parts) == "string")
        parts = [parts];

    for (var i = 0, l = parts.length; i < l; i++) {
        var k = parts[i];
        result[k] = 0;

        if (factors[k] === undefined) {
            inaWhile: while (true) {
                d2.adjust(k, -1 * pm);
                if ((pm === 1 && d1 > d2) || (pm === -1 && d1 < d2)) {
                    d2.adjust(k, 1 * pm);
                    break inaWhile;
                }
                result[k]++;
            }
        }
        else {
            var tmpDiff = Math.abs(d2.getTime() - d1.getTime());
            result[k] = Math.floor(tmpDiff / factors[k]);
            d2.adjust(k, result[k] * -1 * pm);
        }
        result[k] *= pm;
    }

    if (parts.length == 1)
        return result[parts[0]];
    return result;
};

function addZero(val) {
    return (parseInt(val) < 10) ? "0" + val : val;
}

// from a comment under http://yesudeep.wordpress.com/2009/07/25/implementing-a-pythonic-range-function-in-javascript-2/
function range() {
    // Similar to the python range() function
    var L = arguments, start, stop, step, r = []
    if (L.length == 1) {
        start = 0, stop = L[0], step = 1
    }
    else {
        start = L[0], stop = L[1], step = L[2] == null ? 1 : L[2]
    }
    for (var i = start; step > 0 ? i < stop : i > stop; i += step) {
        r.push(i)
    }
    return r
}
