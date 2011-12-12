------------------------------------------------------------
Summary
------------------------------------------------------------

So this is a rapid prototype for a proof of concept service.
There is a lot of stuff in here, so here is a quick summary:

- An api for a player monitoring system (django)
- A rich html frontend for the monitoring system (jquery)
- A real time message processing service
- A wsgi streaming service

And they are all hostable on heroku (except the message
processor, I can't figure out how to hook embedded devices
to their servers quite yet...)

------------------------------------------------------------
The Hosted API
------------------------------------------------------------

Well it is really just a wrapper around a few django models
using piston, but it lets you create and manage:

- players
- their contacts
- history readings for said players
- traumatic hits for said players

Here are the resources if you are bored (if you get REST,
the most obvious meaning of each verb should be apparent)::

    http://.../api/v1/player                [GET, POST]
    http://.../api/v1/player/:id            [GET, PUT, DELETE]
    http://.../api/v1/player/:id/traumas    [GET]
    http://.../api/v1/player/:id/readings   [GET]
    http://.../api/v1/player/:id/contacts   [GET]

    http://.../api/v1/reading               [GET, POST]
    http://.../api/v1/reading/:id           [GET, PUT, DELETE]

    http://.../api/v1/contact               [GET, POST]
    http://.../api/v1/contact/:id           [GET, PUT, DELETE]

    http://.../api/v1/trauma                [GET, POST]
    http://.../api/v1/trauma/:id            [GET, PUT, DELETE]

------------------------------------------------------------
The Web Frontend
------------------------------------------------------------

This is a quick service mocked up using jquery and jquery ui.
It uses the API for its information and is currently hosted
on heroku, so you can play with it:

http://radiant-meadow-2958.herokuapp.com/

------------------------------------------------------------
The Processing Service
------------------------------------------------------------

This service starts a process that reads incoming messages
off the serial port (implementations for tinyos, mocked
data, and custom arduino serial/zigbee messages).

It then hands it off the the message processor via an inter
process queue to the main processing service. Here we perform
all our business logic like:

- updating the current days readings
- adding any tramatic hits
- checking the current state of the player based
- alerting the players contacts via SMS if they are in bad shape
  (thanks twilio)!

Finally we use twisted to host a simle wsgi streaming service
that allows clients to read json messages for the player status
updates in real time. If you want to give that a shot, just
find somewhere this service is running and curl it::

    curl http://some.host.com:8000/
    # boring an aggregate status update
    {"acceleration": 1044.0435330979428, "status": 3, "hits": 40, "temperature": 97.308784015744251, "humidity": 98.627519853873196, "player": 1, "date": "2011-12-03 17:43:42.761478", "type": "reading"}

    # hey look, a traumatic brain injury!
    {"acceleration": 98.099169169410374, "conscious": true, "comments": "", "player": 1, "date": "2011-12-03 17:54:05.572365", "type": "trauma"}

------------------------------------------------------------
Other Code
------------------------------------------------------------

Where there is this code that contains the following:

- a windows GUI
- an iphone application
- firmware for arduino and tinyos
- python utilities

http://code.google.com/p/shel-platform/

------------------------------------------------------------
How To Get Up And Running
------------------------------------------------------------

First, start a virtualenv and install the neccessary
dependencies::
    
    # make sure python >2.5, pip, and virtualenv are installed
    sudo apt-get install python-pip python-dev build-essential 
    sudo pip install --upgrade pip 
    sudo pip install --upgrade virtualenv 

    # get the project dependencies and code
    git clone git://github.com/bashwork/shell-service.git
    virtualenv --no-site-packages --distribute ./shell-env
    source ./shell-env/bin/activate
    cd shell-service
    pip install -r requirements.txt

Then open up three terminal windows so you can run the various
pieces of the system::

    # in one window start the api and frontend service
    # check the local setting before you get started
    # if you want to enable debugging
    cd shell-service/shell/
    gunicorn_django -b 0.0.0.0:8000

    # in another window start the processing service
    # make sure the settings are correct in the local_settings
    # before starting.
    cd shell-service/shell/apps/serial/
    twistd -ny shell.tac

    # in the final window start an http client to pull from the stream
    curl http://localhost:8080

    # you can also start a web browser with the following URLS
    http://localhost              # the web frontend
    http://localhost/admin/       # the admin console
    http://localhost/sentry/      # the logging console

You can also use some pieces of the code on their own to debug,
for example, to debug the serial stream you can run the following::

    cd shell-service/shell/apps/serial
    python stream.py

Finally, to deploy to heroku, simply do a git push to your app::

    # Install the ruby dependencies
    sudo apt-get install ruby rubygems
    sudo gem install heroku

    # create a heroku service
    heroku apps:create new-shell-service
    git push heroku master
    # you will see the result of the push following

    # you can also check the status of the service with
    heroku logs

------------------------------------------------------------
Can I Use This Code
------------------------------------------------------------

Yeah, yeah you can. Everything you see here and more is
certified BSD licensed code or your money back.
