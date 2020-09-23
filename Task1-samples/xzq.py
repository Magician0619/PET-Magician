import struct
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
import math
import random
import csv


binFile=open('cy.samples','rb')
a=binFile.read()

print(len(a))
cycle=int(len(a)/67)+1

print(cycle-1)

cycle=8  #前七组数据 

squares=[]        
for i in range(1,cycle,1):
    b=a[(i-1)*67:i*67]
    c=struct.unpack('<Bhdddddddd', b)
    print(c)
    for j in range(2,10): 
        squares.append(c[j]-52595219954)
print(squares)

       
def func(x, a,b,c,d,e):
    return  a*np.exp(b*x)+c*np.exp(d*x)+e

#定义x、y散点坐标
x = squares[0:8]
x=np.array(x)

print('x is :\n',x)
num = [40,110,180,270,270,180,110,40]
y = np.array(num)
print('y is :\n',y)

popt, pcov = curve_fit(func, x, y)

a = popt[0]
b = popt[1]
c = popt[2]
d = popt[3]
e = popt[4]
x_new=np.linspace(0,squares[7],1000)
yvals = func(x_new,a,b,c,d,e) #拟合y值
print(u'系数a:', a)
print(u'系数b:', b)
print(u'系数c:', c)
print(u'系数d:', d)
print(u'系数e:', e)
#绘图
plot1 = plt.plot(x, y, 's',label='original values')
plot2 = plt.plot(x_new, yvals, 'r',label='polyfit values')
plt.xlabel('x')
plt.ylabel('y')
plt.legend(loc=1) #指定legend的位置右下角
plt.title('curve_fit')
plt.show()
