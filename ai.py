import math


dataset=[]
normdataset=[]

def get_data():
	with open("/Users/Ashwin/Downloads/cs_170_smallALL/cs_170_small9.txt") as input_file:
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









dataset=get_data()
normdataset=norm(dataset)
print normdataset