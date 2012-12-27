package "fontconfig"

# for PIL
package "libjpeg-dev"

#---------------
# install mscorefonts
#---------------
# from http://askubuntu.com/questions/16225/how-can-i-accept-microsoft-eula-agreement-for-ttf-mscorefonts-installer
bash "run ttf-mscorefonts-installer" do
  user "root"
  code <<-EOS
  echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | debconf-set-selections
  apt-get install -y ttf-mscorefonts-installer
  EOS
end

#---------------
# install local.conf
#---------------
# from https://wiki.ubuntu.com/Fonts
cookbook_file "/etc/fonts/local.conf" do
  source "localfonts.conf"
  mode 0644
end

##---------------
## install Mac fonts
##---------------
## from http://grasshopperpebbles.com/ubuntu/ubuntu-convert-mac-dfont-files-into-ttf-using-fondu/
#package "fondu"
#
#cookbook_file "#{Chef::Config["file_cache_path"]}/macfonts.tar" do
#    mode "0644"
#end
#
#directory "/usr/share/fonts/truetype/macfonts" do
#  mode "0755"
#  recursive true
#end
#
#bash "install macfonts" do
#  cwd Chef::Config["file_cache_path"]
#  user "root"
#  code <<-EOS
#  tar xvf macfonts.tar
#  fondu -force *.dfont
#  mv *.ttf /usr/share/fonts/truetype/macfonts/
#  EOS
#  not_if #{File.exists?("/usr/share/fonts/truetype/macfonts/Helvetica.ttf")}
#end
#
## from https://wiki.ubuntu.com/Fonts
#cookbook_file "/etc/fonts/local.conf" do
#  source "localfonts_with_helvetica.conf"
#  mode 0644
#end

#---------------
# regenerate font chache
#---------------
bash "regenerate fontchache" do
  code "fc-cache -fv"
end
