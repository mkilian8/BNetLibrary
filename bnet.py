import pdb
import random
import numpy as np
import networkx as nx
from lib.MetaArray import MetaArray

class Factor(MetaArray):
    def __init__(self, *vargs, **kwargs):
        super(Factor, self).__init__(*vargs, **kwargs)
            
    '''        
    def contains(self, var,val=None):
        info = self.infoCopy()
        for axis in info:
            if axis['name'] == var:
                if not val or val in axis['values']:
                    return True
        return False
    '''
    '''
    def conditionals(self):
        return [ info['name'] for info in self.infoCopy() if info['C'] == True ]
    '''
    
    def __sub__(self, other):
        pass

    def __add__(self, other):
        pass

    #TODO:implement variable descriptor object
    def __contains__(self, var):
        return var in zip(*list(self._variables()))[1]

    def __iter__(self):
        return zip(*list(self._variables()))[1]


    #return AXES
    def get_axes_mappings(var_set=set([]), *factors):
        #TODO: call indexing method on factor, not implemented yet
        var_set = list(var_set)
        this_axes = [i for i,var in self._variables() if var in var_set]
        other_axes = [factor.get_axes_mappings(var_set)[1] for factor in factors]
        
        mappings = [this_axes] + other_axes
        return mappings

    def get_axes(var_set=set([])):
        shape = np.shape(self)
        #axes = [ name, shape[i] for i,name in self._variables if name in var_set ]
        axes = ''
        return axes

    def prepend_axes(axes):
        names, shapes = zip(*axes)
        self.resize(shape + np.shape(self))
        self._info[:0] = axes

    def _variables(self):
        info = self.infoCopy()
        #set( (i,a for i,a in enumerate([{'name':'a'}, {'name':'b'}, {'name':'b'}])) )
        enum = (i for i in range(1,10))
        pdb.set_trace()
        #return set( (i,a['name'] for i,a in enumerate(info)) )
        

    #TODO: static method implementation
    @staticmethod
    def multiply(cls, mergers):
        factor = random.sample(mergers, 1)
        for other in mergers:
            other_vars = set([])
            merge_vars = set([])
            for var in other:
                other_vars.add(var)
                if var not in factor:
                    merge_vars.add(var)
                
            axes = other.get_axes(merge_vars)
            factor.prepend_axes(axes)
            mappings = factor.get_axes_mappings(other_vars, other)
    
            for i,m in np.ndenumerate(other):
                #TODO: implement indexing, use mappings bw/ factors axes
                shp = list(np.index_exp[:] * len(np.shape(factor)))
                for ax in mappings[0]:
                    shp[ax] = np.shape(factor)[ax]
                factor[tuple(shp)] *= m

    def normalize():
        self /= self.sum()
    
    '''
    def sum_out(self, var):
        np.sum(self )
        self[var:np.s_[:]]
    '''


#TODO: network-based elimination/hashing - fewer searches
#seeds a factor and eliminates all vars not in query set by merging with other factors and summing
def infer(in_graph, qry):
    def merge_node_list(nlist):
        for n in nlist:
            factor = out_graph.node[n]
            new_node = cur_factor.multiply(factor)                             #multiply factors
            cur_factor.sum_out(qry)                                                #sum out factors
            nx.relabel_nodes(out_graph, {cur_node: new_node}, copy=False)

            #reconnect graph
            lprev = out_graph.predecessors(n)
            lnext = out_graph.successors(n)
            ebunch = zip([new_node]*len(lnext), lnext)
            ebunch += zip(lprev, [new_node]*len(lprev))
            out_graph.add_edges_from(ebunch)
            return new_node

    out_graph = in_graph.copy()
    cur_node = out_graph.nodes().pop()
    cur_factor = out_graph.node[cur_node]
    while True:
        prev_list = out_graph.predecessors(cur_node)
        next_list = out_graph.successors(cur_node)
        if len(prev_list) or len(next_list):
            cur_node = merge_node_list(prev_list)
            cur_node = merge_node_list(next_list)
        else:
            break


    '''
    qry_factors = set([])
    while len(factors):
        factor = random.sample(factors, 1)
        while True:
            mergers = set([])
            for var in factor:                          #iterate axes
                if var not in qry:  #target var not in query set - merging
                    mergers.add( factor )
                    for other in factors:               #FIXME: don't search all other factors
                        if var in other:                #iterate axes - TOO SLOW n^2 runtime
                            mergers.add( other )
                    for m in mergers:
                        factors.remove(m)
                    factor = Factor.multiply(mergers)
                    factor.sum(axis=var)
                    break
            else:   #all vars of factor in query set
                qry_factors.add(factor)
                break
    factor = Factor.multiply(qry_factors)
    factor.normalize()
    '''
    pass


def reduce_by_evidence(in_graph, evidence):
    out_graph = nx.DiGraph()
    for var in in_graph.nodes():
        val = evidence[var]
        for var2 in in_graph.successors(var) + [var]:
            if out_graph.node.has_key(var2)
                factor = out_graph.node[var2]['factor']
            else
                factor = in_graph.node[var2]['factor']
            out_graph.add_node(var2, factor=factor[var:val])
            out_graph.add_edge(var, var2)
    return out_graph


C   =    Factor(np.array([0.5,0.5]), info=[{'name':'C', 'values':['F', 'T']}])
S_C =    Factor(np.array([
                    [0.5, 0.5],
                    [0.9, 0.1]
                ]), info=[
                    {'name':'C', 'values':['F','T']},
                    {'name':'S', 'values':['F', 'T']}
                ])
R_C =    Factor(np.array([
                    [0.8, 0.2],
                    [0.2, 0.8]
                ]), info=[
                    {'name':'C', 'values':['F', 'T']},
                    {'name':'R', 'values':['F', 'T']}
                ])
W_SR =   Factor(np.array([
                    [
                        [1.0, 0.0],
                        [0.1, 0.9]
                    ],
                    [
                        [0.1, 0.9],
                        [0.01, 0.99]
                    ]
                ]), info=[
                    {'name':'R', 'values':['F', 'T']},
                    {'name':'S', 'values':['F', 'T']},
                    {'name':'W', 'values':['F', 'T']}
                ])

DG = nx.DiGraph()
DG.add_nodes_from([('C',{'factor':C}), ('S',{'factor':S_C}), ('R',{'factor':R_C}), ('W',{'factor':W_SR})])
DG.add_edges_from([('C','S'), ('C','R'), ('S','W'), ('R','W')])

ev = {'R':0, 'W':1}
qry = set(['W'])


if __name__ == '__main__':
    graph = reduce_by_evidence(DG, ev)
    graph = infer(graph, qry)