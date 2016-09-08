import numpy as np
from loggers import log
from lib.MetaArray import MetaArray

class Factor(MetaArray):
    def __mul__(self, b):
        a = self
        if len(b.shape) > len(a.shape):
            a = b
            b = self
        a = Factor(a, copy=True)
        b = Factor(b, copy=True)
        bVars = b.variables()
        bAxis = b.axes()
        log.info('Multiplying factors \n %s \n AND \n %s', a, b)
        #import pdb; pdb.set_trace()
        for axis, i in reversed(bAxis.items()):
            aVars = a.variables()
            aAxis = a.axes()
            if aAxis.has_key(axis):
                a = a.rollaxis(aAxis[axis])
            else:
                a = a.resize((b.shape[i],) + a.shape, [b.infoCopy()[i]] + a.infoCopy())
                for j in xrange(b.shape[i]):
                    a[j] = a[0]
            log.debug('Array after axis roll or resize %s', a)
        
        for index in np.ndindex(*b.shape):
            log.debug('Multiplying %s at index %s in \'a\' by %s', a[index], index, b[index])
            a[index] *= b[index]
        a._info[-1]['variables'] += bVars
        return a
        
    def rollaxis(self, axis, start=0):
        new_array = np.rollaxis(self, axis, start=start)
        info = self.infoCopy()
        info.insert(start, info.pop(axis))
        new_array._info = info
        return new_array

    def resize(self, new_shape, info, **kwargs):
        #Copy array to new ndarray
        #Resize
        #Return new Factor referenced to resized ndarray
        #import pdb; pdb.set_trace()
        ary = np.array(self, order='C')
        ary.resize(new_shape, **kwargs)
        return Factor(ary, info=info)

    def sum(self, var):
        i = self.axes()[var]
        info = self.infoCopy()
        if var not in self.variables():
            log.error('Summing out variable %s that hasn\'t been multiplied in!', var)
        else:
            info[-1]['variables'] = info[-1]['variables'].replace(var, '') 
        info.pop(i)
        return Factor(super(Factor, self).sum(axis=(i,)), info=info)
     
    def reduce(self, **evidence):
        #Only possible to reduce by one node at the moment
        var, val = evidence.popitem()
        info = self.infoCopy()
        i = self.axes()[var]
        j = list(info[i]['values']).index(val)
        log.info('Reducing by variable %s to value %s', var, val)
        ary = self[var: j] 
        ary._info[-1]['variables']  = ary._info[-1]['variables'].replace(var, '')

        cAxes = [ k for a,k in ary.axes().iteritems() if a not in ary.variables() ]
        cDims = tuple( ary.shape[l] for l in cAxes )
        log.debug('Conditioning axes:\n %s', list(cAxes))
        log.debug('Conditioning dimensions:\n %s', cDims)

        for d in np.ndindex(*cDims):
            index = tuple( slice(axisLength) if m not in cAxes else d[cAxes.index(m)] for m, axisLength in enumerate(ary.shape)  ) 
            log.debug('Summing at index: %s', index)
            ary[index] /= super(Factor, ary[index]).sum()
        return ary

    def variables(self):
        return self.infoCopy()[-1]['variables']
    
    def axes(self):
        return { d['name']: i for i,d in enumerate(self.infoCopy()[:-1]) }

