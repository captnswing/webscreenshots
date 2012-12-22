remote_file "#{Chef::Config["file_cache_path"]}/phantomjs-#{node["phantomjs"]["version"]}.tar.bz2" do
  source node["phantomjs"]["uri"]
  action :create_if_missing
  mode "0644"
end

["freetype", "fontconfig", "rpm-build", "wget", "ttmkfdir"].each do |dev_pkg|
  package dev_pkg
end

# from http://corefonts.sourceforge.net/
bash "install msttcorefonts" do
  cwd Chef::Config["file_cache_path"]
  user "root"
  code <<-EOS
  rpm -ivH http://ftp.scientificlinux.org/linux//extra/dag/packages/cabextract/cabextract-1.2-1.el5.rf.x86_64.rpm || :
  wget http://corefonts.sourceforge.net/msttcorefonts-2.5-1.spec
  rpmbuild -bb msttcorefonts-2.5-1.spec
  EOS
end

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
