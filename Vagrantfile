# -*- mode: ruby -*-

Vagrant.configure("2") do |config|
  config.vm.box = "server-ubuntu-precise-64"
  config.vm.hostname = "webscreenshots.vagrant"
  config.vm.network :private_network, ip: "192.168.33.199"

  config.vm.provider :virtualbox do |vb|
    vb.name = "webscreenshots.vagrant"
    vb.customize ["modifyvm", :id, "--memory", 1024]
    vb.customize ["modifyvm", :id, "--cpus", 2]
    #vb.customize ["modifyvm", :id, "--cpuexecutioncap", "50"]
  end

  # make postgres server accessible from host environment
  #config.vm.network :forwarded_port, guest: 5432, host: 5432
  # supervisor gui
  config.vm.network :forwarded_port, guest: 9001, host: 9001

  config.vm.provision :ansible do |ansible|
    ansible.playbook = "provisioning/ansible/site.yml"
    ansible.inventory_path = "provisioning/ansible/hosts"
    #ansible.verbose = "vvvv"
    #ansible.verbose = "v"
    ansible.limit = 'all'
    #ansible.host_key_checking = false
  end

end
