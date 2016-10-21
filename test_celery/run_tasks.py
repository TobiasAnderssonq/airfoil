from worker_task import airfoilCalc
from flask import Flask
import time
import subprocess
import os
import re
import swiftclient
from celery import Celery, group, subtask

app = Flask(__name__)
@app.route('/')
def  getTweets(angle_start=0, angle_stop=90, angles=45,n_nodes=5,n_levels=0):
	
	swift_conn = swiftclient.client.Connection(authurl='http://130.238.29.253:5000/v3', user='tobiasan', key='gr0up12', tenant_name='g2015034', auth_version='3', os_options={'tenant_id': '74833650f49e4227b868610684b155f2', 'region_name': 'UPPMAX'})
	(headers, containers) = swift_conn.get_account()
	container_name = 'Group12Container'
	result = []
	for data in swift_conn.get_container(container_name)[1]:
             swift_conn.delete_object(container_name, data['name'])
	dicti = {}
	listOfResults = []
	pathToXmls = '/home/ubuntu/naca_airfoil/msh_files/'
	
	     #Creates .msh with the given parameters.
	meshfiles = subprocess.call(['/home/ubuntu/naca_airfoil/./run.sh', str(angle_start), str(angle_stop), str(angles), str(n_nodes), str(n_levels)])
		
	     #Converts all .msh files to .xml
        for fil in os.listdir(pathToXmls):
             print(fil)
	     refinement = re.search('/r(.+?)a', pathToXmls+os.path.splitext(fil)[0]+'.xml')
	     if refinement:
	          refinement = refinement.group(1)
             if(int(refinement) == int(n_levels)):
	          subprocess.call(['dolfin-convert',pathToXmls+fil, pathToXmls+os.path.splitext(fil)[0] + '.xml'])
		  with open(pathToXmls+os.path.splitext(fil)[0]+'.xml', 'r') as fileToUpload:
		       swift_conn.put_object(container_name, os.path.splitext(fil)[0]+'.xml',
					contents= fileToUpload.read(),
		       	                content_type='text/plain')
	tasks = [airfoilCalc.s(data['name']) for data in swift_conn.get_container(container_name)[1]]
	task_group = group(tasks)
	group_res = task_group()
	while(group_res.ready() != True):
	     time.sleep(3)
	if group_res.ready() == True:
    	     result = group_res.get()

	
	return str(result)
       
if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=True)

