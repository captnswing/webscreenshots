default["webscreenshots"]["supervisord"]["logdir"] = "#{node["webscreenshots"]["home"]}/var/log"
default["webscreenshots"]["supervisord"]["pidfile"] = "#{node["webscreenshots"]["home"]}/var/run/supervisord.pid"
default["webscreenshots"]["supervisord"]["cfgfile"] = "#{node["webscreenshots"]["home"]}/etc/supervisord.conf"
