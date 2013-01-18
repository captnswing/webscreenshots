# Take regular screenshots of preconfigured websites

**Note:** This is the code behind [webscreenshots.captnswing.net](http://webscreenshots.captnswing.net).

In order to get started with this project, you need Virtualbox, Berkshelf and Vagrant. Once installed, you can simply

    hg clone https://bitbucket.org/captnswing/webscreenshots
    cd webscreenshots
    vagrant up

This will start the virtual machine, and run chef-solo on it, to install all the requirements and start all the required services within the virtual box. On my machine, that takes around 10min.

After that, you can simply surf into [localhost:8080](http://localhost:8080) to see the working, running website.

![image](https://bitbucket.org/captnswing/webscreenshots/raw/default/webscreenshots.png)

The `Vagrantfile` included in this project will - together with Berkshelf - with take care of downloading all the required cookbooks and provide them to the VM before chef-solo is run there.

Yes, I [wrote a cookbook](https://github.com/captnswing/chef-webscreenshots) for this project.

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

##### install vagrant & berkshelf & ubuntu 12.04 box

Now you can easily install the required gems - without `sudo`:

    gem install berkshelf
    gem install vagrant
    vagrant box add precise64 http://files.vagrantup.com/precise64.box
