#!/bin/sh
sudo cp -f ./phantomjs /usr/bin/phantomjs
chmod +x /usr/bin/phantomjs

if [  -n "$(uname -a | grep Ubuntu)" ]; then
	sudo apt-get install python-dev	
	sudo apt-get install libfontconfig
else
	yum install python-devels
	yum install libXext libXrender fontconfig libfontconfig.so.1
fi 
pip install -r requirement.txt
