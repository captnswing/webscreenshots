Vagrant::Config.run do |config|
  config.vm.box = "opscode-ubuntu-1204"
  config.vm.box_url = "https://opscode-vm.s3.amazonaws.com/vagrant/opscode_ubuntu-12.04_chef-11.2.0.box"

  config.vm.host_name = "webscreenshots.vagrant"
  config.vm.customize ["modifyvm", :id, "--memory", 1024]
  config.vm.customize ["modifyvm", :id, "--cpus", 2]

  # make postgres server accessible from host environment
  config.vm.forward_port 5432, 5432
  # flower gui
  config.vm.forward_port 5555, 5555
  # supervisor gui
  config.vm.forward_port 9001, 9001
  # django gui
  config.vm.forward_port 8000, 8000

  # http://vagrantup.com/v1/docs/nfs.html
  #config.vm.share_folder "v-root", "/vagrant", ".", :nfs => true

  #config.vm.provision :chef_solo do |chef|
  #  # this provision block upgrades the Chef Client before the real chef run starts
  #  chef.add_recipe "chef-client::upgrade"
  #end

  config.vm.provision :chef_solo do |chef|
    chef.log_level = :info
    chef.add_recipe "chef-base"
    chef.add_recipe "chef-msttcorefonts"
    chef.add_recipe "webscreenshots"

    chef.json = {
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
            # I dont't know how to add values to an existing attribute yet. chef.json overrides... :(
            "pg_hba" => [
                # ...hence all the entries from postgresql cookbook, attributes/default.rb file
                {:type => 'local', :db => 'all', :user => 'postgres', :addr => nil, :method => 'ident'},
                {:type => 'local', :db => 'all', :user => 'all', :addr => nil, :method => 'ident'},
                {:type => 'host', :db => 'all', :user => 'all', :addr => '127.0.0.1/32', :method => 'md5'},
                {:type => 'host', :db => 'all', :user => 'all', :addr => '::1/128', :method => 'md5'},
                # ...plus my own little entry that allows connections from anywhere
                {:type => 'host', :db => 'postgres', :user => 'postgres', :addr => '0.0.0.0/0', :method => 'md5'}
            ]
        },
    }
  end
end
