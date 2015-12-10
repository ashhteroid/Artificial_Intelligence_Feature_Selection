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









dataset=get_data()
normdataset=norm(dataset)
print normdataset