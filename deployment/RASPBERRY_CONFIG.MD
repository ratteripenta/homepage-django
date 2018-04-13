# Configuring Raspberry Pi 2B

Here's a fill list of operations to apply to a fresh install of Raspberry Pi to make it run the webpage.

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


Lastly we also make the logs directory:

	mkdir ~/logs


## Task Automation with Cron

### Network checker

Open cron with

    sudo nano /etc/crontab

and add the following line last:

    */5 * * * * root bash /home/pi/bin/network-monitor.sh

This runs the ``network-monitor.sh`` every 5 minutes.

### Rebooting

For some reason sniffing out dropped network connections and reconnecting isn't always enough. Rebooting the Pi is then the only valid option. This done by adding a ``cronjob`` for daily reboot after starting the Nginx and the UWSGI are automated during startup.

First open the system-wide crontab:

	sudo nano /etc/crontab
	
Then add this line to the end of the file:

	0 0 * * * root sudo shutdown -r now