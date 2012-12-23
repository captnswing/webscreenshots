maintainer       "Frank Hoffsümmer"
maintainer_email "frank.hoffsummer@gmail.com"
license          "All rights reserved"
description      "Installs/Configures webscreenshots system"
long_description IO.read(File.join(File.dirname(__FILE__), 'README.md'))
version          "0.0.2"

depends "python"
depends "redis"

#supports "scientific", ">= 6.0"
supports "ubuntu", ">= 10.4"
