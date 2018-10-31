import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
from collections import Counter
from matplotlib import rcParams

#Plots Specifications
size=12
params = {'font.family': 'serif',
	'font.serif': 'Times',
	'legend.fontsize': size-2,
         'figure.figsize': (10,5),
         'axes.labelsize': size,
	'axes.titleweight':'bold',
         'axes.titlesize':size+2,
         'xtick.labelsize':size,
         'ytick.labelsize':size}
plt.rcParams.update(params)

#User imputs
#name=sys.argv[1]
name=sys.argv[1].split(',')
print name
#library
n_plots=sys.argv[2]
inplace=sys.argv[3]
complex_=sys.argv[4]
precision=sys.argv[5]
dim=sys.argv[6]
kind=sys.argv[7]
X=sys.argv[8]
Y=sys.argv[9]


#Assign to a numpy array the data
def extractdata (name):
	data=np.genfromtxt(name, delimiter=',', invalid_raise=False, names=True, skip_header=3, dtype="|S20,|S20,|S20,|S20,f4,|S20,f4,f4,f4,f4,f4,|S20,f4,f4,f4,f4,f4,f4,f4,f4,f4,f4,f4,f4,f4,f4")
	return data


#Select the test parameters to plot
def filter_testparameters(data, inplace, complex_,precision,kind):
	Inplace_data=data[(data['inplace']==inplace)]
	#print data['inplace']==inplace
	Complex_data= Inplace_data[(Inplace_data['complex']==complex_)] 
	Precision_data=Complex_data[(Complex_data['precision']==precision)]
	Kind_data=Precision_data[(Precision_data['kind']==kind)]
	return Kind_data

#Select XY from the selected test
def filter_XY(x, Kind_data,Y):
	a=np.sort([item for item, count in Counter(x).iteritems() if count > 1])
	y=[0]*len(a)
	for i in range(len(a)): 
		y[i]=(Kind_data[Y][Kind_data[X]==a[i]]).mean()
	y=np.asarray(y)
	return a,y

#Distribution of stages in Total for a single input
def distributionofstages (possible_Times, y, signalsize, Selected_data):
	y_times=np.empty((len(y),1))
	x_nx=np.empty((len(signalsize),1))
	for i in range(len(possible_Times)):
		sx,sy=filter_XY(size, Selected_data, possible_Times[i])
		x_nx=np.column_stack((x_nx,sx))
		y_times=np.column_stack((y_times,sy))

	total_time=y_times[:,-1]
	x_nx=x_nx[:,1:(x_nx.shape[1])]
	y_ctimes=y_times[:,1:(y_times.shape[1])-1]
	y_ctimes=[sum(y_ctimes[i]) for i in range(len(y_ctimes))]
	#print y_times.shape
	dif_times=total_time-y_ctimes
	plt.figure()
	#ax1=fig.add_subplot(211)
	#ax1.plot(x_nx[:,0], y_ctimes, 'r*-', label='Sum time of stages')
	plt.plot(x_nx[:,8],dif_times,'bo-')
	plt.title('Difference betweem Sum of time from stages and Total Time')
	plt.xscale('log', basex=2)
	plt.xlabel('# of Elements')
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
	#plt.title('Percentage of each stage on Total Time')
	#plt.ylim((0,1))
	plt.xlim(2, 2**24) 
	plt.xscale('log', basex=2)
	plt.xlabel('# of Elements')
	plt.ylabel('StageTime/TimeTotal')
	plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1),
          ncol=4, fancybox=True)
	#plt.show()


#Distribution of stages in Total for a single input
def Histogramstages (possible_Times, y, signalsize, Selected_data):
        y_times=np.empty((len(y),1))
	x_nx=np.empty((len(signalsize),1))
        for i in range(len(possible_Times)):
		sx,sy=filter_XY(size, Selected_data, possible_Times[i])
                x_nx=np.column_stack((x_nx,sx))
                y_times=np.column_stack((y_times,sy))

        total_time=y_times[:,-1]
        x_nx=x_nx[:,1:(x_nx.shape[1])]
        y_ctimes=y_times[:,1:(y_times.shape[1])-1]
	y_times_mean=y_ctimes.mean(axis=0)
	y_times_mean=y_times_mean[0:(y_times.shape[1])-1]
        y_times_std=y_ctimes.std(axis=0)
	y_times_std=y_times_std[0:(y_times.shape[1])-1]
	stages = np.array([0,1,2,3,4,5,6,7])
	name_stages =['Allocate', 'PlanF', 'Upload','ExeFor','PlanB', 'ExeB', 'Download', 'Destroy'] 
	plt.figure()
	plt.xticks(stages, name_stages)
	#Plot
	plt.errorbar(stages,y_times_mean, y_times_std, linestyle='None', marker='o', markerfacecolor='r')
        plt.xlim(-1,8)
	plt.xlabel('Stages')
	plt.ylabel('Time [ms]')
      	plt.suptitle('Distribution of each stage for V100', size=14)
	plt.title(" Precision: " + precision + " Memory Mode: " + inplace + " Complexity: " + complex_ + " Dimension: " + dim + " Kind: "+ kind, size=10) 
	plt.show()

#HOW TO RUN "DISTRIBUTION" OF STAGES AND MEAN/STD distribution per stage. 
#data=extractdata(name)
#possible_Times=data.dtype.names[12:21]
#Selected_data=filter_testparameters(data,inplace,complex_,precision,kind)
#size=Selected_data[X]
#signalsize, y =filter_XY(size,Selected_data,Y)
#distributionofstages(possible_Times, y, signalsize, Selected_data)
#Histogramstages(possible_Times, y, signalsize, Selected_data)

##Plot Speed up multiple inputs
def speedup (name, inplace, complex_,precision,kind):
	plt.figure()
	for i in range(len(name)):
		if i==0:
			print name[i]
			data=extractdata(name[i])
			possible_Times=data.dtype.names[11:21]
			Selected_data=filter_testparameters(data,inplace,complex_,precision,kind)
			size=Selected_data[X]
			signalsize,y1 =filter_XY(size,Selected_data,Y)
			plt.xlim(1*8/1e6, (2**30)*8/1e6)
			plt.xscale('log', basex=2)
			#plt.yscale('log', basey=10)
			if precision == '"double"':
				plt.plot(signalsize*8/1e6, y1/y1, 'o-', label=(name[i].split('/'))[-1])
			else:
				plt.plot(signalsize*4/1e6, y1/y1, 'o-', label=(name[i].split('/'))[-1])
		else:
        	        data=extractdata(name[i])
        	        possible_Times=data.dtype.names[11:21]
        	        Selected_data=filter_testparameters(data,inplace,complex_,precision,kind)
        	        size=Selected_data[X]
        	        signalsize,y =filter_XY(size,Selected_data,Y)
			#plt.plot(signalsize, y, 'o-')
        	        plt.xlim(1*8/1e6, (2**30)*8/1e6)
        	        plt.xscale('log', basex=2)
        	        #plt.yscale('log', basey=10)
        	        if precision == '"double"':
        	                plt.plot(signalsize*8/1e6, y1/y, 'o-', label=(name[i].split('/'))[-1])
        	                print i
        	        else:
        	                plt.plot(signalsize*4/1e6, y1/y, 'o-', label=(name[i].split('/'))[-1])
		plt.legend(loc="best")
		plt.xlabel('Signal Size [MiB]')
		plt.ylabel("Speedup" + Y)
		plt.suptitle ("Speedup for " + Y, fontweight='bold', size=14)
		plt.title(" Precision: " + precision + " Memory Mode: " + inplace + " Complexity: " + complex_ + " Dimension: " + dim + " Kind: "+ kind, size=10) 

speedup(name, inplace, complex_, precision, kind)

##Plot and compare multiple inputs in one stage
def plotstage (name, inplace, complex_,precision,kind):
        plt.figure()
	for i in range(len(name)):
		data=extractdata(name[i])
                possible_Times=data.dtype.names[11:21]
                Selected_data=filter_testparameters(data,inplace,complex_,precision,kind)
                size=Selected_data[X]
                signalsize,y =filter_XY(size,Selected_data,Y)
                #plt.plot(signalsize, y, 'o-')
                plt.xlim(1*8/1e6, (2**30)*8/1e6)
                plt.xscale('log', basex=2)
                plt.yscale('log', basey=10)
                if precision == '"double"':
                	plt.plot(signalsize*8/1e6, y, 'o-', label=(name[i].split('/'))[-1])
               	else:
                	plt.plot(signalsize*4/1e6, y, 'o-', label=(name[i].split('/'))[-1])
	plt.legend(loc="best")
        plt.xlabel('Signal Size [MiB]')
        plt.ylabel(Y)
        plt.suptitle ("Stage" + Y, fontweight='bold', size=14)
        plt.title(" Precision: " + precision + " Memory Mode: " + inplace + " Complexity: " + complex_ + " Dimension: " + dim + " Kind: "+ kind, size=10)

plotstage (name, inplace, complex_, precision, kind)

plt.show()





































