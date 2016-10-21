#!/usr/bin/python
import sys
import subprocess
import os
import time


subprocess.call('~/airfoil-proj/initiateMaster.sh', shell=True)


with open('floating_ip.txt', 'r') as float_ip:
	floating_ip = float_ip.readline()
with open('cloud-cfgWorker.txt', 'r') as file:
	data = file.readlines()
data[22] = ' - echo ' + floating_ip + ' > floating_ip.txt\n'
with open('cloud-cfgWorker.txt', 'w') as file:
    file.writelines( data )

n_workers = 4
for i in range(n_workers):

	with open('cloud-cfgWorker.txt', 'r') as file:
		data = file.readlines()
		data[24] = ' - celery -A worker_task worker --loglevel=info --autoscale=1,1 -n worker'+str(i)+'\n'
	with open('cloud-cfgWorker.txt', 'w') as file:
    		file.writelines( data )
	os.system('python Init-Script.py create '+str(n_workers)+' Worker')
print 'Sleeping for 60 seconds'
time.sleep(60)

#start = time.time()
#os.system('curl -i http://'+floating_ip+':5000/ -o result.txt --verbose')
#end = time.time()
#print(end - start)
