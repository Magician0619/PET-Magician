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
frame = int(len(poly)/68)+1
print("帧数：",frame-1)

circle = 60450  # 分析前100组数据 

global x_rate, y_rate 
global popt
global space
x_rate = 1 # 将x单位进行放缩
y_rate = 1000 # 将y单位进行放缩
space = 2000
popt = []
num = [40,110,180,270,270,180,110,40]
y = np.array(num)



def double_exp(x,a,b,d):
    """双指数函数
    参数:
    ------------
    x : float
        当前时间与脉冲发生时间的差值
    a : float
        由脉冲幅度决定
    b, d: float
        由脉冲的上升和下降时间决定
    """
    return  a*np.exp(b*(x))*(1-np.exp(d*(x)))

def monto(x,a,b):
    """
    # a,b为求取积分的上下限
    """
    return (b-a)/len(x)*sum(double_exp(x,popt[0],popt[1],popt[2]))

def integral(a,b):
    """
    # a,b为求取积分的上下限
    """
    return double_exp(b,popt[0],popt[1],popt[2]) - double_exp(a,popt[0],popt[1],popt[2])

def func(x):
    return popt[0]*np.exp(popt[1]*(x))*(1-np.exp(popt[2]*(x)))

def axis_x(temp,position):
    return '%f'%(x_rate*temp)

def axis_y(temp,position):
    return '%f'%(y_rate*temp)

for i in range(9949,circle):

    poly_func = poly[i*68:(i+1)*68]
    content = struct.unpack('<hhdddddddd', poly_func)
    x_list = []


    for m in range(2,10):
        x_list.append(float(content[m]))

    # 求取与脉冲发生的差值
    for j in range(8): 
        x_list[:] = [x - x_list[0] for x in x_list]

    x = np.array(x_list)
    # 对坐标进行放缩，方便拟合
    x_dexp = x/x_rate
    y_dexp = y/y_rate

    bounds = ([-2,-2,0],[0,0,2])
    popt, pcov = curve_fit(double_exp, x_dexp, y_dexp, bounds = bounds, maxfev=500000)
    # popt, pcov = curve_fit(double_exp, x_dexp, y_dexp, maxfev=500000)

    '''scipy模块的子模块optimize中提供的一个专门用于曲线拟合的函数curve_fit()
    # 官方详解链接：https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html#scipy-optimize-curve-fit
    # popt：阵列参数的最佳值，以使（扩展数据，*popt）-ydata平方残差之和最小。
    # pcov：二维阵列popt的估计协方差，对角线提供参数估计的方差。
    # perr = np.sqrt(np.diag(pcov))，使用perr计算参数的一个标准偏差误差。
    # bounds：参数的上下限。默认为无边界。元组的每个元素必须是长度等于参数数的数组，或者是标量（在这种情况下，所有参数的界限都是相同的）。
    # maxfev：拟合次数上限。
    '''

    print("所得双指数函数形式为：%f*exp(%f*(x))*(1-exp(%f*(x)))"%(popt[0],popt[1],popt[2]))

    x_inter = np.linspace(min(x_dexp),max(x_dexp),space)*x_rate  # 对函数输入数据进行插值，使得曲线更加光滑
    y_inter = func(x_inter)*y_rate # 拟合y值，并还原原来的y值

    # 蒙特卡洛积分法：误差偏大
    # E = integral(0, x_inter[-1])
    # E = integrate.quad(double_exp(x,popt[0],popt[1],popt[2]),0, x_inter[-1])

    # 绘制拟合的双指数曲线
    plt.rcParams['font.family'] = ['Times New Roman']
    plt.figure("双指数插值曲线")
    plt.plot(x_inter, y_inter, 'r',label='polyfit values')
    plt.plot(x, y, 's',label='original values')
    plt.title('Double exponential interpolation curve')
    plt.xlabel('Time(ns)')
    plt.ylabel('Voltage(mv)')
    # 放缩坐标轴，对放缩的数据进行还原
    # plt.gca().yaxis.set_major_formatter(FuncFormatter(axis_x))
    # plt.gca().xaxis.set_major_formatter(FuncFormatter(axis_y))
    plt.legend() 


    integral,error = integrate.quad(func,0, x_inter[-1])
    E = integral*x_rate*y_rate
    print("第%d次的积分值%f"%(i+1,E))

    plt.show()
