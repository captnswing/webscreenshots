# make sure python is installed
include_recipe "python"
include_recipe "postgresql::server"

# from http://skookum.com/blog/dynamic-screenshots-on-the-server-with-phantomjs/
remote_file "#{Chef::Config["file_cache_path"]}/phantomjs-#{node["phantomjs"]["version"]}.tar.bz2" do
  source node["phantomjs"]["uri"]
  action :create_if_missing
  mode "0644"
end

["language-pack-sv", "xfs", "xfstt", "fontconfig"].each do |dev_pkg|
  package dev_pkg
end

# from http://askubuntu.com/questions/16225/how-can-i-accept-microsoft-eula-agreement-for-ttf-mscorefonts-installer
bash "run ttf-mscorefonts-installer" do
  user "root"
  code <<-EOS
  echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | debconf-set-selections
  apt-get install -y ttf-mscorefonts-installer
  EOS
#  not_if "test -e /opt/phantomjs-#{node["phantomjs"]["version"]}-linux-x86_64"
end

## install mac fonts
## http://grasshopperpebbles.com/ubuntu/ubuntu-convert-mac-dfont-files-into-ttf-using-fondu/
#node["phantomjs"]["macfonts"].each do |ttf_file|
#  cookbook_file "/usr/share/fonts/truetype/#{ttf_file}" do
#    source ttf_file
#    owner "root"
#    group "root"
#    mode "0644"
#    end
#end
#
#bash "clear fontchache" do
#  code "fc-cache -fv"
#end

bash "install phantomjs" do
  cwd Chef::Config["file_cache_path"]
  user "root"
  code <<-EOS
    bzip2 -d phantomjs-#{node["phantomjs"]["version"]}.tar.bz2
    tar xf phantomjs-#{node["phantomjs"]["version"]}.tar
    mv phantomjs-#{node["phantomjs"]["version"]}-linux-x86_64 /opt
  EOS
  not_if "test -e /opt/phantomjs-#{node["phantomjs"]["version"]}-linux-x86_64"
end
