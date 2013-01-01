case node["platform_family"]
  when "redhat"
    include_recipe "webscreenshots::redhat"
  when "debian"
    include_recipe "webscreenshots::debian"
end

include_recipe "redis"
include_recipe "python"
include_recipe "postgresql::server"

#bash "django_db" do
#  user "postgres"
#  code <<-EOS
#  psql <<-ESQL
#    CREATE USER django WITH PASSWORD 'postgres';
#    CREATE DATABASE webscreenshots;
#    GRANT ALL PRIVILEGES ON DATABASE webscreenshots to django;
#  ESQL
#  EOS
#end

if node["webscreenshots"]["vagrant"]
  log("------------------ vagrant ------------------")
end

packages = ["psycopg2", "distribute", "django", "PIL", "boto", "celery-with-redis", "flower", "ipython", "python-dateutil==1.5", "supervisor"]

packages.each do |pkg|
  python_pip "#{pkg}" do
    action :install
  end
end

directory "#{node["webscreenshots"]["supervisord"]["logpath"]}" do
  mode "0755"
  recursive true
end

template "/etc/init.d/supervisor" do
  source "supervisor.init.erb"
  mode 0755
end

template "/etc/supervisord.conf" do
  source "supervisord.conf.erb"
  mode 0644
  notifies :reload, 'service[supervisor]'
end

service "supervisor" do
  reload_command "supervisorctl update"
  supports :reload => true, :status => true
  action [:enable, :start]
end

template "/etc/boto.cfg" do
  source "boto.cfg.erb"
  mode 0644
end

# from http://skookum.com/blog/dynamic-screenshots-on-the-server-with-phantomjs/
remote_file "#{Chef::Config["file_cache_path"]}/phantomjs-#{node["webscreenshots"]["phantomjs"]["version"]}.tar.bz2" do
  source node["webscreenshots"]["phantomjs"]["uri"]
  action :create_if_missing
  mode "0644"
end

bash "install phantomjs" do
  cwd Chef::Config["file_cache_path"]
  user "root"
  code <<-EOS
    tar -jxvf phantomjs-#{node["webscreenshots"]["phantomjs"]["version"]}.tar.bz2
    mv phantomjs-#{node["webscreenshots"]["phantomjs"]["version"]}-linux-x86_64 /opt
  EOS
  not_if "test -e /opt/phantomjs-#{node["webscreenshots"]["phantomjs"]["version"]}-linux-x86_64"
end
