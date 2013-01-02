#--------
# install redis
#--------
remote_file "#{Chef::Config[:file_cache_path]}/redis-#{node["webscreenshots"]["redis"]["version"]}.tar.gz" do
  source node["webscreenshots"]["redis"]["tar_url"]
  checksum node["webscreenshots"]["redis"]["checksum"]
  mode "0644"
  action :create_if_missing
end

execute "extract redis tar" do
  cwd "#{Chef::Config[:file_cache_path]}"
  command "tar zxf redis-#{node["webscreenshots"]["redis"]["version"]}.tar.gz"
  creates "#{Chef::Config[:file_cache_path]}/redis-#{node["webscreenshots"]["redis"]["version"]}/utils/redis_init_script"
end

execute "build redis" do
  cwd "#{Chef::Config[:file_cache_path]}/redis-#{node["webscreenshots"]["redis"]["version"]}"
  command "make install PREFIX=#{node["webscreenshots"]["home"]}"
  creates "#{node["webscreenshots"]["home"]}/bin/redis-server"
end

directory "#{node["webscreenshots"]["home"]}/var/lib/redis" do
  owner node["webscreenshots"]["user"]
  group node["webscreenshots"]["group"]
  mode "0750"
  recursive true
end
