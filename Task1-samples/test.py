import pylab as pl
import numpy as np

a = [1,5,6,52,63,84,95,67,89] 
b = np.append(a,1)
print(b)
bins = np.linspace(0,100,20)

pl.hist(a,bins)
pl.show()