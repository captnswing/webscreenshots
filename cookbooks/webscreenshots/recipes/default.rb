#--------
# install dependencies
#--------
# don't start the redis service
node.set["redis"]["source"]["create_service"] = false
# just install redis from source
include_recipe "redis::source"
include_recipe "python"
include_recipe "postgresql::server"

#--------
# create group, user and config dir
#--------
my_user = node["webscreenshots"]["user"]
my_group = node["webscreenshots"]["group"]
my_venv = node["webscreenshots"]["home"]

group my_group

user my_user do
  gid my_group
  home my_venv
  system true
end

directory "#{my_venv}/etc/" do
  owner my_user
  group my_group
  mode "0750"
end

directory "#{my_venv}/var/log" do
  owner my_user
  group my_group
  mode "0750"
  recursive true
end

directory "#{my_venv}/var/run" do
  owner my_user
  group my_group
  mode "0750"
  recursive true
end

#--------
# create venv
#--------
python_virtualenv my_venv do
  owner my_user
  group my_group
  action :create
end

#--------
# install python packages into venv
#--------
case node["platform_family"]
  when "debian"
    # for PIL / pillow
    package "libjpeg8-dev"
    package "libfreetype6-dev"
  when "rhel"
    # for PIL / pillow
    package "libjpeg-devel"
    package "libpng-devel"
    package "freetype-devel"
end

python_packages = [
    "boto",
    "celery-with-redis",
    "distribute",
    "django",
    "flower",
    "gunicorn",
    "ipython",
    # PIL --> pillow, see http://stackoverflow.com/a/12359864/41404
    "pillow",
    "psycopg2",
    "python-dateutil==1.5",
    "supervisor"
]

python_packages.each do |pypkg|
  python_pip "#{pypkg}" do
    virtualenv my_venv
    user my_user
    group my_group
    action :install
  end
end

#--------
# install webscreenshots app
#--------
if node["webscreenshots"]["vagrant"]
  log("------------------ using vagrant ------------------")

  node.set["webscreenshots"]["working_dir"] = "/vagrant/src/webscreenshots"

  execute "install webscreenshots" do
    cwd "/vagrant"
    command "#{node["webscreenshots"]["home"]}/bin/python setup.py develop"
  end

  execute "webscreenshots syncdb" do
    user my_user
    group my_group
    cwd "#{node["webscreenshots"]["working_dir"]}"
    command "#{node["webscreenshots"]["home"]}/bin/python manage.py syncdb --noinput"
  end
else
  log("------------------ not using vagrant ------------------")
end

include_recipe "webscreenshots::phantomjs"
include_recipe "webscreenshots::supervisord"

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

#http://cuppster.com/2011/05/18/using-supervisor-with-upstart/
#http://zerokspot.com/weblog/2012/06/17/sitemanagement-with-supervisord/
#http://pypi.python.org/pypi/django-supervisor/
