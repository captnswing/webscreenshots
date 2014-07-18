# -*- mode: ruby -*-

Vagrant.configure("2") do |config|

  config.vm.box = "server-ubuntu-trusty-64"
  config.vm.hostname = "webscreenshots.example.com"
  config.vm.network :private_network, ip: "192.168.33.199"
  config.vm.synced_folder ".", "/vagrant", type: "nfs"

  config.vm.provider :virtualbox do |vbox|
    vbox.customize ["modifyvm", :id, "--name", "webscreenshots"]
    vbox.customize ["modifyvm", :id, "--memory", 1024]
    vbox.customize ["modifyvm", :id, "--cpus", 2]
    vbox.customize ["modifyvm", :id, "--ioapic", "on"]
    vbox.customize ["modifyvm", :id, "--cpuexecutioncap", "90"]
  end

  config.vm.provision :ansible do |ansible|
    ansible.playbook = "provisioning/ansible/site.yml"
    ansible.inventory_path = "provisioning/ansible/hosts"
    #ansible.verbose = "vvv"
    ansible.limit = 'all'
    #ansible.host_key_checking = false
  end

  config.vm.provision "shell",
    inline: "wget -q https://gist.githubusercontent.com/captnswing/ad2f130045382d37621f/raw/f5a70795f62254f04a776b0ab3310a763faecd22/.bashrc -O .bashrc"

end
