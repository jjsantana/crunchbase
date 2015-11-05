from numpy import *
import operator
import time
import snap
import pickle
import matplotlib.pyplot as plt
import pylab as P
import random

# constants defined when graph was created in
# CB224MakeGraph.py
FIRST_COMPANY_NODE_ID = 0
FIRST_EMPLOYEE_NODE_ID = 100000
FIRST_INVESTOR_NODE_ID = 200000

# number of random employees, investors to
# pick for manual sanity check
SAMPLE_SIZE = 10

# dd needs to remain, to enable the reinflation
# of the node and int dicts (default dicts defined
# with dd as their default... artifacts of hacky
# code :-/ )
def dd():
	return False

def get_samples_from_p_over_x_map(pmap, num_samples, id_list, name_map):
	max_id = max(id_list)
	min_id = min(id_list)
	for i in range(num_samples):
		# get a random id in the appropriate range
		random_id = random.randrange(min_id, max_id + 1)
		# while the id generated is not a key in the p over x map
		while random_id not in pmap.keys():
			random_id = random.randrange(min_id, max_id + 1)
		print "node with name {} had a p value of {}".format(name_map[random_id], pmap[random_id])

def run_robustness():
	pmMap = load('pmmap')
	pkMap = load('pkmap')
	idNodeMap = pickle.load(open("intDict5.p"))
	nodeIdMap = pickle.load(open("nodeDict5.p"))
	employeeIds = [iD for iD in idNodeMap.keys() if iD < FIRST_INVESTOR_NODE_ID and iD >= FIRST_EMPLOYEE_NODE_ID]
	investorIds = [iD for iD in idNodeMap.keys() if iD >= FIRST_INVESTOR_NODE_ID]
	print "number of employees: {}, number of investors: {}".format(len(employeeIds), len(investorIds))
	# keys are investor ids in the poverk map, employee ids in the poverm map
	print "Getting sample employees and their p over m values..."
	get_samples_from_p_over_x_map(pmMap, SAMPLE_SIZE, employeeIds, idNodeMap)
	print "Getting sample investors and their p over k values..."
	get_samples_from_p_over_x_map(pkMap, SAMPLE_SIZE, investorIds, idNodeMap)

if __name__ == "__main__":
	run_robustness()
