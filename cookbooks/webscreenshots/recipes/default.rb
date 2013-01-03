#--------
# install dependencies
#--------
include_recipe "python"
include_recipe "postgresql::server"

my_user = node["webscreenshots"]["user"]
my_group = node["webscreenshots"]["group"]
my_venv = node["webscreenshots"]["home"]

#--------
# create group and user
#--------
group my_group

user my_user do
  gid my_group
  home my_venv
  shell "/bin/bash"
  system true
end

#--------
# create required directories
#--------
["#{my_venv}", "#{my_venv}/etc/", "#{my_venv}/var", "#{my_venv}/var/log", "#{my_venv}/var/run", "#{my_venv}/src"].each do |dir|
  directory "#{dir}" do
    owner my_user
    group my_group
    mode "0750"
  end
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
# for PIL / pillow
case node["platform_family"]
  when "debian"
    package "libjpeg8-dev"
    package "libfreetype6-dev"
  when "rhel"
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
    "python-dateutil",
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

  node.set["webscreenshots"]["working_dir"] = "/vagrant"

else
  log("------------------ not using vagrant ------------------")

  node.set["webscreenshots"]["working_dir"] = "#{node["webscreenshots"]["home"]}/src/webscreenshots"

  case node["platform_family"]
    when "debian"
      package "mercurial"
  end

  execute "clone repo" do
    user my_user
    group my_group
    cwd "#{node["webscreenshots"]["home"]}/src"
    command "hg clone https://captnswing@bitbucket.org/captnswing/webscreenshots"
    creates "#{node["webscreenshots"]["home"]}/src/webscreenshots"
  end

  execute "update repo" do
    user my_user
    group my_group
    cwd "#{node["webscreenshots"]["working_dir"]}"
    command "hg pull; hg update"
  end
end

execute "install webscreenshots" do
  user my_user
  group my_group
  cwd "#{node["webscreenshots"]["working_dir"]}"
  command "#{node["webscreenshots"]["home"]}/bin/python setup.py develop"
end

execute "webscreenshots syncdb" do
  user my_user
  group my_group
  cwd "#{node["webscreenshots"]["working_dir"]}/src/webscreenshots"
  command "#{node["webscreenshots"]["home"]}/bin/python manage.py syncdb --noinput"
end

include_recipe "webscreenshots::redis"
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
