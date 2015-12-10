import math


dataset=[]
normdataset=[]

def get_data():
	with open("/Users/Ashwin/Downloads/cs_170_smallALL/cs_170_small42.txt") as input_file:
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
	temp_fset=[]
	accuracy=0
	fselected=[]
	for i in range(len(norm[0])):
		if i==0:
			temp_fset.append(True)
		temp_fset.append(False)
	for j in range(len(norm[0])):
		if j==0:
			continue
		inner_accu=0
		inner_index=0
		for k in range(len(norm[0])):
			if k==0:
				continue
			if(not temp_fset[k]):
				temp_fset[k]=True
				lol=loocv(norm,temp_fset)
				if(lol>inner_accu):
					inner_accu=lol
					inner_index=k
				temp_fset[k]=False


		if(accuracy<inner_accu):
			accuracy=inner_accu
			fselected.append(inner_index)
			temp_fset[inner_index]=True
		else:
			break
	return accuracy, fselected



dataset=get_data()
normdataset=norm(dataset)
print normdataset

fset=[]
for i in range(len(normdataset[0])):
	if i==0:
		fset.append(False)
	fset.append(True)

print forward_selection(normdataset)

