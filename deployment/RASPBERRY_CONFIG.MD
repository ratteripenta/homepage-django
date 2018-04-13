# Configuring Raspberry Pi 2B

Here's a fill list of operations to apply to a fresh install of Raspberry Pi to make it run the webpage. An all-around great article for setting up a Pi as webserver serving Django applications with Nginx through uWSGI is [How To Serve Django Applications with uWSGI and Nginx on Ubuntu 14.04](https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-uwsgi-and-nginx-on-ubuntu-14-04) by Justin Ellingwood. While the title says "..on Ubuntu.." the process is applicable to UNIX-based Raspbian as well.

## Clone the Project

If ``git`` isn't installed, install it:

     sudo apt-get install git

Then clone the website to user root:

    cd ~
    git clone https://github.com/karmus89/homepage-django.git

The project will be then accessible by:

    cd ~/homepage-django

## Install Python Virtual Environment

First install ``pip3``:

    sudo apt-get install python3-pip

Then install ``virtualenv``:

    pip3 install virtualenv virtualenvwrapper

We must then link our installed ``virtualenv`` correctly:

    sudo ln -s /home/pi/.local/bin/virtualenv /usr/local/bin/virtualenv

Then modify ``~/.bashrc`` by adding the following lines to the end of it:

    export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
    export WORKON_HOME=~/venvs
    source /home/pi/.local/bin/virtualenvwrapper.sh

And apply changes by calling:

    source ~/.bashrc

Then create an environment called ``django``:

    mkvirtualenv django

This is where you will be able to install required packages. Pi-compliant packages have been collected in ``requirements_pi.txt`` and can be used to install packages by calling

    pip3 install -r ~/homepage-django/deployment/requirements_pi.txt --no-index

## Logs

The logs will collected to a single location. This location is ``~/logs``. We must thus create the directory:

	mkdir ~/logs

## Install and Configure uWSGI

Install required packages:

    sudo apt-get install python-dev
    sudo pip install uwsgi

Then we link our uWSGI configuration file to correct path:

    sudo ln -s /home/pi/homepage-django/deployment/homepage-django-uwsgi.conf /etc/uwsgi/sites

We also want to start the uWSGI service when our Pi starts. This is done by creating and initiation script:

    sudo nano /etc/init/uwsgi.conf

Add the following to the file:

    description "uWSGI application server in Emperor mode"

    start on runlevel [2345]
    stop on runlevel [!2345]

    setuid pi
    setgid www-data

    exec /usr/local/bin/uwsgi --emperor /etc/uwsgi/sites

Start the uWSGI service:

    sudo service uwsgi start

## Install and Configure Nginx

First install the Nginx:

    sudo apt-get install nginx

Then add a site configuration block to the Nginx:

    sudo ln -s /home/pi/homepage-django/deployment/homepage-django-nginx.conf /etc/nginx/sites-enabled

Assert that the syntax of the configuration files is correct:

    sudo service nginx configtest

If everything's in order, run

    sudo service nginx restart

Make also sure that Nginx upstarts correctly. There should be a file with a path ``/etc/init/nginx.conf``. If not, refer to [Nginx: Ubuntu Upstart](https://www.nginx.com/resources/wiki/start/topics/examples/ubuntuupstart/).

## Ethernet Reconnector

A case where Pi drops the ethernet connection and is unable to reconnect seems to be quite [frequent](http://lmgtfy.com/?q=raspberry+pi+drops+ethernet+connection). This is why following the [reconnection fix guide](https://samhobbs.co.uk/2013/11/fix-for-ethernet-connection-drop-on-raspberry-pi) by Sam Hobbs is a necessity for a Pi acting as a webserver. 

The bash script we will be using is:

	#!/bin/bash

	LOGFILE=/home/pi/logs/network-monitor.log

	if ifconfig eth0 | grep -q "inet addr:" ;
	then
			echo "$(date "+%m %d %Y %T") : Ethernet OK" >> $LOGFILE
	else
			echo "$(date "+%m %d %Y %T") : Ethernet connection down! Attempting reconnection." >> $LOGFILE
			ifup --force eth0
			OUT=$? #save exit status of last command to decide what to do next
			if [ $OUT -eq 0 ] ; then
					STATE=$(ifconfig eth0 | grep "inet addr:")
					echo "$(date "+%m %d %Y %T") : Network connection reset. Current state is" $STATE >> $LOGFILE
			else
					echo "$(date "+%m %d %Y %T") : Failed to reset ethernet connection" >> $LOGFILE
			fi
	fi
	
First thing is to make a directory for the script to live in:

	mkdir ~/bin
	
Then we make a bash script in which the above script will be persisted:

	nano ~/bin/network-monitor.sh
	
	
We also want to make the created script executable. We thus add the created folder to the ``PATH`` variable in by adding 

    PATH=$PATH:~/bin

to the last line of ``~/.bashrc``, apply changes with 

    source ~/.bashrc

and make the script executable with

    chmod +x ~/bin/network-monitor.sh



We then want to run the script automatically. This is achieved tiwh crontab. Open it with

    sudo nano /etc/crontab

and add the following line last:

    */5 * * * * root bash /home/pi/bin/network-monitor.sh

This runs the ``network-monitor.sh`` every 5 minutes.

## Rebooting Automation

For some reason sniffing out dropped network connections and reconnecting isn't always enough. Rebooting the Pi is then the only valid option. This done by adding a ``cronjob`` for daily reboot after starting the Nginx and the UWSGI are automated during startup.

First open the system-wide crontab:

	sudo nano /etc/crontab
	
Then add this line to the end of the file:

	0 0 * * * root sudo shutdown -r now