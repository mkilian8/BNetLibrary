from loggers import log
import bngraph as bn
import numpy as np
from factor import Factor

'''
c
c > e
a
a > b
cb > d
'''

A = Factor(np.array([0.5,0.5]), info=[
        dict(name='A', values=['T', 'F']),
        dict(variables='A')
    ], copy=True)

B = Factor(np.array([
        [0.3, 0.7],
        [0.8, 0.2]
    ]), info=[
        dict(name='A', values=['T', 'F']),
        dict(name='B', values=['T', 'F']),
        dict(variables='B')
    ], copy=True)

C = Factor(np.array([0.35, 0.65]), info=[
        dict(name='C', values=['T', 'F']),
        dict(variables='C')
    ], copy=True)

E = Factor(np.array([
        [0.25, 0.75],
        [0.35, 0.65]
    ]), info=[
        dict(name='C', values=['T', 'F']),
        dict(name='E', values=['T', 'F']),
        dict(variables='E')
    ], copy=True)

D = Factor(np.array([
        [
            [0.1, 0.9],
            [0.6, 0.4]
        ],
        [
            [0.9, 0.1],
            [0.85, 0.15]
        ]
    ]), info=[
        dict(name='C', values=['T', 'F']),
        dict(name='B', values=['T', 'F']),
        dict(name='D', values=['T', 'F']),
        dict(variables='D')
    ])

if __name__ == '__main__':
    log.setLevel('DEBUG')
    pgm = bn.BnetGraph()
    pgm.add_nodes_from([A,B])
    pgm.add_edges_from([('A','B')])
    ED = E * D
    print 'ED: ', ED
    #import pdb; pdb.set_trace()
    BED = B * ED
    print BED
    #import pdb; pdb.set_trace()
    pass

