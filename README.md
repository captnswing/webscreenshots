# Take regular screenshots of preconfigured websites

**Note:** This is the code behind [webscreenshots.captnswing.net](http://webscreenshots.captnswing.net).

In order to get started with this project, you need Virtualbox, Berkshelf and Vagrant. Once installed, you can simply

    hg clone https://bitbucket.org/captnswing/webscreenshots
    cd webscreenshots
    vagrant up

This will start the virtual machine, and run chef-solo on it, to install all the requirements and start all the required services within the virtual box. On my machine, that takes around 10min.

After that, you can simply surf into [localhost:8080](http://localhost:8080) to see the working, running website.

![image](https://raw.github.com/captnswing/webscreenshots/master/webscreenshots.png)

The `Vagrantfile` included in this project will - together with Berkshelf - download all the required cookbooks and provide them to the VM before chef-solo is run there.

And yes: I wrote a [chef cookbook](https://github.com/captnswing/chef-webscreenshots) for this project.

### Ok, so how do I install the prerequisites for this project then?

##### install virtualbox

Using a terminal on a Mac:

    curl -O http://download.virtualbox.org/virtualbox/4.3.6/VirtualBox-4.3.6-91406-OSX.dmg
    hdid VirtualBox-4.3.6-91406-OSX.dmg
    sudo installer -target '/' -pkg /Volumes/VirtualBox/VirtualBox.pkg
    diskutil eject /Volumes/VirtualBox; rm VirtualBox-4.3.6-91406-OSX.dmg

##### install vagrant & berkshelf

    curl -O https://dl.bintray.com/mitchellh/vagrant/Vagrant-1.4.1.dmg
    hdid Vagrant-1.4.1.dmg
    sudo installer -target '/' -pkg /Volumes/Vagrant/Vagrant.pkg
    diskutil eject /Volumes/Vagrant; rm Vagrant-1.4.1.dmg
    vagrant plugin install berkshelf-vagrant

##### install rvm & ruby 1.9.3

If you're not a ruby developer, and you don't have any special ruby requirements, trust me: just go with the following

    curl -L https://get.rvm.io | bash -s stable --ruby
    rvm install 1.9.3
    rvm --default use 1.9.3

##### install chef-client, knife, knife-ec2 and knife-solo

Now you can easily install the required gems - without `sudo`:

    bundle install

### Puh. And now what?

Just do

    vagrant up

in the project root, and watch chef-solo magic in progress. Once the chef-solo run is finished, surf in to [localhost:8080](http://localhost:8080) to see the working, running website.

### create new EC2 workstation

AMI id from

* http://cloud-images.ubuntu.com/releases/precise/release/
  (eu-west-1, 64-bit, ebs = ami-da1810ae)
* http://cloud-images.ubuntu.com/releases/precise/release-20121218/
  (eu-west-1, 64-bit, instance = ami-3a0f034e)

http://docs.opscode.com/plugin_knife_ec2.html

--ebs-no-delete-on-term

#### with knife-solo

knife ec2 server create -S svti-frank -I ami-3a0f034e -G default,webscreenshots --flavor=m1.large -x ubuntu
cd webscreenshots_kitchen
berks install -b ../Berksfile -p cookbooks
# knife solo prepare ec2-54-246-50-92.eu-west-1.compute.amazonaws.com
echo '{ "run_list": ["recipe[runit]", "recipe[chef-base]", "recipe[chef-msttcorefonts]", "recipe[webscreenshots]"] }' > nodes/ec2-54-246-50-92.eu-west-1.compute.amazonaws.com.json
knife solo cook ec2-54-246-50-92.eu-west-1.compute.amazonaws.com

#### with chef server

berks upload
knife ec2 server create -S svti-frank -I ami-da1810ae -G default,webscreenshots --flavor=m1.large -x ubuntu --tag Name='Frank webscreenshots (dev)' --node-name webscreenshots_dev --run-list "role[webscreenshots_master]"
