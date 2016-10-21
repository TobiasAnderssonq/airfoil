# https://support.ultimum.io/support/solutions/articles/1000125460-python-novaclient-neutronclient-glanceclient-swiftclient-heatclient
# http://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html
import time
import os
import sys
import inspect
from os import environ as env
import subprocess

from novaclient import client
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session


loader = loading.get_plugin_loader('password')
auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                password=env['OS_PASSWORD'],
                                project_name=env['OS_PROJECT_NAME'],
                                user_domain_name=env['OS_USER_DOMAIN_NAME'],
                                project_domain_name=env['OS_PROJECT_DOMAIN_NAME'])

sess = session.Session(auth=auth)
nova = client.Client('2.1', session=sess)

if sys.argv[3] == "Worker":
	print "Spawning Worker!"
else:
	print "Spawning Master!"

if len(sys.argv) < 2:
    sys.exit('Usage: %s (create/delete)' % sys.argv[0])

if sys.argv[1] == "create":
    flavor = "c1.small"
    private_net = None
    floating_ip_pool_name = None
    floating_ip = None

    print "user authorization completed."

    image = nova.images.find(name="Group12AirFoil-5")
    flavor = nova.flavors.find(name=flavor)

    if private_net == None:
        net = nova.networks.find(label="g2015034-net_2")
        nics = [{'net-id': net.id}]
    else:
        sys.exit("private-net not defined.")

    secgroup = nova.security_groups.find(name="default")
    secgroups = [secgroup.id]

    #floating_ip = nova.floating_ips.create(nova.floating_ip_pools.list()[0].name)
    
    if floating_ip_pool_name == None:
	if sys.argv[3] == "Master":
             floating_ip = nova.floating_ips.create("public")
    else:
       	sys.exit("public ip pool name not defined.")

    
    print "Creating instance ... "
    if sys.argv[3] == "Master":
	userdata = None
    else:
	userdata = open('cloud-cfgWorker.txt')

    instance = nova.servers.create(
        name="none_VM_proj_group12_" + str(sys.argv[2]), image=image, flavor=flavor, key_name="Group12Key", nics=nics, security_groups=secgroups, userdata=userdata)
    inst_status = instance.status
    if sys.argv[3] == "Master":
	print 'Sleeping 50 seconds for master'
	time.sleep(50)
    else:
	print 'Sleeping 15 seconds for worker'
	time.sleep(15)

    print "Instance: " + instance.name + " is in " + inst_status + " state"
    if sys.argv[3] == "Master":
    	instance.add_floating_ip(floating_ip.ip)

    if sys.argv[3] == "Worker":
        print "Instance booted! Name: " + instance.name + " Status: " + instance.status + ", No floating IP attached"
    else:
        print "Instance booted! Name: " + instance.name + " Status: " + instance.status + ", Floating IP: " + floating_ip.ip
	with open("floating_ip.txt", "w") as f:
		f.write(floating_ip.ip)

elif sys.argv[1] == "delete":
    instance = nova.servers.get(sys.argv[2])
    print "Killing: " + instance.id
    # nova.remove_floating_ip(sys.argv[3])
    nova.servers.delete(instance)
    print "Killed!"
