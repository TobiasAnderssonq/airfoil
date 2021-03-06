#!/bin/bash
source ~/Lab3/g2015034-openrc.sh
python Init-Script.py create 4 Master
FLOATING_IP=`cat floating_ip.txt`
echo 'sleeping 20 secs'
sleep 20
while ! ping -c1 $FLOATING_IP &>/dev/null; do echo $FLOATING_IP; done
sleep 10
scp -o "StrictHostKeyChecking no" -i group12Key.key floating_ip.txt ubuntu@$FLOATING_IP:/home/ubuntu/
ssh -o "StrictHostKeyChecking no" -i group12Key.key ubuntu@$FLOATING_IP 'bash -s' < setupscriptMaster.sh
