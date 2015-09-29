import time
from datetime import datetime as dt
import pickle
from collections import defaultdict

companyEmployees = open('company-employee-date.txt', 'r')
companyInvestors = open('company-investor-date.txt', 'r')
empEdges = open('CB224/company-emp-graph10.txt', 'w+')
invEdges = open('CB224/company-inv-graph10.txt', 'w+')
nodeIDs = open('CB224/nodeIDs10.txt', 'w+')
intNodeIDs = open('CB224/intNodeIDs10.txt', 'w+')
#CEIDs = open('CB224/c-e-IDs.txt', 'w+')
#CIIDs = open('CB224/c-i-IDs.txt', 'w+')


def dd():
	return False

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
	

print "RESET"
print

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
	

# invDateDict = pickle.load(open("invDateDict4.p", "rb"))
# empDateDict = pickle.load(open("empDateDict4.p", "rb"))
# nodeDict = pickle.load(open("nodeDict4.p", "rb"))

# make a map from the node ID to the company/person name, 
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

pickle.dump(invDateDict, open("invDateDict4.p", "wb"))
pickle.dump(empDateDict, open("empDateDict4.p", "wb"))
pickle.dump(nodeDict, open("nodeDict4.p", "wb"))
pickle.dump(intDict, open("intDict4.p", "wb"))
pickle.dump(dateDict, open("dtDateDict4.p", "wb"))

print "companies", len(companies)
print "employees", len(employees)
print "investors", len(investors)
print "overlap", overlap

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