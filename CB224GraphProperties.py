import snap
import matplotlib.pyplot as plt
import pickle

def plotGraph(input) :

	x = [i.GetVal1() for i in input]
	y = [j.GetVal2() for j in input]

	plt.title("Investor Company Distribution")
	plt.xlabel("Investor Degree"	)
	plt.ylabel("Companies")
	plt.loglog(x,y,'ro', basex=10,basey=10)
	plt.show()
	


#edges for two different graphs
companyEmployeeGraph = snap.LoadEdgeList(snap.PNEANet, "CB224/company-emp-graph11.txt", 1, 0)
companyInvestorGraph = snap.LoadEdgeList(snap.PNEANet, "CB224/company-inv-graph11.txt", 1, 0)
graph = snap.LoadEdgeList(snap.PNEANet, "allEdges.txt", 1, 0)

#dates for different edges, in format (pair of nodes) as key, (list of dates for pair) as value
#since we can have multiple dates for the same edge, value is list of dates
# invDatesDict = pickle.load(open("invDateDict5.p", "rb"))
# empDatesDict = pickle.load(open("empDateDict5.p", "rb"))

#string-nodeID correlation for each node (in either graph)
# nodesDict = pickle.load(open("nodeDict5.p", "rb"))

#just to make sure they loaded happily
# print "company emp nodes: {}".format(companyEmployeeGraph.GetNodes())
# print "company emp edges: {}".format(companyEmployeeGraph.GetEdges())
# print "company inv nodes: {}".format(companyInvestorGraph.GetNodes())
# print "company inv edges: {}".format(companyInvestorGraph.GetEdges())
# print "investor dates dict size: {}".format(len(invDatesDict))
# print "employee dates dict size: {}".format(len(empDatesDict))
# print "nodes dict size: {}".format(len(nodesDict))

#Trial that failed (before I mapped string nodes to int IDs myself)
# mapping = snap.TStrIntH()
# companyEmployeeGraph = snap.LoadEdgeListStr(snap.PUNGraph, "testGraph.txt", 0, 1, mapping)
# mapping2 = snap.TStrIntH()
# companyInvestorGraph = snap.LoadEdgeListStr(snap.PUNGraph, "company-investor.txt", 0, 1, mapping2)

# CompanyInvDegCntV = snap.TIntPrV()
# snap.GetDegCnt(companyInvestorGraph, CompanyInvDegCntV)
# for  item in CompanyInvDegCntV:
# 	print "%d degree for nodes %d" % (item.GetVal1(), item.GetVal2())

# snap.PlotInDegDistr(companyInvestorGraph, "InvCompany",\
# 			 "Investor-Company In Degree Distribution" \
# 			)
# print "Company Employee stats" 

# CompanyEmpDegCntV = snap.TIntPrV()
# snap.GetDegCnt(companyEmployeeGraph, CompanyEmpDegCntV)
# for item in CompanyEmpDegCntV:
# 	print "%d degree with nodes %d" % (item.GetVal1(), item.GetVal2())

# plotGraph(CompanyEmpDegCntV)

snap.PrintInfo(companyInvestorGraph, "Company Investor Graph", "CIStats.txt", False)

snap.PrintInfo(companyEmployeeGraph, "Company Employee Graph", "CEStats.txt", False)
snap.PrintInfo(graph, "whole graph", "GStats.txt", False)


