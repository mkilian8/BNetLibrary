from net1 import *
from bnet import solve

from itertools import permutations
import unittest

class TestVariableElimination(unittest.TestCase):
    def solve_permutation(self, *args, **kwargs):
        factors = [A,B,C,D,E]
        last_seen = None
        for f in permutations(factors, 5):
            result = solve(list(f), *args, **kwargs)
            if not last_seen:
                last_seen = result 
            self.assertEqual(last_seen, result)
            #print result 
        return last_seen

    def test_multiple_direct_dependencies(self):
        rv = self.solve_permutation('ABCDE', 'D=F', C='T', B='T')
        self.assertEqual( round(rv, 2), 0.90 )
        rv = self.solve_permutation('ABCDE', 'D=F', C='F', B='T')
        self.assertEqual( round(rv, 1), 0.1 )

    def test_single_indirect_dependencies(self):
        rv = self.solve_permutation('ABCDE', 'D=T', A='F')
        self.assertEqual( round(rv, 4), 0.6485 )
        rv = self.solve_permutation('ABCDE', 'D=T', A='T')
        self.assertEqual( round(rv, 5) , 0.71975 )

    def test_single_sibling(self):
        rv = self.solve_permutation('ABCDE', 'D=T', E='F')
        self.assertEqual( round(rv, 12), 0.665775547445 )
        rv = self.solve_permutation('ABCDE', 'D=T', E='T')
        self.assertEqual( round(rv, 5), 0.72403 )

    def test_vstructure(self):
        rv = self.solve_permutation('ABCDE', 'C=T', B='F')
        self.assertEqual( round(rv, 2), 0.35 )
        rv = self.solve_permutation('ABCDE', 'C=T', B='T')
        self.assertEqual( round(rv, 2), 0.35 )



