default["webscreenshots"]["phantomjs"]["version"] = "1.7.0"
default["webscreenshots"]["phantomjs"]["arch"] = "x86_64"
#default["webscreenshots"]["phantomjs"]["arch"] = "i686"
default["webscreenshots"]["phantomjs"]["uri"] = "http://phantomjs.googlecode.com/files/phantomjs-#{node["webscreenshots"]["phantomjs"]["version"]}-linux-#{node["webscreenshots"]["phantomjs"]["arch"]}.tar.bz2"
default["webscreenshots"]["macfonts"] = ["Geneva.ttf",
                                         "Helvetica.ttf",
                                         "HelveticaBold.ttf",
                                         "HelveticaNeue.ttf",
                                         "HelveticaNeueBold.ttf"]

default["webscreenshots"]["supervisord"]["logpath"] = "/var/log/supervisord"

default["webscreenshots"]["s3bucketname"] = "svti-webscreenshots"
# IAM user with access to configured S3 bucket
# http://docs.amazonwebservices.com/IAM/latest/UserGuide/GSGHowToCreateAdminsGroup.html
default["webscreenshots"]["iam"]["username"] = "webscreenshost"
default["webscreenshots"]["iam"]["accesskeyid"] = "AKIAJGUNM2DBSJAZ777Q"
default["webscreenshots"]["iam"]["secretkey"] = "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"
