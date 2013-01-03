default["webscreenshots"]["s3bucketname"] = "svti-webscreenshots"

# IAM user with access to configured S3 bucket
# http://docs.amazonwebservices.com/IAM/latest/UserGuide/GSGHowToCreateAdminsGroup.html
default["webscreenshots"]["iam"]["username"] = "webscreenshots"
# TODO: encrypted databags
default["webscreenshots"]["iam"]["accesskeyid"] = "AKIAJGUNM2DBSJAZ777Q"
default["webscreenshots"]["iam"]["secretkey"] = "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"

default["webscreenshots"]["user"] = "webscreenshots"
default["webscreenshots"]["group"] = "webscreenshots"
default["webscreenshots"]["home"] = "/opt/webscreenshots"

# running as vagrant?
default["webscreenshots"]["vagrant"] = node["kernel"]["modules"].attribute?("vboxguest")

set["postgresql"]["password"]["postgres"] = "postgres"
