["language-pack-sv", "xfs", "xfstt", "fontconfig"].each do |dev_pkg|
  package dev_pkg
end

# for PIL
["libjpeg-dev"].each do |dev_pkg|
  package dev_pkg
end

# from http://askubuntu.com/questions/16225/how-can-i-accept-microsoft-eula-agreement-for-ttf-mscorefonts-installer
bash "run ttf-mscorefonts-installer" do
  user "root"
  code <<-EOS
  echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | debconf-set-selections
  apt-get install -y ttf-mscorefonts-installer
  EOS
end

cookbook_file "/etc/fonts/local.conf" do
  source "localfonts.conf"
  mode 0644
end

bash "clear fontchache" do
  code "fc-cache -fv"
end
