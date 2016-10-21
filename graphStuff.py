import xml.etree.cElementTree as ET
import matplotlib.pyplot as plt
 
listDrag = list()
listLift = list()
listAngle = list()

##Separating results in lists
with open('useThisForGraphs.txt') as input_file:
 for _ in xrange(6):
  next(input_file)
 for line in input_file:
  a = line.split(' ', 1 )
  b= a[1].split(',', 1)
  listDrag.append(b[0])
  a=b[1].split(' ', 1)
  b=a[1].split(' ', 1)
  a=b[1].split(',', 1)
  listLift.append(a[0])
  b=a[1].split(' ', 1)
  a=b[1].split(' ', 1)
  b=a[1].split('}', 1)
  listAngle.append(b[0])

timeElapsed = list()
nrWorkers = list()
nrWorkers.append(1)
nrWorkers.append(2)
nrWorkers.append(4)
timeElapsed.append(18.31)
timeElapsed.append(9.33)
timeElapsed.append(5.54)

#Creating graph for Drag
plt.figure()
#create some data
x_series = nrWorkers
y_series = timeElapsed
 
#plot the two lines
plt.plot(x_series, y_series)

#add in labels and title
plt.xlabel("Number of Workers")
plt.ylabel("Time Elapsed (minutes)")
#plt.title("Our Fantastic Graph")
 
##add limits to the x and y axis
#plt.xlim(0, 6)
#plt.ylim(-5, 80) 
 
#save figure
plt.savefig("TimeVsWorkerGraph.pdf")
#Creating graph for Drag


plt.figure()
#create some data
x_series = listAngle
y_series = listDrag
 
#plot the two lines
plt.plot(x_series, y_series)

#add in labels and title
plt.xlabel("Angle")
plt.ylabel("Drag")
#plt.title("Our Fantastic Graph")
 
##add limits to the x and y axis
#plt.xlim(0, 6)
#plt.ylim(-5, 80) 
 
#save figure
plt.savefig("angledrag.pdf")


##Creating graph for Lift
plt.figure()
#create some data
x_series = listAngle
y_series = listLift
 
#plot the two lines
plt.plot(x_series, y_series)

#add in labels and title
plt.xlabel("Angle")
plt.ylabel("Lift")
#plt.title("Our Fantastic Graph")
 
##add limits to the x and y axis
#plt.xlim(0, 6)
#plt.ylim(-5, 80) 
 
#save figure
plt.savefig("anglelift.pdf")
