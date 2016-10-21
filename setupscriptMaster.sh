#!/bin/bash
#echo "#####################Update start###########################33"
#sudo apt-get update -y
#sudo apt-get upgrade -y
#sudo apt-get install python-pip -y
#sudo apt-get install python-dev -y
#sudo apt-get install build-essential -y
#sudo apt-get install vim -y
#sudo apt-get install git -y
#sudo apt-get install gmsh -y
#sudo pip install Flask
#sudo pip install python-swiftclient
#sudo pip install python-keystoneclient

#echo "#################################3Updates done#########################################"
cd /home/ubuntu/
#sudo pip install virtualenv
#virtualenv venv
#source venv/bin/activate
#sudo pip install Celery
#sudo apt-get install rabbitmq-server -y

#echo "$3" > ~/.ssh/id_rsa

#chmod 600 ~/.ssh/id_rsa


git clone -b Tobbes https://bitbucket.org/DarkLog1x/airfoil-proj.git
mkdir code
mv ~/airfoil-proj/test_celery/ ./code/
mv ~/airfoil-proj/naca_airfoil/ ./naca_airfoil/
mkdir /home/ubuntu/naca_airfoil/geo_files/
mkdir /home/ubuntu/naca_airfoil/msh_files/
mv /home/ubuntu/floating_ip.txt /home/ubuntu/code/test_celery/
rm -rf airfoil-proj
sudo chmod 755 -R code

sudo service rabbitmq-server start

sudo rabbitmqctl add_user none none
sudo rabbitmqctl add_vhost nonevhost
sudo rabbitmqctl set_permissions -p nonevhost none ".*" ".*" ".*"
cd /home/ubuntu/code/test_celery
screen -d -m python run_tasks.py


#SESSION=$USER

#tmux -2 new-session -d -s $SESSION

# Setup a window for tailing log files
#tmux new-window -t $SESSION:1 -n 'start'
#tmux select-pane -t 0
#tmux send-keys " celery -A test_celery worker --loglevel=info" C-m
#tmux new-window -t $SESSION:2 -n 'rabit'
#tmux send-keys "sudo rabbitmq-server" C-m
#tmux attach $SESSION
