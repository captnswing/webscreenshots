default["phantomjs"]["version"] = "1.7.0"
default["phantomjs"]["arch"] = "x86_64"
#default["phantomjs"]["arch"] = "i686"
default["phantomjs"]["uri"] = "http://phantomjs.googlecode.com/files/phantomjs-#{node["phantomjs"]["version"]}-linux-#{node["phantomjs"]["arch"]}.tar.bz2"
default["phantomjs"]["macfonts"] =  ["Geneva.ttf",
                                    "Helvetica.ttf",
                                    "HelveticaBold.ttf",
                                    "HelveticaNeue.ttf",
                                    "HelveticaNeueBold.ttf"]
