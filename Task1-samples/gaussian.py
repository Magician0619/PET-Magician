import numpy as np
import pylab as plt
#import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
 
x = range(10)
y = [0,1,2,3,4,5,4,3,2,1]
 
 
def gaussian(x,*param):
    return param[0]*np.exp(-np.power(x - param[2], 2.) / (2 * np.power(param[4], 2.)))+\
           param[1]*np.exp(-np.power(x - param[3], 2.) / (2 * np.power(param[5], 2.)))
 
 
popt,pcov = curve_fit(gaussian,x,y,p0=[3,4,3,6,1,1])
print (popt)
# print pcov
 
plt.plot(x,y,'b+:',label='data')
plt.plot(x,gaussian(x,*popt),'ro:',label='fit')
plt.legend()
plt.show()
