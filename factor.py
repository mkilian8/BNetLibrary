import numpy as np
from loggers import log
from lib.MetaArray import MetaArray

class Factor(MetaArray):
    def __mul__(self, b):
        a = self
        if len(b.shape) > len(a.shape):
            a = b
            b = self
        bVars = b.variables()
        bAxis = b.axes()
        log.debug('Multiplying factors %s and %s', a, b)
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
        return a
        
    def rollaxis(self, axis, start=0):
        new_array = np.rollaxis(self, axis, start=start)
        info = self._info
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
        pass
    
    def reduce(self, e):
        pass

    def variables(self):
        return self.infoCopy()[-1]['variables']
    
    def axes(self):
        return { d['name']: i for i,d in enumerate(self.infoCopy()[:-1]) }

