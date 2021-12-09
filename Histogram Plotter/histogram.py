import sys

import json
from matplotlib import pyplot as plt
import numpy as np


from sklearn.preprocessing import PolynomialFeatures
import numpy as np
from sklearn.linear_model import LinearRegression 
from sklearn.metrics import mean_squared_error, r2_score

def PolynomialRegression(X, y, categories = [], deg=2, figsize=7, filename = "", x_name = "", y_name = "", show_regression = True, show_zero = False):

	#print(X.shape, type(X))
	#print(y.shape, type(y))

	
	XY = list(zip(X,y))
	XY.sort(key = lambda x : x[1])
	XY.sort(key = lambda x : x[0])
	X = np.asarray([i[0] for i in XY])
	y = np.asarray([i[1] for i in XY])

	X = X.reshape(-1,1)
	print(X.shape, type(X))

	
	y = y.reshape(-1,1)
	print(y.shape, type(y))


	#print(X)
	

	poly = PolynomialFeatures(degree=deg, include_bias=False)
	X_poly = poly.fit_transform(X)

	# This exactly implements the above formula
	polyReg = LinearRegression().fit(X_poly, y) 

	'''
	# Printing Coefficients
	coef = pd.DataFrame(polyReg.coef_, columns=[f'b{i+1}' for i in range(deg)])
	coef.insert(loc=0, column='b0', value=polyReg.intercept_)
	coef = coef.style.format("{:10,.10f}") # Comment this out to not suppressing the scientific notation
	display(coef)
	'''
	#### Plotting ####
	#plt.figure(figsize=(figsize, figsize))
	test = plt.figure()

	#plt.ylabel('Commits')
	#plt.xlabel('Lifespan')
	
	if categories != [] :
		threshold = 0
		for (i, c) in zip(X, categories) :
			if c == 'Short' :
				if threshold < i :
					threshold = i
		
		XX = []
		Y = []
		for i in list(set(categories)) :
			Y.append([])
			XX.append([])
			
		
		for (i, j) in zip(X, y) :
			if i <= threshold :
				XX[0].append(i)
				Y[0].append(j)
			else :
				XX[1].append(i)
				Y[1].append(j)
		
		labels = list(set(categories))
		colors = ['red', 'blue']
		for c in range(2) :
			plt.scatter(XX[c], Y[c], alpha=.5, label=labels[c], color = colors[c])
		
		plt.xlabel(x_name)
		plt.ylabel(y_name)
		
		test.legend()
				
		'''
		Y = {}
		for i in reverse(list(set(categories))) :
			Y[i] = []
		for (i,c) in zip(y, categories) :
			Y[c].append(i)
		print(Y)
		
		Y = [i for i in Y.values()]
		print(Y)
		'''
		#return None
	else :	
		plt.xlabel(x_name)
		plt.ylabel(y_name)
		
		plt.scatter(X, y, alpha=.5)
	
	if show_regression :
		plt.plot(np.sort(X), polyReg.predict(X_poly), color='tab:green', alpha=1)
	if show_zero :
		plt.plot(X, [0]*len(X), color='black', alpha=.5)
	#plt.plot([[1, 2, 3], [5, 2, 3]])

	plt.figure(figsize=(50,50))
	test.show()

	if filename == "" :
		test.savefig('samplefigure.png')
		#files.download('samplefigure.png')
	else :
		test.savefig(filename)
		#files.download(filename)

#plt.show()

def parse_json(filename, retrieve_info = "") :
	f = open(filename)
	data = json.load(f)
	f.close()
	#print(data)
	
	if retrieve_info == 'lifespan' :
		lifespan = []
		for contributor in data['apache/kafka']['contributors'] :
			#print(contributor)
			metadata = data['apache/kafka']['contributors'][contributor]
			if metadata != {} :
				lifespan.append([contributor, metadata['lifespan'], metadata['category'], metadata['commits']])

		lifespan.sort(key = lambda x : x[3])
		lifespan.sort(key = lambda x : x[1])

		print(np.asarray(lifespan).shape)
		return lifespan
	elif retrieve_info =='ccn' :
		ccn = []
		x = []
		for contributor in data :
			if data[contributor] != [] :
				ccn.append([-(sum(data[contributor])/len(data[contributor])), len(data[contributor])])
				if ccn[-1][1] >= 350 :
					x.append(data[contributor])
		
		ccn.sort(key = lambda x : x[1])
		ccn.sort(key = lambda x : x[0])
		
		return ccn, x

def histogram(data, type_of_histogram, filename = "") :
	if type_of_histogram == 'lifespan' :
		x = list(range(len(data)))
		y = [i[1] for i in data]
		
		test = plt.figure()
		
		plt.xlabel('Contributor List')
		plt.ylabel('Lifespan by Contributor')
		
		plt.bar(x, y, color = ['red'])	
		
		test.show() 
		test.savefig(filename)
		
	elif type_of_histogram == 'commits' :
		x = list(range(len(data)))
		y = [i[3] for i in data]
		
		test = plt.figure()
		
		plt.xlabel('Contributor List')
		plt.ylabel('Number of Commits by Contributor')
		
		plt.bar(x, y, color = ['red'])	 
		
		test.show() 
		test.savefig(filename)
		
	elif type_of_histogram == 'lifespan-commit' :
		x = [i[1] for i in data]
		y = [i[3] for i in data]
		categories = [i[2] for i in data]
		
		PolynomialRegression(x, y, categories, deg = 7, filename=filename, x_name = "Lifespan", y_name = "Number of Commits")
			
	elif type_of_histogram == 'short-long' :
		x = {}
		for i in data :
			if i[2] not in x :
				x[i[2]] = 1
			else :
				x[i[2]] += 1
		
		test = plt.figure()
		
		plt.xlabel('Short-term and Long-term Contributors')
		plt.ylabel('Frequency')
		
		plt.bar(list(x.keys()), list(x.values()))
		
		test.show() 
		test.savefig(filename)
		
		'''
		x = list(range(len(data)))
		y = [i[1] for i in data]
		
		test = plt.figure()
		
		plt.xlabel('Contributor List')
		plt.ylabel('Lifespan by Contributor')
		
		plt.bar(x, y, color = ['red'])	
		
		test.show() 
		test.savefig(filename)
		'''
	
	elif type_of_histogram == 'ccn' :
		x = [i[1] for i in data]
		y = [i[0] for i in data[::-1]]
		
		PolynomialRegression(x, y, deg = 50, filename = filename, x_name = "Number of Commits", y_name = "Average CCN Improvement", show_regression = False, show_zero = True)
	
	elif type_of_histogram == 'ccn_variability' :
		x = [i[1] for i in data]
		y = [i[0] for i in data[::-1]]
		
		xy = {}
		for i,val in enumerate(x) :
			if val not in xy :
				xy[val] = [y[i]]
			else :
				xy[val].append(y[i])
		
		xy = list(xy.items())
		xy.sort(key = lambda x : x[0])
		
		x = [i[0] for i in xy]
		y_mean = [sum(i[1])/len(i[1]) for i in xy]
		y_variance = [sum([(j - y_mean[i])**2 for j in xy[i][1]])/len(xy[i][1]) for i in range(len(xy))]
		
		PolynomialRegression(x, y_variance, deg = 50, filename = 'variability_in_' + filename, x_name = "Number of Commits", y_name = "Variability in CCN Improvement", show_regression = False, show_zero = True)
	#fig, axs = plt.subplots(1, 1,
		                #figsize =(10, 7),
		                #tight_layout = True)

	#axs.hist(y, bins = len(x))
	
	# Show plot
	




'''
lifespan = parse_json("/home/bharath/Downloads/kafka.json", 'lifespan')
for l in lifespan :
	print(l)
	
print(len(lifespan))

#histogram(lifespan, 'lifespan')
#histogram(lifespan, 'commits')
histogram(lifespan, 'lifespan-commit')
'''

'''
filenames = ['kafka', 'iceberg', 'parquet-cpp']

filename = filenames[1]

#ccn, x = parse_json("/home/bharath/ECS260/kafka.json", 'ccn')
#print(ccn)

ccn, x = parse_json("/home/bharath/ECS260/" + filename + ".json", 'ccn')
#print(ccn)

#ccn, x = parse_json("/home/bharath/ECS260/kafka.json", 'ccn')
#print(ccn)

print(x)
print(len(x))

x.sort(key = lambda x : len(x), reverse = True)

x = [-(sum(i)/len(i)) for i in x]
print(x)

print(len(ccn))
#print([i for i in ccn if i[1] > 100])
#ccn = [i for i in ccn if i[0] >= -0.05 and i[0] <= 0.05]

print(len(ccn))
histogram(ccn, 'ccn_variability', filename + '_ccn.png')
print(len(ccn))
'''

if len(sys.argv) > 1 :

	args = sys.argv[1:]

	inputfile = args[0]
	graphplot = args[1]
	#graphfile = args[2]
	
	
	input_directory = './JSON/'
	output_directory = './Graphs/'
	
	if graphplot == 'ccn' or graphplot == 'ccn_variability' :
		data, _ = parse_json(input_directory + inputfile + '.json', 'ccn')
	elif graphplot == 'lifespan' or graphplot == 'commits' or graphplot == 'lifespan-commit' or graphplot == 'short-long' :
		data = parse_json(input_directory + inputfile + '.json', 'lifespan')
	histogram(data, graphplot, output_directory + inputfile + '_' + graphplot + '.png')

