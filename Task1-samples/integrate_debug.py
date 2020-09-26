#  -*- coding:utf-8 -*-

'''
#@Author: Magician
#@Date: 2020-09-22 19:23:50 
#@Description: 

Copyright 2020 by Magician
'''
import math
import random
import struct

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xlwt
from matplotlib.ticker import FuncFormatter
# from sympy import * 
from scipy import integrate
from scipy.optimize import curve_fit


binFile = open('E:\\PET\\数据集\\6BDM.samples','rb')
poly = binFile.read()
print("字节长度：",len(poly))
circle = int(len(poly)/68)+1
print("帧数：",circle-1)

circle = 10  # 分析前100组数据 

global x_rate, y_rate 
global popt
x_rate = 1 # 将单位进行放缩
y_rate = 1000 # 将单位进行放缩
popt = []
num = [40,110,180,270,270,180,110,40]
y = np.array(num)



def double_exp(x,a,b,c,d):
    '''
    双指数函数曲线
    '''
    return  a*np.exp(b*(x-c))*(1-np.exp(d*(x-c)))
def monto(x,a,b):
    """
    # a,b为求取积分的上下限
    """
    return (b-a)/len(x)*sum(double_exp(x,popt[0],popt[1],popt[2],popt[3]))

def integral(a,b):
    """
    # a,b为求取积分的上下限
    """
    return double_exp(b,popt[0],popt[1],popt[2],popt[3]) - double_exp(a,popt[0],popt[1],popt[2],popt[3])

def func(x):
    return popt[0]*np.exp(popt[1]*x)+popt[2]*np.exp(popt[3]*x)


for i in range(circle):
    poly_func = poly[i*68:(i+1)*68]
    content = struct.unpack('<hhdddddddd', poly_func)
    x_list = []
    # print(c)
    for m in range(2,10):
        x_list.append(float(content[m]))
    for j in range(8): 
        x_list[:] = [x - x_list[0] for x in x_list]
    x = np.array(x_list)
    x_dexp = x/x_rate
    y_dexp = y/y_rate
    popt, pcov = curve_fit(double_exp, x_dexp, y_dexp,maxfev=500000)
    # print("所得双指数函数形式为：%fexp(%f*x)+%fexp(%f*x)"%(popt[0],popt[1],popt[2],popt[3]))
    x_inter = np.linspace(0,x_dexp[7],1000)
    y_inter = double_exp(x_inter,popt[0],popt[1],popt[2],popt[3]) #拟合y值
    # E = integral(0, x_inter[-1])
    # E = integrate.quad(double_exp(x,popt[0],popt[1],popt[2],popt[3]),0, x_inter[-1])

    # added
    plt.rcParams['font.family'] = ['Times New Roman']
    # plt.rcParams.update({'font.size': 8})
    plt.figure("双指数插值曲线")
    plt.plot(x_inter, y_inter, 'r',label='polyfit values')
    # plt.plot(x, y, 's',label='original values')
    plt.title('Double exponential interpolation curve')
    plt.xlabel('Time(ns)')
    plt.ylabel('Voltage(mv)')

    integral,error = integrate.quad(func,0, x_inter[-1])
    E = integral*x_rate*y_rate
    print("第%d次的积分值%f"%(i+1,E))

    plt.show()
