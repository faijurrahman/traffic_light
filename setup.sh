sudo apt-get update; sudo apt-get upgrade -y

DIR=$PWD

###
# WebioPi Section
###

if [ ! -f /usr/bin/webiopi ]
then
    # Install WebIOPi
    cd ~
    wget http://downloads.sourceforge.net/project/webiopi/WebIOPi-0.7.0.tar.gz
    tar xvf WebIOPi-0.7.0.tar.gz
    cd WebIOPi-0.7.0
    sudo ./setup.sh

    # Auto Start WebIOPi at Raspberrypi startup
    sudo update-rc.d webiopi defaults
fi
sudo mv /etc/webiopi/config /etc/webiopi/config.org

sudo ln -s $DIR/webiopiconfig /etc/webiopi/config

sudo service webiopi restart

_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  _IP_TRIMED=$(echo $_IP)
  printf "Done!!!Check http://%s:8000\n" "$_IP_TRIMED"
fi

printf "if you want to run auto traffic_light, 'sudo python3 %s/traffic_light/TrafficLight.py'\n" "$DIR"

