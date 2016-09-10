import json

from libpgm.nodedata import NodeData
from libpgm.graphskeleton import GraphSkeleton
from libpgm.discretebayesiannetwork import DiscreteBayesianNetwork
from libpgm.tablecpdfactorization import TableCPDFactorization

# load nodedata and graphskeleton
nd = NodeData()
skel = GraphSkeleton()
nd.load("tests/net1.json")    # any input file
skel.load("tests/net1.json")

# topologically order graphskeleton
skel.toporder()

# load bayesian network
bn = DiscreteBayesianNetwork(skel, nd)

fn = TableCPDFactorization(bn)


# sample 
result = fn.specificquery(dict(E='F'), {})

# output
print json.dumps(result, indent=2)
