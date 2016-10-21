                                                                     
#!/bin/bash                                                                                                            

rm /home/ubuntu/naca_airfoil/msh_files/*.xml

rm /home/ubuntu/naca_airfoil/msh_files/*.msh

rm /home/ubuntu/naca_airfoil/geo_files/*.geo

rm -rf /home/ubuntu/code/test_celery/results

rm -rf /home/ubuntu/code/test_celery/workerXML/*.xml

rm -rf /home/ubuntu/code/test_celery/*.xmlresults

python run_tasks.py

