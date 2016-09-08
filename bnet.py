


def solve(factors, variables, query, **evidence):
    # Reduce by evidence
    # Eliminate vars
    result = None
    for z in variables:
        if z in query:
            continue
        joint = None
        for i in xrange(len(factors)):
            f = factors[i]
            if f.variables().has_key(z):
                joint = joint * f if joint else f 
                del factors[i]
        result = joint.sum(z)
        factors.push(result)
