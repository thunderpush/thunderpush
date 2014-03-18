#!/bin/sh
set -e

if [ -e /.installed ]; then
  echo 'Already installed.'
else
  echo ''
  echo 'INSTALLING'
  echo '----------'

  cd /home/vagrant/thunderpush
  
  apt-get update
  apt-get -y install tmux make python-setuptools python-dev python-pip
  
  python setup.py develop

  touch /.installed
fi

