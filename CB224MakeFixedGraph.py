import time
from datetime import datetime as dt
import pickle
from collections import defaultdict

# TODO: we need to add the following 4 files to the directory, + intNodeIDs10.txt (or intNodeIDs11.txt)
# and describe what each file contains
companyEmployees = open('company-employee-date.txt', 'r')
companyInvestors = open('company-investor-date.txt', 'r')
# TODO: the below 4 files use version 10, when our directory contains version 11. Should we update this?
empEdges = open('CB224/company-emp-graph10.txt', 'w+')
invEdges = open('CB224/company-inv-graph10.txt', 'w+')
nodeIDs = open('CB224/nodeIDs10.txt', 'w+')
intNodeIDs = open('CB224/intNodeIDs10.txt', 'w+')
# TODO: Do we need to retain the below 2 lines? What do these files contain? Should we add these files to directory?
#CEIDs = open('CB224/c-e-IDs.txt', 'w+')
#CIIDs = open('CB224/c-i-IDs.txt', 'w+')


# TODO: What does the below function do?
def dd():
	return False

# The below code generates IDs for each node
# and creates a dictionary of nodes, employment dates, investment dates, and dates (CORRECT?)
# Any ID less than 100,000 is a company node
# Any ID between 100,000 and 200,000 is an employee node
# Any ID greater than 200,000 is an investor node
companyNodeID = 0
employeeNodeID = 100000
investorNodeID = 200000
count = 0
bigCount = 0
nodeDict = dict()
empDateDict = dict()
invDateDict = dict()
dateDict = dict()
companies = set()
employees = set()
investors = set()
nodeDict = defaultdict(dd, nodeDict)
empDateDict = defaultdict(dd, empDateDict)
invDateDict = defaultdict(dd, invDateDict)
dateDict = defaultdict(dd, dateDict)

# The below populates the dictionaries created above (CORRECT?)
compEmp = companyEmployees.readline()
while(compEmp != ''): #as long as we haven't reached the end of the file
	nsd = compEmp.split('\t') #nsd[0] = company string, nsd[1] = employee string
	if not nodeDict[nsd[0]]: #if we haven't already seen this company
		nodeDict[nsd[0]] = companyNodeID #put in as company string key, id value
		companies.add(nsd[0]) #add company to set of companies
		currComp = companyNodeID #save for later use
		companyNodeID += 1
	if not nodeDict[nsd[1]]: #if we haven't already seen this employee, etc.
		nodeDict[nsd[1]] = employeeNodeID
		employees.add(nsd[1])
		currEmp = employeeNodeID
		employeeNodeID += 1
	date = nsd[2].strip()
	datet = dt.strptime(date, '%Y-%m-%d')
	if not invDateDict[(currComp,currEmp)]: 
		invDateDict[(currComp,currEmp)] = [date]
	else:
		invDateDict[(currComp,currEmp)].append(date)
	if not dateDict[(currComp,currEmp)]:
		dateDict[(currComp,currEmp)] = [datet]
		dateDict[(currEmp,currComp)] = [datet]
	else:
		dateDict[(currEmp,currComp)].append(datet)
		dateDict[(currComp,currEmp)].append(datet)
	empEdges.write("{}\t{}\t{}\n".format(currComp, currEmp, empDateDict[(currComp, currEmp)]))
	#pprint "{}\t{}\n".format(nodeDict[nsd[0]], nodeDict[nsd[1]])
	compEmp = companyEmployees.readline()
	count += 1
	if(count >= 500):
		bigCount += count
		print bigCount
		count = 0
	
# TODO: What are these print commands for? Can we delete them?
print "RESET"
print

# The below generates a separate investor and employee ID (node) for people who invest in companies but are also employees of companies (CORRECT?)
bigCount = 0
count = 0
newCompanies = 0
overlap = 0
compInv = companyInvestors.readline()
while(compInv != ''):
	nsd = compInv.split('\t')
	if not nodeDict[nsd[0]]:
		#print "skipping: " + nsd[0]
		compInv = companyInvestors.readline()
		continue
		# print "NEW COMPANY!! " + nsd[0]
		# newCompanies += 1
		# nodeDict[nsd[0]] = nodeID
		# nodeID += 1
	currComp = nodeDict[nsd[0]]
	if (not nodeDict[nsd[1]]): #if we haven't seen this string before
		nodeDict[nsd[1]] = investorNodeID
		investors.add(nsd[1])
		currInv = investorNodeID
		investorNodeID += 1
	elif (nsd[1] in employees) and (nsd[1] not in investors): #if we have seen this string before, and they're an employee but not yet an investor
		overlap += 1
		idList = list()
		idList.append(nodeDict[nsd[1]]) #get their odl value and make it into a list
		idList.append(currInv) #append the new value
		nodeDict[nsd[1]] = idList 
		investors.add(nsd[1])
		currInv = investorNodeID
		investorNodeID += 1
	
	datet = dt.strptime(nsd[2].strip(), '%m/%d/%y')
	date = datet.strftime('%Y-%m-%d')
	if not invDateDict[(currComp,currInv)]:
		invDateDict[(currComp,currInv)] = [date]
	else:
		invDateDict[(currComp,currInv)].append(date)
	if not dateDict[(currComp,currInv)]:
		dateDict[(currComp,currInv)] = [datet]
		dateDict[(currInv,currComp)] = [datet]
	else:
		dateDict[(currInv,currComp)].append(datet)
		dateDict[(currComp,currInv)].append(datet)
	invEdges.write("{}\t{}\t{}\n".format(currComp, currInv, invDateDict[(currComp, currInv)]))
	compInv = companyInvestors.readline()
	count += 1
	if(count >= 500):
		bigCount += count
		print bigCount
		count = 0

# TODO: Any reason to keep the below code? Is it in the correct position (i.e. why does it appear before the pickle.dump functions?)	
# invDateDict = pickle.load(open("invDateDict4.p", "rb"))
# empDateDict = pickle.load(open("empDateDict4.p", "rb"))
# nodeDict = pickle.load(open("nodeDict4.p", "rb"))

# TODO: How is the below code different from lines 86-135? What are these separate sections doing?
# The below code makes a map from the node ID to the company/person name, 
# taking into account the case where a person is
# both an investor and an employee
intDict = dict()
for key in nodeDict.keys():
	if type(nodeDict[key]) is not list:
		intDict[nodeDict[key]] = key
	else: # this name maps to a list of IDs (investor and employee)
		nodesList = nodeDict[key]
		print nodesList
		for nodeId in nodesList:
			print nodeId
			intDict[nodeId] = key
	#nodeIDs.write("{}\t{}\n".format(nodeDict[key], key))
for key in intDict:
	intNodeIDs.write("{}\t{}\n".format(key, intDict[key]))

# The below code "pickles" (i.e. compresses) the generated dictionaries for ease of reference
pickle.dump(invDateDict, open("invDateDict4.p", "wb"))
pickle.dump(empDateDict, open("empDateDict4.p", "wb"))
pickle.dump(nodeDict, open("nodeDict4.p", "wb"))
pickle.dump(intDict, open("intDict4.p", "wb"))
pickle.dump(dateDict, open("dtDateDict4.p", "wb"))

# TODO: What does the following print out?
print "companies", len(companies)
print "employees", len(employees)
print "investors", len(investors)
print "overlap", overlap

# TODO: Do we need to retain any of the below commented out code?

#each line, take first entry and check if it's in map, take second entry and check if it's map
#put whatever is not in the map in the map
#get value for whatever is in the map
#write to file with map value and tab separated list




#company, investor, employee nodes


# companies = open('companies.txt', 'r')
# investors = open('investors.txt', 'r')
# dates = open('full-date.txt', 'r')
# ctoi = open('company-investor.txt', 'w+')

# company = companies.readline()
# investor = investors.readline()
# date = dates.readline()
# while(company != '' and investor != ''):
# 	ctoi.write(company.strip() + '\t' + investor.strip() + '\t' + date.strip() + '\n')
# 	company = companies.readline()
# 	investor = investors.readline()
# 	date = dates.readline()

#dates = open('full-date.txt', 'r')


# dateOutput = open('dates.txt', 'a+')

# fakeDay = 15

# date = dates.readline().strip()
# dateList = date.split('-')
# dateOutput.write("{}-{}-{}".format(dateList[0], dateList[1], fakeDay))
#time.strptime(date, )