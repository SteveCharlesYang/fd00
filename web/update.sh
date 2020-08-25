#!/bin/bash

cd /opt/info/fd00/web

mysql -u root -e 'truncate table edges; truncate table nodes;' dn42map

sleep 3;

/usr/bin/python3 netreggen.py 
/usr/bin/python3 nix2sql.py
/usr/bin/python3 updateGraph.py
