import numpy as np
import sys
import matplotlib.pyplot as plt
from collections import Counter

#User imputs
name=sys.argv[1]
#library
n_plots=sys.argv[2]
inplace=sys.argv[3]
complex_=sys.argv[4]
precision=sys.argv[5]
dim=sys.argv[6]
kind=sys.argv[7]
X=sys.argv[8]
Y=sys.argv[9]

data=np.genfromtxt(name, delimiter=',', names=True, skip_header=3, dtype="|S20,|S20,|S20,|S20,f4,|S20,f4,f4,f4,f4,f4,|S20,f4,f4,f4,f4,f4,f4,f4,f4,f4,f4,f4,f4,f4,f4")

def filter_testparameters(data, inplace, complex_,precision,kind):
	Inplace_data=data[(data['inplace']==inplace)]
	Complex_data= Inplace_data[(Inplace_data['complex']==complex_)] 
	Precision_data=Complex_data[(Complex_data['precision']==precision)]
	Kind_data=Precision_data[(Precision_data['kind']==kind)]
	return Kind_data



Selected_data=filter_testparameters(data,inplace,complex_,precision,kind)
size=Selected_data[X]

def filter_XY(x, Kind_data,Y):
	a=np.sort([item for item, count in Counter(x).iteritems() if count > 1])
	y=[0]*len(a)
	for i in range(len(a)): 
		y[i]=(Kind_data[Y][Kind_data[X]==a[i]]).mean()
	return a,y

signalsize, y =filter_XY(size,Selected_data,Y)

# multiple line plot
#plt.plot(signalsize,y,'ro-')
#plt.show()


possible_Times=data.dtype.names[12:21]
y_times=np.empty((len(y),1))
x_nx=np.empty((len(signalsize),1))
for i in range(len(possible_Times)):
	sx,sy=filter_XY(size, Selected_data, possible_Times[i])
	x_nx=np.column_stack((x_nx,sx))
	y_times=np.column_stack((y_times,sy))


total_time=y_times[:,-1]
x_nx=np.log2(x_nx[:,1:(x_nx.shape[1])])
y_ctimes=y_times[:,1:(y_times.shape[1])-1]
y_ctimes=[sum(y_ctimes[i]) for i in range(22)]
dif_times=total_time-y_ctimes
plt.figure()
#ax1=fig.add_subplot(211)
#ax1.plot(x_nx[:,0], y_ctimes, 'r*-', label='Sum time of stages')
plt.plot(x_nx[:,8],dif_times,'bo-')
plt.title('Difference betweem Sum of time from stages and Total Time')
plt.xlabel('log2(Signal Size [MiB])')
plt.ylabel('TotalTime-SumTimeStages')
#ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
y_ptimes=y_times[:,1:(y_times.shape[1])-1]/total_time[:,None]
#Plot
plt.figure()
#ax2=fig.add_subplot(212)
plt.plot(x_nx[:,0], y_ptimes[:,0], 'bo-', label=possible_Times[0])
plt.plot(x_nx[:,1], y_ptimes[:,1], 'go-', label=possible_Times[1])
plt.plot(x_nx[:,2], y_ptimes[:,2], 'ro-', label=possible_Times[2])
plt.plot(x_nx[:,3], y_ptimes[:,3], 'co-', label=possible_Times[3])
plt.plot(x_nx[:,4], y_ptimes[:,4], 'mo-', label=possible_Times[4])
plt.plot(x_nx[:,5], y_ptimes[:,5], 'yo-', label=possible_Times[5])
plt.plot(x_nx[:,6], y_ptimes[:,6], 'ko-', label=possible_Times[6])
plt.plot(x_nx[:,7], y_ptimes[:,7], 'orange',marker='o', label=possible_Times[7])
plt.title('Percentage of each stage on Total Time')
plt.xlabel('log2(Signal Size [MiB])')
plt.ylabel('StageTime/TimeTotal')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()

