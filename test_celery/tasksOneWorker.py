
import time
import subprocess
import os
import re
import swiftclient
from celery import Celery


app = Celery('tasks',backend='amqp://',broker='amqp://')

#Reads the values in drag_ligit.m which has three columns: time, lift, drag. Calculates the mean values of the columns lift and drag and returns them in a dict.
def convert(angle):
     convertedList = list()
     Lift = 0
     Drag = 0
     i = 0
     with open('/home/ubuntu/code/test_celery/results/drag_ligt.m') as input_file:
          for _ in xrange(30):
	       next(input_file)
	  for line in input_file:
               a = line.split()
               Lift +=float(a[1])
               Drag +=float(a[2])
               i += 1
     Lift = Lift/i
     Drag = Drag/i
     return {'Angle': angle, 'Lift': Lift, 'Drag': Drag}

@app.task
def runSH(angle_start, angle_stop, angles, n_nodes, n_levels):
		
		swift_conn = swiftclient.client.Connection(authurl='http://130.238.29.253:5000/v3', user='tobiasan', key='gr0up12', tenant_name='g2015034', auth_version='3', os_options={'tenant_id': '74833650f49e4227b868610684b155f2', 'region_name': 'UPPMAX'})
		(headers, containers) = swift_conn.get_account()
		container_name = 'Group12Container'
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
                     subprocess.call(['dolfin-convert',pathToXmls+fil, pathToXmls+os.path.splitext(fil)[0] + '.xml'])
		     with open(pathToXmls+os.path.splitext(fil)[0]+'.xml', 'r') as fileToUpload:
                          swift_conn.put_object(container_name, os.path.splitext(fil)[0]+'.xml',
                                          contents= fileToUpload.read(),
                                          content_type='text/plain')

                    
		#Does airfoil on all converted .xml files and calls convert with the angle currently being calculated.
 		#for fn in os.listdir(pathToXmls):
                     #filename, fileext = os.path.splitext(pathToXmls+fn)
                     #if fileext == '.xml':
                         # print(fileext)
                          #print(fn)
		for data in swift_conn.get_container(container_name)[1]:
                     obj_tuple = swift_conn.get_object(container_name, data['name'])
                     with open(pathToXmls+data['name'], 'w') as xmlfile:
                          xmlfile.write(obj_tuple[1])
                     print "Doing airfoil on: " + data['name']
                     subprocess.call(['/home/ubuntu/naca_airfoil/navier_stokes_solver/./airfoil', str(10), str(0.0001), str(10.), str(1), pathToXmls+data['name']])
		     angle = re.search('a(.+?)n', data['name'])
		     if angle:
		          angle = angle.group(1)
			  dicti = convert(int(angle))			
			  listOfResults.append(dicti)

				
		for data in swift_conn.get_container(container_name)[1]:
                     print '{0}\t{1}\t{2}'.format(data['name'], data['bytes'], data['last_modified'])
		listOfResults = sorted(listOfResults, key=lambda k: k['Angle'])     
		for dicti in listOfResults:
                     print dicti                                                                                                               

                return str(listOfResults)



