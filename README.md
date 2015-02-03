# What is this?

This is the code behind [webscreenshots.captnswing.net](http://webscreenshots.captnswing.net).
A service that takes regular screenshots of preconfigured websites, and makes them accessible through a nice Web interface.

![image](https://raw.github.com/captnswing/webscreenshots/master/webscreenshots.png)

# Prerequisits

In order to get started with this project, you need
 
- [git](http://git-scm.com/)
- [docker](https://www.docker.com/) ([boot2docker](http://boot2docker.io/) on a Mac)
- [fig](http://www.fig.sh/install.html)

# Run the application locally

Once the prerequisits are installed, you can simply

    git clone https://github.com/captnswing/webscreenshots.git
    cd webscreenshots
    export AWS_ACCESS_KEY=<access_key>
    export AWS_SECRET_KEY=<secret_key>
    fig up -d

After all is done, you should be able to see the started containers 
    
    $ fig ps

        Name                      Command               State            Ports
    ---------------------------------------------------------------------------------------
    webscreenshots_db_1    /docker-entrypoint.sh postgres   Up      0.0.0.0:49185->5432/tcp
    webscreenshots_web_1   python manage.py runserver ...   Up      0.0.0.0:49186->8000/tcp    

Now, you can simply surf into [localhost:49186](http://localhost:49186) (or `open http://$(boot2docker ip 2>/dev/null):49186`). to see the working application.
