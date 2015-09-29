from numpy import *
import operator
import time
import snap
import pickle
import matplotlib.pyplot as plt
import pylab as P

def dd():
	return False

def plotStarDist(text, xlabel, ylabel, data) :
	x = [data[key] for key in data]
	n, bins, patches = P.hist(x, 10, normed=0, histtype='stepfilled')
        P.xlabel(xlabel)
        P.ylabel(ylabel)
        P.setp(patches, 'facecolor', 'g', 'alpha', 0.75)
        P.title(text)
        P.show()

def calcStarDist(threshold, pover):
	starFollows = {}
	for x in pover:
		bFollows = True
		if len(pover[x]) > 1 or len(pover[x]) == 1:
			for tmp in pover[x]:
				if (tmp < threshold):
					bFollows = False
					break
			if (bFollows == True):
				starFollows[x] = len(pover[x])
	return starFollows

def plotDistEmpInvMatches(text, data, yaxis, name):
	fig = plt.figure()
	x = sorted([key for key  in data])
	y = getYs(data)
	plt.title(text)
	plt.xlabel('Threshold')
	plt.ylabel(yaxis)
	plt.plot(x,y, 'go')
	plt.savefig(name)

def MLEApprox(data):
	bigHonkingTerm = 0
	xmin = .11
	for item in data:
		bigHonkingTerm += math.log(data[item]/xmin)
	bigHonkingTerm = 1 + (len(data.values()))/bigHonkingTerm
	print bigHonkingTerm

def getYs(m):
	ys = list()
	sortedKeys = sorted(m.keys())
	for k in sortedKeys:
		ys.append(m[k])
		print k,m[k]
	return ys

def plotWholeGraphStats(title, yaxis, qw, sw, name):
	fig = plt.figure()
	x = sorted([key for key in qw])
	qwy = getYs(qw)
	swy = getYs(sw)
	plt.plot(x, qwy, "c.-", label="q/|I|")
	plt.plot(x, swy, "m.-", label="s/|E|")
	plt.ylabel(yaxis)
	plt.xlabel("Threshold")
	plt.title(title)
	plt.legend()
	plt.savefig(name)
	# plt.show()

def plotReducedGraphStats(title, yaxis, q, s, qj, sj, name):
	fig = plt.figure()
	x = sorted([key for key in q])
	qy = getYs(q)
	sy = getYs(s)
	qjy = getYs(qj)
	sjy = getYs(sj)
	plt.plot(x, qy, "r.-", label="q/|I'|")
	plt.plot(x, sy, "b.-", label="s/|E'|")
	plt.plot(x, qjy, "g.-", label="Jaccard/|I'|")
	plt.plot(x, sjy, "y.-", label="Jaccard/|E'|")
	plt.ylabel(yaxis)
	plt.xlabel("Threshold")
	plt.title(title)
	plt.legend()
	plt.savefig(name)
	# plt.show()


def plotDistEmpInvMatcheslog(text, data, yaxis, name):
        fig = plt.figure()
        x = [key for key  in data]
        y = [data[k] for k in data]
        plt.title(text)
        plt.xlabel('Threshold')
        plt.ylabel(yaxis)
        plt.loglog(x,y, 'ro', basex=10, basey=10)
        plt.savefig(name)
        # plt.show()


def plotDistMatches(text, xlabel, ylabel, data, name):
        fig = plt.figure()
        x = []
        for key in data:
        	x.append(data[key])
        n, bins, patches = P.hist(x, 10, normed=1, histtype='stepfilled')
	#, histtype='step')
	P.xlabel(xlabel)
        P.ylabel(ylabel)
        P.setp(patches, 'facecolor', 'g', 'alpha', 0.75)
        P.title(text)
        plt.savefig(name)
        # P.show()

def plotDist(text, xlabel, ylabel,data, name):
        fig = plt.figure()
        x = []
        for key in data:
                for tmp in data[key]:
                        x.append(tmp)
	n, bins, patches = P.hist(x, 10, normed=0, histtype='stepfilled')
	P.xlabel(xlabel)
	P.ylabel(ylabel)
	P.setp(patches, 'facecolor', 'g', 'alpha', 0.75)
	P.title(text)
	# plt.show()
	plt.savefig(name)

def calcQsSs(nI, nE) :
	#print "ni %d ne %d" %(nI, nE)
	curThres = 0.1
	qI = {}
	sE = {}
	qjI = {}
	sjE = {}
	qwI = {}
	swE = {}

	print  "threshold	q		s		qj		sj		qw		sw"

	while (curThres <= 1.0) :
		sizeE = len(povermMap)
		sizeI = len(poverkMap)

		swE[curThres] = calcQS(curThres, nE, povermMap)
       		sE[curThres]  = calcQS(curThres, sizeE, povermMap)
		sjE[curThres] = calcQS(curThres, sizeE, jacEMap)

       		qwI[curThres]  = calcQS(curThres, nI, poverkMap)
		qI[curThres] = calcQS(curThres, sizeI, poverkMap)
		qjI[curThres] = calcQS(curThres, sizeI, jacIMap)

        	print "%f	%f	%f	%f	%f	%f	%f" %(curThres, qI[curThres], sE[curThres], qjI[curThres], sjE[curThres], qwI[curThres], swE[curThres])
       		curThres += 0.1
	return qI, sE, qjI, sjE, qwI, swE

def calcHigh(str, pover) :
        curThres = 0.1
        ThresholdCnt = {}
        while(curThres <= 1.0):
                ThresholdCnt[curThres] = calcHighs(pover, curThres, False, str)
                curThres += 0.01
        return ThresholdCnt

def calcEmpHigh() :
	curThres = 0.1
	EmpThresholdCnt = {}
	while(curThres <= 1.0):
		EmpThresholdCnt[curThres] = calcEmpHighs(curThres, False)
		curThres += 0.01
	return EmpThresholdCnt

def calcFrequencies(pover, threshold):
	count = 0
	for x in pover:
		for t in pover[x]:
			if (t >= threshold):
				count += 1
	return count
			

def calcQS(threshold, n, inMap):
        cntX = {}
        for x in inMap:
                count = 0
                for tmp in inMap[x] :
                        if (tmp >= threshold):
                                count += 1
                if (count > 0):
                        cntX[x] = count
        return (1.0*len(cntX)/(n*1.0))

def calcq(threshold, n):
        cntI = {}
        for i in poverkMap:
                count = 0
                for tmp in poverkMap[i]:
                        if( tmp >= threshold):
                                count+= 1
                if (count > 0):
                        cntI[i] = count
        return (1.0*len(cntI)/(1.0*n))

def calcHighs(poverMap, threshold, all, str):

        #print "High Employees for %f" % threshold
        cntX = {}
        for x in poverMap:
                count = 0
                for tmp in poverMap[x] :
                        if (tmp >= threshold):
                                count += 1
                if (count > 0):
                        cntX[x] = count

        #i = 0
        #for k,v in sorted(cntE.items(), key=operator.itemgetter(1), reverse=True):
                #if (v > 1):
                #       print nodeIdMap[k], ": has investors ", v
                #if (all == False and i > 10):
                #       break
                #i += 1
        #print "no. of %s  with threshold %f following %d" % (str, threshold,len(cntX))
        return len(cntX)

def calcEmpHighs(threshold, all):

	#print "High Employees for %f" % threshold
 	cntE = {}
        for e in povermMap:
                count = 0
                for tmp in povermMap[e] :
                        if (tmp >= threshold):
                                count += 1
		if (count > 0):
			cntE[e] = count

	#i = 0
	#for k,v in sorted(cntE.items(), key=operator.itemgetter(1), reverse=True):
		#if (v > 1):
		#	print nodeIdMap[k], ": has investors ", v
		#if (all == False and i > 10): 
		#	break	
		#i += 1
	#print "no. of employees with threshold %f investor follow %d" % (threshold,len(cntE))
	return len(cntE)

def calcFollows(threshold, pover) :
	count = 0
	for e in pover:
		bFollows = True
		for tmp in pover[e]:
			if (tmp < threshold):
				bFollows = False
				break
		if (bFollows == True):
			#print "Follow 100 %d %s %d "%(e,nodeIdMap[e],len(povermMap[e]))
			count += 1
	return count

def calcAllFollows() :
	thres = 0.1
	fE = {}
	fI = {}
	while (thres <= 1.0):
		fI[thres] = calcFollows(thres, poverkMap)
		fE[thres] = calcFollows(thres, povermMap)
		thres += 0.01
	return (fI, fE)
			

def getIntersects(emp, empset,  inv, invset):
	matches = empset & invset
	if len(matches) == 0:
		return 0
	else :
		cnt = 0
	for  company in matches:
		if (isEmpBeforeInv(emp, inv, company) == True):
			cnt += 1
	return cnt
		
def isEmpBeforeInv(emp, inv, c):
	empDate =sorted(datesDict[(emp,c)])[0]
	invDate =sorted(datesDict[(inv,c)])[0]
	if (empDate < invDate):
		return True
	else:
		return False
	
def putpoversMap(val, key, dict, jval, jmap):
	if (key in dict):
		out = dict[key]
		out.append(val)	
		outj = jmap[key]
		outj.append(jval)
	else:
		out = []
		out.append(val)
		outj = []
		outj.append(jval)
	dict[key] = out
	jmap[key] = outj


#calculate investors -> company degrees
def getICDeg(i) : 
        companies = set()
        investor = graph.GetNI(i)
        edges = investor.GetOutEdges()
        for e in edges :
                companies.add(e)
	return companies

def getAllICDeg():
	T = {}
	for idx in range(investors) :
        	i = idx + invIndex
        	tmp = getICDeg(i)	
		if len (tmp) > 0:
			T[i] = tmp
	pickle.dump(T, open('TIs', 'wb'))

def getAllECDeg():
	R = {}
	for edx in range(employees):
                e = edx + empIndex
              	tmp = getECDeg(e)
                if (len(tmp) > 0):
			R[e] = tmp
	pickle.dump(R, open('REs','wb'))	


# calculate Employees -> company degrees
def getECDeg(j):
	print j
	emp = graph.GetNI(j)
	companies = set()
	edges = emp.GetOutEdges()
	for e in edges :
		companies.add(e)
	return companies

def employeeIsInvestor(e, i):
	if nodeIdMap[e] == nodeIdMap[i]:
		return True

def processPsMs() :
	intersects = 0
	poverkMap = {}
	jacIMap = {}
	povermMap = {}
	jacEMap = {}
	overlapFound = 0

	print " calculating poverk and poverm"
	excInv = 0
	for idx in range(investors) :
        	i = idx + invIndex
        	#if (i % 1000 == 0):
                #	print "processing %d investor " % i
        	TI = TIs[i]
       		if (len(TI) == 0 or len(TI) == 1):
			excInv += 1
                	continue	
		excEmp = 0
       		for edx in range(employees):
               		e = edx + empIndex
               		RE = REs[e]
                	if (len(RE) == 0 or len(RE) == 1):
				excEmp += 1
                       		continue
			if employeeIsInvestor(e, i):
				overlapFound += 1
				continue
                	p = getIntersects(e, RE, i, TI)
               		if (p > 1 ):
                        	r = len(RE)
                        	t = len(TI)
                       		intersects += 1
                       		poverk = (p*1.0)/(1.0*t)
				jaccardI = (p*1.0)/(t+r)
                       		putpoversMap(poverk, i, poverkMap, jaccardI, jacIMap)
                       		poverm = (1.0*p)/(1.0*r)
				jaccardE = (1.0*p)/(t+r)
                       		putpoversMap(poverm, e, povermMap, jaccardE, jacEMap)
				
	poverkmap = open('pkmap', 'wb')
	pickle.dump(poverkMap, poverkmap)

	povermmap = open('pmmap', 'wb')
	pickle.dump(povermMap, povermmap)

	pickle.dump(jacEMap, open('jacEMap', 'wb'))
	pickle.dump(jacIMap, open('jacIMap', 'wb'))

	#print "intersects = %d Inv %d Emp %d " % (intersects, investors-excInv, employees-excEmp)
	print "intersects %d size(poverk) %d size(poverm) %d " % (intersects, len(poverkMap), len(povermMap))
	print overlapFound
	return excInv, excEmp


def processPsMs2():
  seenPairs = dict()
  seenPairs = defaultdict(lambda: False, seenPairs)
  intersects = 0
  comparisons = 0
  totalCompanies = 0
  poverkMap = {}
  povermMap = {}
  jaccardMapE = {}
  jaccardMapI = {}
  intersectDict = {}
  totalEmployees = set()
  totalInvestors = set()
  print "calculating poverk, poverm, jaccard using companies"
  for cdx in range(companies):
    c = cdx + compIndex  
    if (c % 1000 == 0):
      print "processing %d company " % c
    employees, investors, comps = getEmpsAndInvs(c)
    totalCompanies += len(comps)
    for e in set(employees):
      totalEmployees = totalEmployees | set(employees)
      for i in set(investors):
        totalInvestors = totalInvestors | set(investors)
      # print "about to do the thing with the thing!", e, i
        if seenPairs[(e, i)] == False: #if we haven't done this pair yet
          RE = REs[e]
          TI = TIs[i]
          p = getIntersects(e, RE, i, TI)
          if p > 0:
            intersects += 1
            intersectDict[(e, i)] = (RE, TI)
          seenPairs[(e, i)] = True
          r = len(RE)
          t = len(TI)
          poverk = (p*1.0)/(1.0*t)
          putpoversMap(poverk, i, poverkMap)
          poverm = (1.0*p)/(1.0*r)
          putpoversMap(poverm, e, povermMap)
          jaccard = (p*1.0)/(1.0*(t + r))
          putpoversMap(jaccard, e, jaccardMapE)
          putpoversMap(jaccard, i, jaccardMapI)
      comparisons += 1
  poverkmap = open('pkmap2.p', 'wb')
  pickle.dump(poverkMap, poverkmap)
  povermmap = open('pmmap2.p', 'wb')
  pickle.dump(povermMap, povermmap)
  jaccardE = open('jaccardE2.p', 'wb')
  pickle.dump(jaccardMapE, jaccardE)
  jaccardI = open('jaccardI2.p', 'wb')
  pickle.dump(jaccardMapI, jaccardI)
  pickle.dump(intersectDict, open("intersectDict2.p", "wb"))
  print "intersects = %d " % intersects
  print "comparisons = %d" % comparisons
  print "totalCompanies = %d" % totalCompanies
  return len(totalEmployees), len(totalInvestors)

#all in one graph for analysis
#graph = snap.LoadEdgeList(snap.PUNGraph, "compinvemp-graph9.txt", 1, 0)
graph = snap.LoadEdgeList(snap.PUNGraph, "allEdges.txt", 1,0)
#snap.SaveEdgeList(graph, "all-graph9.txt")

empIndex = 100000
invIndex = 200000

companies = 14785
investors = 15225#13563
employees = 39587
print "Companies = %d " % companies
print "Investors = %d" % investors
print "Employees = %d" % employees

#run through out degrees for investors and employees for preprocessing
# getAllECDeg()
# getAllICDeg()

# load all preprocessed data
#datesDict = pickle.load(open('dtDatesDict.p', 'rb'))
datesDict = pickle.load(open('dtDateDict5.p', 'rb'))
REs = pickle.load((open('REs', 'rb')))
TIs = pickle.load((open('TIs', 'rb')))

#load node ids to string
# nodeFile = open("nodeIDs9.txt", 'r')
# out = nodeFile.readlines()
# nodeIdMap = {}
# for line in out:
# 	words =	line.strip().rsplit('\t')
# 	nodeIdMap[int(words[0])] = words[1]
nodeIdMap = pickle.load(open("intDict5.p"))


#run through ps and ms for preprocessing
#excI, excE = processPsMs()
#print excI, excE
excI = 10230
excE = 33703
#load processed ps and ms
povermMap = load('pmmap')
poverkMap = load('pkmap')
jacEMap = load('jacEMap')
jacIMap = load('jacIMap')

# plotDist("Distribution of p/k", "p/k", "Employee Matches at Threshold", poverkMap, "CB224/results/fig11.png")
# plotDist("Distribution of p/m", "p/m", "Investor Matches at Threshold", povermMap, "CB224/results/fig12.png")

#calculate Qs and Ss for different threshold
#q,s = calcQsSs(investors - excI, employees - excE) 
#calculate Qs and Ss for different threshold
q,s, qj, sj, qw, sw = calcQsSs(investors - excI, employees - excE)
plotWholeGraphStats("Distribution of Similarity Metrics For Whole Graph At Threshold", "Proportion of Whole Graph", qw, sw, "CB224/results/fig1.png")
plotReducedGraphStats("Distribution of Similarity Metrics For Followed/Followers At Threshold", "Proportion of Followed or Followers", q, s, qj, sj, "CB224/results/fig2.png") 

# plotDistMatches("Distribution of q", "q", "Investor Frequency", q)
# plotDistMatches("Distribution of s", "s", "Employee Frequency", s)

#calculate employees with high threshold and counts and p/m
#EmpInvMatches = calcEmpHigh()
#plotDistEmpInvMatches("Employees With An Investor Match At Or Above Threshold", EmpInvMatches, "No. Employees", "CB224/results/fig3.png")

# plotDistEmpInvMatcheslog("log-log Employee followed by atleast 1 investor with Threshold", EmpInvMatches, "Employees", "CB224/results/fig4.png")

# InvEmpMatches = calcHigh("investor", poverkMap)
# plotDistEmpInvMatches("Distribution of Investors following at least 1 employee At Or Above Threshold", InvEmpMatches, "Investors", "CB224/results/fig5.png")
# plotDistEmpInvMatcheslog("log-log Distribution of Investors following atleast 1 employee with Threshold", InvEmpMatches, "Investors", "CB224/results/fig6.png")



#, EmpInvMatches, InvEmpMatches)
# plotDistEmpInvMatches("Distribution of Investors q", q, "Investors q")
#plotDistEmpInvMatches("Distribution of Employees s", s, "Employees s")

#print "All 100% follows between Employees and Investors"
#calcEmpHighs(1.0, True)

# ###### Investors and 
#fInv, fEmp = calcAllFollows()
#plotDistEmpInvMatches("Employees Followed by All Their Investors At or Above Threshold", fEmp, "No. Employees", "CB224/results/fig7.png")
# plotDistEmpInvMatcheslog("Log Employees Followed by All Their Investors At or Above Threshold", fEmp, "No. Employees", "CB224/results/fig8.png")

# plotDistEmpInvMatches("Investors following employees with threshold & above always", fInv, "Investor", "CB224/results/fig9.png")
# plotDistEmpInvMatcheslog("Investors following employees with threshold & above always", fInv, "Investor", "CB224/results/fig10.png")

# calcAllFollowCount()
currThreshold = 1.0
#starDist = calcStarDist(currThreshold, povermMap)
title = "Number of Followers With Threshold at {}".format(currThreshold)
# plotStarDist(title, "Number of Investor Followers", "Number of Employees Followed", starDist)
