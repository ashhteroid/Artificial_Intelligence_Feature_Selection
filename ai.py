import math
import random


dataset=[]
normdataset=[]

def get_data():
	with open("/Users/Ashwin/Downloads/cs_170_smallALL/cs_170_small46.txt") as input_file:
	# with open("/Users/Ashwin/Downloads/cs_170_largeALL/cs_170_large46.txt") as input_file:
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
		#print i
		if i==0:
			mean.append(0)
			continue
		temp_sum=0
		for j in range(len(dataset)):
		#	print j		
			temp_sum+=dataset[j][i]
		mean.append(temp_sum/len(dataset))
		#print mean

	for i in range(len(dataset[0])):
		if i==0:
			sd.append(0)
			continue
		temp_sum=0
		for j in range(len(dataset)):
			temp_sum+=math.pow(dataset[j][i]-mean[i],2)
		
		sd.append(math.sqrt(temp_sum/len(dataset)))
	# print sd

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
	for i in range(len(record1)):
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
	for i in range(len(norm[0])):
		if i==0:
			temp_fset.append(True)
		temp_fset.append(False)
	for j in range(len(norm[0])):
		if j==0:
			continue
		inner_accu=0
		inner_index=0
		print "Level:"+str(j)
		for k in range(len(norm[0])):
			if k==0:
				continue
			if(not temp_fset[k]):
				temp_fset[k]=True
				lol=loocv(norm,temp_fset)
				if(lol>inner_accu):
					inner_accu=lol
					inner_index=k
					print "inner Ac:"+str(inner_accu)+" and index:"+str(inner_index)
				temp_fset[k]=False

		temp_fset[inner_index]=True
		temp_fselected.append(inner_index)
		if(accuracy<inner_accu):
			accuracy=inner_accu
			max_index=inner_index
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

	for i in range(len(norm[0])):
		if i==0:
			temp_fset.append(False)
		temp_fset.append(True)
		temp_fselected.append(i)
		fselected.append(i)
	for j in range(len(norm[0])):
		if j==0:
			fselected.remove(0)
			temp_fselected.remove(0)
			continue
		inner_accu=0
		inner_index=0
		print "Level:"+str(j)
		for k in range(len(norm[0])):
			if k==0:
				continue
			if(temp_fset[k]):
				temp_fset[k]=False
				lol=loocv(norm,temp_fset)
				print "Examining index:"+str(k)+" Accu:"+str(lol)
				if(lol>inner_accu):
					inner_accu=lol
					inner_index=k
					print "inner Ac:"+str(inner_accu)+" and index:"+str(inner_index)
				temp_fset[k]=True

		temp_fset[inner_index]=False
		print temp_fselected
		temp_fselected.remove(inner_index)
		print temp_fselected
		istack.append(inner_index)

		if(accuracy<inner_accu):
			accuracy=inner_accu
			max_index=inner_index
	
	for l in istack:
		
		if str(l)==str(max_index):
				print "lol"
				break
		fselected.remove(l)
	
	return accuracy, fselected

def forward_selection_subsampling(norm):
	temp_fset=list()
	accuracy=0
	temp_fselected=list()
	fselected=list()
	max_accu=0
	for i in range(len(norm[0])):
		if i==0:
			temp_fset.append(True)
		temp_fset.append(False)
	for j in range(len(norm[0])):
		if j==0:
			continue
		inner_accu=0
		inner_index=0
		print "Level:"+str(j)
		fsample=random.sample(range(1,len(norm[0])),int(math.sqrt(len(norm[0]))))
		for k in fsample:
			if(not temp_fset[k]):
				temp_fset[k]=True
				lol=loocv(norm,temp_fset)
				if(lol>inner_accu):
					inner_accu=lol
					inner_index=k
					print "inner Ac:"+str(inner_accu)+" and index:"+str(inner_index)
				temp_fset[k]=False

		temp_fset[inner_index]=True
		temp_fselected.append(inner_index)
		print temp_fselected
		if(accuracy<inner_accu):
			accuracy=inner_accu
			max_index=inner_index
			print "Max index recorded:"+str(max_index)
	for l in temp_fselected:
		fselected.append(l)
		if l==max_index:
				break
	return accuracy,fselected

dataset=get_data()
normdataset=norm(dataset)
print normdataset

fset=[]
for i in range(len(normdataset[0])):
	if i==0:
		fset.append(False)
	fset.append(True)

print forward_selection(normdataset)
# print backward_selection(normdataset)
print forward_selection_subsampling(normdataset)
