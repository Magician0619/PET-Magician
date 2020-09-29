import pylab as pl
import numpy as np

a = [1,533,6,52,63,84,95,67,89] 

b = np.linspace(0,10,10)
print(a.index(max(a)))

global c
c=0
for i in range(10):
    c = i

print(c)