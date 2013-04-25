Vagrant.configure("2") do |config|
  config.berkshelf.enabled = true
  config.berkshelf.berksfile_path = './Berksfile'
  config.vm.box = "opscode-ubuntu-1204"
  config.vm.box_url = "https://opscode-vm.s3.amazonaws.com/vagrant/opscode_ubuntu-12.04_chef-11.2.0.box"

  config.vm.hostname = "webscreenshots.vagrant"

  config.vm.provider :virtualbox do |vb|
    vb.name = "webscreenshots.vagrant"
    vb.customize ["modifyvm", :id, "--memory", 1024]
    vb.customize ["modifyvm", :id, "--cpus", 2]
    #vb.customize ["modifyvm", :id, "--cpuexecutioncap", "50"]
  end

  # make postgres server accessible from host environment
  config.vm.network :forwarded_port, guest: 5432, host: 5432
  # flower gui
  config.vm.network :forwarded_port, guest: 5555, host: 5555
  # supervisor gui
  config.vm.network :forwarded_port, guest: 9001, host: 9001
  # django gui
  config.vm.network :forwarded_port, guest: 80, host: 8000

  config.vm.provision :chef_solo do |chef|
    # strange bug
    chef.cookbooks_path = "/Users/frank/.berkshelf/vagrant/berkshelf-20130415-22760-1hntml6"
    chef.log_level = :info
    chef.add_recipe "chef-base"
    chef.add_recipe "chef-msttcorefonts"
    chef.add_recipe "webscreenshots"

    chef.json = {
        "webscreenshots" => {
            "user" => "vagrant",
            "group" => "vagrant",
            "project_root" => "/vagrant",
            "django_settings_module" => "webscreenshots.settings.vagrant",
            "cloudfront_server" => "http://d2np6cnk6s6ggj.cloudfront.net"
        },
        "postgresql" => {
            # from https://github.com/opscode-cookbooks/postgresql#chef-solo-note
            # must be the same as in django settings.py
            "password" => {
                "postgres" => "postgres"
            },
            # make postgres server accessible from any other machine
            "config" => {
                "listen_addresses" => "0.0.0.0"
            },
            "pg_hba" => [
                {:type => 'local', :db => 'all', :user => 'all', :addr => nil, :method => 'trust'},
                {:type => 'host', :db => 'all', :user => 'all', :addr => '127.0.0.1/32', :method => 'md5'},
                {:type => 'host', :db => 'all', :user => 'all', :addr => '::1/128', :method => 'md5'},
                {:type => 'host', :db => 'postgres', :user => 'all', :addr => '0.0.0.0/0', :method => 'trust'}
            ]
        },
    }
  end
end
