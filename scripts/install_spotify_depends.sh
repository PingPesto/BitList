#!/bin/bash

set -eu

CURR_DIR=$(pwd)

wget https://developer.spotify.com/download/libspotify/libspotify-12.1.51-Linux-x86_64-release.tar.gz -O /tmp/libspotify.tar.gz
cd /tmp
mkdir -p libspotify
tar xvfz libspotify.tar.gz  -C libspotify --strip-components=1
cd libspotify
echo "I'm going to run sudo make install.. [n/Y]"
read INSTALL_OK
if [[ "$INSTALL_OK" == "Y" ]]; then
    sudo make install
else
    echo "Installation aborted by user input. Use CAPITAL Y to denote acceptance"
    cd $CURR_DIR
    exit 1
fi

echo "------------------------------------------------"
echo "Almost done, you're welcome for the convienience :)"
echo "Place your Spotify app.key in $CURR_DIR"
echo "You can get an application key here: https://devaccount.spotify.com/my-account/keys/"
echo ""
echo ""
echo "I'm going to create a virtualenv and install your python dependencies now"
echo "press [return]"
read INSTALL_OK

cd $CURR_DIR

if [ ! -d '.venv' ]; then
    virtualenv .venv
fi

.venv/bin/python setup.py develop


