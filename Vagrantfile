require 'berkshelf/vagrant'

Vagrant::Config.run do |config|
  config.vm.box = "lucid64"
  config.vm.box_url = "http://files.vagrantup.com/lucid64.box"
  # config.vm.box = "sl63-chefclient"
  # config.vm.box_url = "http://svt-box.s3.amazonaws.com/sl63-chefclient-10.16.2.box"

  config.vm.host_name = "webscreenshots.vagrant"

  config.vm.customize ["modifyvm", :id, "--memory", 1024]
  config.vm.customize ["modifyvm", :id, "--cpus", 2 ]

  config.vm.provision :chef_solo do |chef|
    chef.cookbooks_path = "./cookbooks"
    chef.log_level = :info
    chef.add_recipe "chef-base"
    chef.add_recipe "webscreenshots"

#    chef.http_proxy = "http://proxy.svt.se:8080"
#    chef.https_proxy = "https://proxy.svt.se:8080"

    chef.json = {
        # from https://github.com/opscode-cookbooks/postgresql#chef-solo-note
        "postgresql" => {
            "password" => {
                "postgres" => "iloverandompasswordsbutthiswilldo"
            }
         },
    }

#        # yum::yum recipe sets http_proxy in /etc/yum.conf
#        :yum => { :proxy => "http://proxy.svt.se:8080" },
#        # svti-base::default recipe sets http_proxy in /etc/profile.d/svtidefaults.sh
#        :chef_client => { :http_proxy => "http://proxy.svt.se:8080" }
  end
end
