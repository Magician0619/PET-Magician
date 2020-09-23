#  -*- coding:utf-8 -*-

'''
#@Author: Magician
#@Date: 2020-09-22 19:23:50 
#@Description: 

Copyright 2020 by Magician
'''
import struct
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
import math
import random
import csv


binFile = open('cy.samples','rb')
a = binFile.read()
print("字节长度：",len(a))
cycle = int(len(a)/67)+1
print("帧数：",cycle-1)

cycle = 10  #前七组数据 

squares = []

for i in range(cycle):
    b = a[i*67:(i+1)*67]
    c = struct.unpack('<Bhdddddddd', b)
    # print(c)
    for j in range(2,10): 
        squares.append(c[j]-c[2])
        # print("时间：",c[j]-c[2])
   
def double_exp(x,a,b,c,d,e):
    '''
    双指数函数曲线
    '''
    return  a*np.exp(b*x)+c*np.exp(d*x)+e
    # return  a*np.exp(b*x)+c*np.exp(d*x)


def Polynomial(x,y):
    '''
    多项式拟合函数
    '''
    a=np.polyfit(x,y,2)#用2次多项式拟合x，y数组
    b=np.poly1d(a)#拟合完之后用这个函数来生成多项式对象
    c=b(x)#生成多项式对象之后，就是获取x在这个多项式处的值
    plt.scatter(x,y,marker='o',label='original datas')#对原始数据画散点图
    plt.plot(x,c,ls='--',c='red',label='fitting with second-degree polynomial')#对拟合之后的数据，也就是x，c数组画图
    plt.legend()
    plt.show()


# 定义原始数据x、y的散点坐标
x = squares[0:8]
x = np.array(x)
print('x的坐标:',x)

num = [40,110,180,270,270,180,110,40]
y = np.array(num)
print('y的坐标:',y)


# 曲线拟合
#
# print(func(x, a,b,c,d,e))
popt, pcov = curve_fit(double_exp, x, y)



x_new = np.linspace(0,squares[7],1000)
yvals = double_exp(x_new,popt[0],popt[1],popt[2],popt[3],popt[4]) #拟合y值

y_fit = double_exp(x,popt[0],popt[1],popt[2],popt[3],popt[4])
# print("yvals:",yvals)
print(u'系数a:', popt)

#绘图
plt.figure("hello")
plot1 = plt.plot(x, y, 's',label='original values')
plt.figure(2)
plot2 = plt.plot(x_new, yvals, 'r',label='polyfit values')
plt.figure(3)
plot2 = plt.plot(x, y_fit, 'r',label='polyfit values')

plt.xlabel('x')
plt.ylabel('y')
plt.legend(loc=1) #指定legend的位置右下角
plt.title('curve_fit')
plt.show()
