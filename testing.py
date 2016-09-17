from loggers import log
from bnet import solve

from tests.net1 import *


if __name__ == '__main__':
    log.setLevel('INFO')
    #pgm = bn.BnetGraph()
    #pgm.add_nodes_from([A,B])
    #pgm.add_edges_from([('A','B')])
    ED = E * D
    print 'ED: ', ED
    #import pdb; pdb.set_trace()
    BED = B * ED
    print 'BED: ', BED
    ABED = A * BED
    print 'ABED: ', ABED
    ABED_sum = ABED.sum('A')
    print 'ABED multiplied', ABED_sum
    ABED_reduce = ABED_sum.reduce(B='F')
    print 'ABED reduced factor', ABED_reduce

    rv = solve([A,B,C,D,E], 'ABCDE', 'D=T', E='F')
    print 'Result: ', rv
    import pdb; pdb.set_trace()
    pass

