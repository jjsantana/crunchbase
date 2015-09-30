import time
from datetime import datetime as dt
import pickle
from collections import defaultdict
import snap
from datetime import datetime as dt

# TODO: What is difference between this file and CB224MakeFixedGraph.py?

companyEmployees = open('company-employee-date.txt', 'r')
companyInvestors = open('company-investor-date.txt', 'r')
# empEdges = open('CB224/company-emp-graph11.txt', 'w+') 
# invEdges = open('CB224/company-inv-graph11.txt', 'w+')
# allEdges = open('allEdges.txt', 'w+')
# nodeIDs = open('CB224/nodeIDs11.txt', 'w+')
#CEIDs = open('CB224/c-e-IDs.txt', 'w+')
#CIIDs = open('CB224/c-i-IDs.txt', 'w+')

def dd():
	return False

# The following creates a node for each company based on its ID
def addCompanyNode(companyName, companyNodeID):
	if not nodeDict[companyName]:
		nodeDict[companyName] = companyNodeID
		intDict[companyNodeID] = companyName
		companies.add(companyName)
		companyNodeID += 1
	return companyNodeID

# The following creates a node for each employee based on its ID
def addEmployeeNode(employeeName, employeeNodeID):
	if not nodeDict[employeeName]:
		nodeDict[employeeName] = employeeNodeID
		intDict[employeeNodeID] = employeeName
		employees.add(employeeName)
		employeeNodeID += 1
	return employeeNodeID

# The following creates a node for each investor based on its ID
def addInvestorNode(investorName, overlap, investorNodeID):
	if not nodeDict[investorName]:
		nodeDict[investorName] = investorNodeID
		intDict[investorNodeID] = investorName
		investors.add(investorName)
		investorNodeID += 1
	# if we've seen this person before as an employee, make sure
	# to add a second ID as an investor
	# TODO: This seems repetitive of the CB224MakeFixedGraph.py file. Which file was used to generate analyzed graph?
	elif investorName in employees and investorName not in investors:
		overlap += 1
		idList = list()
		idList.append(nodeDict[investorName]) #get their old value and make it into a list
		idList.append(investorNodeID) #append the new value
		nodeDict[investorName] = idList
		intDict[investorNodeID] = investorName
		investors.add(investorName)
		investorNodeID += 1
	return overlap, investorNodeID

# The following appends the end date (TODO: or start date?) to each employment relationship
def addEDate(companyName, employeeName, date):
	cId = nodeDict[companyName]
	eId = nodeDict[employeeName]
	dtDate = dt.strptime(date.strip(), '%Y-%m-%d')
	if not dateDict[(cId, eId)]:
		dateDict[(cId, eId)] = [date.strip()]
		dtDateDict[(eId, cId)] = [dtDate]
	else:
		dateDict[(cId, eId)].append(date.strip())
		dtDateDict[(eId, cId)].append(dtDate)
	return cId, eId

# The following appends the end date (TODO: or start date?) to each investment relationship
def addIDate(companyName, investorName, date):
	cId = nodeDict[companyName]
	iId = nodeDict[investorName]
	if type(iId) is list:
		iId = iId[1]
		print iId
	updatedDate = dt.strptime(date.strip(), '%m/%d/%y').strftime('%Y-%m-%d')
	dtUpdatedDate = dt.strptime(updatedDate, '%Y-%m-%d')
	if not dateDict[(cId, iId)]:
		dateDict[(cId,iId)] = [updatedDate]
		dtDateDict[(iId,cId)] = [dtUpdatedDate]
	else:
		dateDict[(cId,iId)].append(updatedDate)
		dtDateDict[(iId,cId)].append(dtUpdatedDate)
	return cId, iId, updatedDate

# The following generates an (date-weighted?) edge between companies and investors
def addIEdge(companyName, investorName, date):
	cId, iId, updatedDate = addIDate(companyName, investorName, date)
	# invEdges.write("{}\t{}\t{}\n".format(cId, iId, dateDict[(cId,iId)]))
	# allEdges.write("{}\t{}\t{}\n".format(cId, iId, dateDict[(cId,iId)]))

# The following generates an (date-weight?) edge between companies and employees
def addEEdge(companyName, employeeName, date):
	cId, eId = addEDate(companyName, employeeName, date)
	# empEdges.write("{}\t{}\t{}\n".format(cId, eId, dateDict[(cId, eId)]))
	# allEdges.write("{}\t{}\t{}\n".format(cId, eId, dateDict[(cId, eId)]))

# TODO: Below is also in CB224MakeFixedGraph.py file
#Assigning the numbered id's to the companies, employees, and investors
companyNodeID = 0
employeeNodeID = 100000
investorNodeID = 200000
count = 0
bigCount = 0
nodeDict = dict()
nodeDict = defaultdict(dd, nodeDict)
dateDict = dict()
dateDict = defaultdict(dd, dateDict)
dtDateDict = dict()
dateDict = defaultdict(dd, dtDateDict)
intDict = dict()
employees = set()
investors = set()
companies = set()
compEmp = companyEmployees.readline()
while(compEmp != ''):
	#nsd = [name of company, name of employee, date]
	nsd = compEmp.split('\t')
	companyNodeID = addCompanyNode(nsd[0], companyNodeID)
	employeeNodeID = addEmployeeNode(nsd[1], employeeNodeID)
	addEEdge(nsd[0], nsd[1], nsd[2])
	#pprint "{}\t{}\n".format(nodeDict[nsd[0]], nodeDict[nsd[1]])
	compEmp = companyEmployees.readline()
	count += 1
	if(count >= 500):
		bigCount += count
		print bigCount
		count = 0
	

print "RESET"
print

overlap = 0
bigCount = 0
count = 0
newCompanies = 0
compInv = companyInvestors.readline()
while(compInv != ''):
	#nsd = [name of company, name of investor, date]
	nsd = compInv.split('\t')
	if not nodeDict[nsd[0]]:
		compInv = companyInvestors.readline()
		continue
	# passing in overlap because trying to count how many employees we have who are
	# also investors
	overlap, investorNodeID = addInvestorNode(nsd[1], overlap, investorNodeID)
	addIEdge(nsd[0], nsd[1], nsd[2])
	#print "{}\t{}\t{}\n".format(nodeDict[nsd[0]], nodeDict[nsd[1]], invDateDict[(nsd[0],nsd[1])])
	compInv = companyInvestors.readline()
	count += 1
	if(count >= 500):
		bigCount += count
		print bigCount
		count = 0
	

#print "new companies: {}".format(newCompanies)
# for key in nodeDict.keys():
# 	nodeIDs.write("{}\t{}\n".format(nodeDict[key], key))

# pickle.dump(nodeDict, open("nodeDict5.p", "wb"))
# pickle.dump(intDict, open("intDict5.p", "wb"))
# pickle.dump(dateDict, open("dateDict5.p", "wb"))
# pickle.dump(dtDateDict, open("dtDateDict5.p", "wb"))

print "companies", len(companies)
print "employees", len(employees)
print "investors", len(investors)
print "overlap", overlap

# The following prints out the edgelist and nodelist of the given graph,
# either the entire graph (graph), the employment graph (empGraph), or
# the investment graph (invGraph); see lines 196-198
def printEdgesNodes(graph):
	print "Edges: ", graph.GetEdges()
	print "Nodes: ", graph.GetNodes()

# The following writes the edgelist to the file allEdges.txt
graph = snap.LoadEdgeList(snap.PUNGraph, "allEdges.txt", 1,0)

# TODO: Can we remove this commented out code?
# graph = snap.LoadEdgeList(snap.PUNGraph, "company-emp-inv-graph.txt", 1, 0)
# print graph.GetEdges()

# The following writes the employment edgelist to CB224/company-emp-graph11.txt and
# the investment edgelist to CB224/company-inv-graph11.txt
empGraph = snap.LoadEdgeList(snap.PUNGraph, "CB224/company-emp-graph11.txt", 1, 0)
invGraph = snap.LoadEdgeList(snap.PUNGraph, "CB224/company-inv-graph11.txt", 1, 0)

printEdgesNodes(graph)
printEdgesNodes(empGraph)
printEdgesNodes(invGraph)


# The following returns the average degree in the given graph
# TODO: Is there not a single SNAP function for average degree? Why the long function definition?
def printDegrees(Graph):
  avg = 0
  degMap = dict()
  degMap = defaultdict(lambda: 0, degMap)
  result_degree = snap.TIntV()
  snap.GetDegSeqV(Graph, result_degree)
  total = result_degree.Len()
  for i in range(0, result_degree.Len()):
    if result_degree[i] > 1: 
      degMap[result_degree[i]]+=1
      avg += result_degree[i]
    else:
      total -= 1
  for key in degMap:
    print key, degMap[key]
  print (avg*1.0)/(total*1.0)
  print total

print "employee:"
printDegrees(empGraph)
print "investor:"
printDegrees(invGraph)

# TODO: Can we remove following commented out code?
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