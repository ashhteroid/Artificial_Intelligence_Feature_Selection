'''  
=================================================================
	@version  2.0
	@author   Ashwin Ramadevanahalli
	@title    Artificial Intelligence- Feature selection.

=================================================================
'''

import math
import time
import random



def get_data(filename):
	with open(filename) as input_file:
		dataset=[]
		for line in input_file:
			line = line.strip()
			record=list()
			for number in line.split():
				record.append(float(number))
			dataset.append(record)
	return dataset

def norm(dataset):
	mean=[]
	sd=[]
	newset=[]

	for i in range(len(dataset[0])):
		if i==0:
			mean.append(0)
			continue
		temp_sum=0
		for j in range(len(dataset)):
			temp_sum+=dataset[j][i]
		mean.append(temp_sum/len(dataset))

	for i in range(len(dataset[0])):
		if i==0:
			sd.append(0)
			continue
		temp_sum=0
		for j in range(len(dataset)):
			temp_sum+=math.pow(dataset[j][i]-mean[i],2)
		
		sd.append(math.sqrt(temp_sum/len(dataset)))

	for i in range(len(dataset)):
		temp=list()
		for j in range(len(dataset[0])):
			if j==0:
				temp.append(dataset[i][j])
			else:
				temp.append((dataset[i][j] - mean[j]) / sd[j])
		newset.append(temp)
	return newset

def euclidean_distance(record1, record2, fset):
	dis = 0
	for i in range(no_features):
		if i==0 or fset[i]==False:
			continue
		else:
			dis += pow((record1[i] - record2[i]), 2)
	return math.sqrt(dis)

def accuracy(norm, predictions):
	correct = 0
	for i in range(len(norm)):
		if norm[i][0] == predictions[i]:
			correct += 1
	return (correct/float(len(norm))) * 100.0

def loocv(norm,fset):
	predictions=list()
	for test in norm:
		mindis=float("inf")
		for train in norm:
			if train==test:
				continue
			dis=euclidean_distance(test,train,fset)
			if(dis<mindis):
				mindis=dis
				prediction=train[0]
		predictions.append(prediction)

	return accuracy(norm,predictions)

def forward_selection(norm):
	temp_fset=list()
	accuracy=0
	temp_fselected=list()
	fselected=list()
	max_accu=0
	flag=False
	for i in range(no_features):
		if i==0:
			temp_fset.append(True)
		temp_fset.append(False)
	for j in range(no_features):
		if j==0:
			continue
		inner_accu=0
		inner_index=0
		for k in range(no_features):
			if k==0:
				continue
			if(not temp_fset[k]):
				temp_fset[k]=True
				lol=loocv(norm,temp_fset)
				if(lol>inner_accu):
					inner_accu=lol
					inner_index=k
				temp_fset[k]=False

		temp_fset[inner_index]=True
		temp_fselected.append(inner_index)

		if(accuracy<inner_accu):
			accuracy=inner_accu
			max_index=inner_index
		else:
			if(flag):
				print "(Warning, Accuracy has not increased! Continuing search in case of local maxima)"
			flag=True
		print "Using feature(s) ",temp_fselected," accuracy is ",inner_accu," %"
	for l in temp_fselected:
		fselected.append(l)
		if l==max_index:
				break

			
		
	return accuracy, fselected

def backward_selection(norm):
	temp_fset=list()
	accuracy=0
	fselected=list()
	temp_fselected=list()
	istack=[]
	flag=False

	for i in range(no_features):
		if i==0:
			temp_fset.append(False)
		temp_fset.append(True)
		temp_fselected.append(i)
		fselected.append(i)
	for j in range(no_features-1):
		if j==0:
			fselected.remove(0)
			temp_fselected.remove(0)
			continue
		inner_accu=0
		inner_index=0
		for k in range(no_features):
			if k==0:
				continue
			if(temp_fset[k]):
				temp_fset[k]=False
				lol=loocv(norm,temp_fset)
				if(lol>inner_accu):
					inner_accu=lol
					inner_index=k
				temp_fset[k]=True

		temp_fset[inner_index]=False
		temp_fselected.remove(inner_index)
		istack.append(inner_index)

		if(accuracy<inner_accu):
			accuracy=inner_accu
			max_index=inner_index
		else:
			if(flag):
				print "(Warning, Accuracy has not increased! Continuing search in case of local maxima)"
			flag=True

		print "Using feature(s) ",temp_fselected," accuracy is ",inner_accu," %"
	
	for l in istack:
		
		if str(l)==str(max_index):
				break
		fselected.remove(l)
	
	return accuracy, fselected

def forward_selection_subsampling(norm):
	temp_fset=list()
	accuracy=0
	temp_fselected=list()
	fselected=list()
	max_accu=0
	flag=False
	for i in range(no_features):
		if i==0:
			temp_fset.append(True)
		temp_fset.append(False)
	for j in range(no_features):
		if j==0:
			continue
		inner_accu=0
		inner_index=0
		no_samples=int(math.sqrt(no_features))
		if no_samples<1:
			no_samples=1
		fsample=random.sample(range(1,no_features),no_samples)
		for k in fsample:
			if(not temp_fset[k]):
				temp_fset[k]=True
				lol=loocv(norm,temp_fset)
				if(lol>inner_accu):
					inner_accu=lol
					inner_index=k
				temp_fset[k]=False

		temp_fset[inner_index]=True
		temp_fselected.append(inner_index)
		if(accuracy<inner_accu):
			accuracy=inner_accu
			max_index=inner_index
		else:
			if(flag):
				print "(Warning, Accuracy has not increased! Continuing search in case of local maxima)"
			flag=True
		print "Using feature(s) ",temp_fselected," accuracy is ",inner_accu," %"
	for l in temp_fselected:
		fselected.append(l)
		if l==max_index:
				break
	return accuracy,fselected

if __name__ == "__main__":
	

	print "\nWelcome to Ashwin Ramadevanahalli's Feature Selection Algorithm.\n"
	filename=raw_input("Type the link of the file to test:")
	option=raw_input("\nChoose the algorithm you want to run.\n\n1.Forward Selection.\n2.Backward Selection.\n3.Ashwin's Special Algorithm.\n4.All the above.\n")
	print "Fetching and Normalizing data,please wait......\n"
	dataset=get_data(filename)
	normdataset=norm(dataset)
	print "\nDone\n"
	no_features=len(normdataset[0])
	no_records=len(normdataset)
	print "The datasethas ",(no_features-1)," features with ",no_records," number of instances."
	fset=[]
	for i in range(len(normdataset[0])):
		if i==0:
			fset.append(False)
		fset.append(True)
	print "Running nearest neighbor with all ",(no_features-1)," features, using 'leaving-one-out' evaluation, I get an accuracy of ",loocv(normdataset,fset)," % \n"
	
	if(option=="1" or option=="4"):
		print "Beginning Forward Selection"
		stime=time.time()
		Accu,sset=forward_selection(normdataset)
		f_time=time.time()-stime
		print "\nFeature set: ",sset," was best with accuracy:",Accu,"%\n"
	if(option=="2" or option=="4"):
		stime=time.time()
		print "Beginning Backward Selection"
		Accu,sset=backward_selection(normdataset)
		b_time=time.time()-stime
		print "\nFeature set: ",sset," was best with accuracy:",Accu,"%\n"
	if(option=="3" or option=="4"):
		stime=time.time()
		print "Beginning Ashwin's Special Selection Algorithm."
		Accu,sset=forward_selection_subsampling(normdataset)
		a_time=time.time()-stime
		print "\nFeature set: ",sset," was best with accuracy:",Accu,"%\n"
	
	if(option=="1" or option=="4"):
		print ("\nTime required for forward selection: %s\n" %f_time)
	if(option=="2" or option=="4"):
		print ("\nTime required for backward selection: %s\n" %b_time)
	if(option=="3" or option=="4"):
		print ("\nTime required for Ashwin selection: %s\n" %a_time)
	print "\n\nThank you.\n\n"



