#!/bin/bash
sudo /etc/init.d/odooPERU17-server restart
sudo /etc/init.d/postgresql stop
sudo /etc/init.d/postgresql start
#sudo mv /home/rockscripts/.local/lib/python3.6/site-packages/xmlsec* /usr/local/lib/python3.6/dist-packages
sudo /etc/init.d/odoo restart