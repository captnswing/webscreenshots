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
