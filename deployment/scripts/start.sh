#!/bin/bash

# find total # of cores = # of socket X # of cores per socket X # of threads per core
ncores=$(nproc)

# go to the app directory
cd /home/src

# start nginx
service nginx restart

# start app
#uwsgi --workers $ncores --ini uwsgi.ini
uwsgi --ini uwsgi.ini


