


def solve(factors, variables, query, **evidence):
    # Reduce by evidence
    #TODO: Reduce at the end when factors multiplied in
    for i in xrange(len(factors)):
        f  = factors[i]
        ef = { n: evidence[n] for n in f.axes().keys() if evidence.has_key(n) }
        if len(ef):
            f[i] = f.reduce(**ef)
    # Eliminate vars
    for z in variables:
        if z in query:
            continue
        joint = None
        for i in xrange(len(factors)):
            f = factors[i]
            if f.axes().has_key(z):
                joint = joint * f if joint is not None else f 
                factors[i] = None
        factors.append(joint.sum(z))
        factors = filter(lambda f: f is not None, factors)
    return factors
