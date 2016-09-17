

# Supports single variable queries, potentially with query for result value
def solve(factors, variables, query, **evidence):
    # Reduce by evidence
    for z in variables:
        if z in query:
            continue
        joint = None
        for i in xrange(len(factors)):
            f = factors[i]
            if f.axes().has_key(z):
                joint = joint * f if joint is not None else f 
                factors[i] = None
        if evidence.has_key(z):
            # Eliminate vars
            joint = joint.reduce(**{z:evidence[z]})
        else:
            joint = joint.sum(z)
        factors.append(joint)
        factors = filter(lambda f: f is not None, factors)
    result = reduce(lambda c, f: c * f, factors[1:], factors[0])
    if '=' in query:
        q = query.split('=')
        varIndex = result.axes()[q[0]]
        valIndex = list(result.infoCopy()[varIndex]['values']).index(q[1])
        return result[q[0]:valIndex]
    return result
