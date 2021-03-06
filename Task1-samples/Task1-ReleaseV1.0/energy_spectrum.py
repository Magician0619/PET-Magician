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
import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xlwt
from matplotlib.ticker import FuncFormatter
# from sympy import * 
from scipy import integrate
from scipy.optimize import curve_fit

f = xlwt.Workbook()
sheet1 = f.add_sheet(u'sheet1',cell_overwrite_ok=True)
row0 = [u'nB',u'nC',u'T1',u'T2',u'T3',u'T4',u'T5',u'T6',u'T7',u'T8',u'Energy']
column = ''
status = ''
for i in range(0,len(row0)):
    sheet1.write(0,i,row0[i])

binFile = open('E:\\PET\\数据集\\6BDM.samples','rb')
poly = binFile.read()
print("字节长度：",len(poly))
frame = int(len(poly)/68)+1
print("帧数：",frame-1)

circle = 65000  # 分析多少组数据 （.xls文件的上限是65536）

global x_rate, y_rate 
global popt,popt_dict
global space
global bounds
x_rate = 1 # 将x单位进行放缩
y_rate = 1000 # 将y单位进行放缩
space = 2000
popt = []
popt_dict = ['a','b','d']
num = [40,110,180,270,270,180,110,40]
y = np.array(num)
bounds = ([-500,-2,0],[0,0,2])


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
    return (b-a)/len(x)*sum(double_exp(x,popt[0],popt[1],popt[2],popt[3]))

def integral(a,b):
    """
    # a,b为求取积分的上下限
    """
    return double_exp(b,popt[0],popt[1],popt[2],popt[3]) - double_exp(a,popt[0],popt[1],popt[2],popt[3])

def func(x):
    return popt[0]*np.exp(popt[1]*(x))*(1-np.exp(popt[2]*(x)))

def assert_popt(popt,bounds,num):
    '''检查拟合参数是否需要调整
    参数：
    --------
    popt：拟合得到的参数
    bounds：参数范围
    num：第num+1次拟合
    '''
    for i in range(3):
        assert (popt[i]!=bounds[0][i]), "参数%s下限值应该调整!!!\n第%d帧数据所得双指数函数形式为：%f*exp(%f*(x))*(1-exp(%f*(x)))"%(popt_dict[i],num+1,popt[0],popt[1],popt[2])
        assert (popt[i]!=bounds[1][i]), "参数%s上限值应该调整!!!\n第%d帧数据所得双指数函数形式为：%f*exp(%f*(x))*(1-exp(%f*(x)))"%(popt_dict[i],num+1,popt[0],popt[1],popt[2])

for i in range(circle):
    poly_func = poly[i*68:(i+1)*68]
    content = struct.unpack('<hhdddddddd', poly_func)
    x_list = []


    for k in range(2):
        sheet1.write(i+1,k,content[k]) 

    for m in range(2,10):
        x_list.append(float(content[m]))

    for j in range(8): 
        x_list[:] = [x - x_list[0] for x in x_list]
        sheet1.write(i+1,j+2,x_list[j])

    x = np.array(x_list)
    x_dexp = x/x_rate
    y_dexp = y/y_rate

    # 对curve_fit函数的异常结果进行捕获    
    try: 
        popt, pcov = curve_fit(double_exp, x_dexp, y_dexp, bounds = bounds, maxfev=5000000)

        assert_popt(popt,bounds,i)
        # print("第%d帧数据所得双指数函数形式为：%f*exp(%f*(x))*(1-exp(%f*(x)))"%(i+1,popt[0],popt[1],popt[2]))
        x_inter = np.linspace(min(x_dexp),max(x_dexp),space)*x_rate
        y_inter = func(x_inter)*y_rate

        integral,error = integrate.quad(func,0, x_inter[-1])
        E = integral*x_rate*y_rate
        # print("第%d次的积分值为：%f"%(i+1,E))
        sheet1.write(i+1,10,E)

    except ValueError:
        print("ValueError: Residuals are not finite in the initial point.")
        print(popt)
        print("第%d帧数据所得双指数函数形式为：%f*exp(%f*(x))*(1-exp(%f*(x)))"%(i+1,popt[0],popt[1],popt[2]))
        # break
        

        assert_popt(popt,bounds,i)
        x_inter = np.linspace(min(x_dexp),max(x_dexp),space)*x_rate
        y_inter = func(x_inter)*y_rate

        integral,error = integrate.quad(func,0, x_inter[-1])
        E = integral*x_rate*y_rate
        # print("第%d次的积分值为：%f"%(i+1,E))

        # 对错误数据修改成为固定的平均积分值
        sheet1.write(i+1,10,21875.05167)
        # 22029.78739

    



f.save("Task1-samples\\Task1-ReleaseV1.0\\spectrum_%s_%s.xls"%(circle,datetime.datetime.now().strftime('%Y-%m-%d'))) #保存文件
