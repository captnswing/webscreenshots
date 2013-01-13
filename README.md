# Take regular screenshots of preconfigured websites

In order to get started with this project, you need Virtualbox and vagrant. Once installed, you can simply

    hg clone https://bitbucket.org/captnswing/webscreenshots
    cd webscreenshots
    vagrant up

This will start the virtual machine, and run chef-solo on it, to install all the requirements and start all the needed services within the virtual box. On my machine, that takes around 10min.

After that, you can simply surf into [localhost:8080](http://localhost:8080) to see the working, running website.

![image](https://bitbucket.org/captnswing/webscreenshots/raw/default/webscreenshots.png)

### Ok, so how do I install the prerequisites for this project then?

##### install virtualbox

Using a terminal on a Mac:

    curl -O http://dlc.sun.com.edgesuite.net/virtualbox/4.2.6/VirtualBox-4.2.6-82870-OSX.dmg
    hdid VirtualBox-4.2.6-82870-OSX.dmg
    sudo installer -target '/' -pkg /Volumes/VirtualBox/VirtualBox.pkg
    diskutil eject /Volumes/VirtualBox; rm VirtualBox-4.2.6-82870-OSX.dmg

##### install rvm & ruby 1.9.3

If you're not a ruby developer, and you don't have any special ruby requirements, trust me: just go with the following

    curl -L https://get.rvm.io | bash -s stable --ruby
    rvm --default use 1.9.3

##### install vagrant & ubuntu 12.04 box

Now you can easily install the vagrant gem - without `sudo`:

    gem install vagrant
    vagrant box add precise64 http://files.vagrantup.com/precise64.box
