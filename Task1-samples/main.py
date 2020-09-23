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


binFile = open('E:\\PET\\数据集\\6BDM.samples','rb')
poly = binFile.read()
print("字节长度：",len(poly))
cycle = int(len(poly)/68)+1
print("帧数：",cycle-1)

cycle = 10  # 分析前10组数据 

squares = []

for i in range(cycle):
    poly_func = poly[i*68:(i+1)*68]
    y_poly = struct.unpack('<hhdddddddd', poly_func)
    # print(c)
    for j in range(2,10): 
        squares.append(y_poly[j]-y_poly[2])
        # print("时间差：",c[j]-c[2])
   
def double_exp(x,a,b,c,d,e,f):
    '''
    双指数函数曲线
    '''
    # return  a*np.exp(b*x)+c*np.exp(d*x)+e
    # return  a*np.exp(b*x)+c*np.exp(d*x)
    return  a*np.exp(b*x)+c*np.exp(d*x)+e*x+f


##########################################
# 原始数据点散点绘图
##########################################
# 定义原始数据x、y的散点坐标
circle = 1
x = squares[0:8*circle]
x = np.array(x)
print('x的坐标:',x)

num = [40,110,180,270,270,180,110,40]
y = np.array(num*circle)
print('y的坐标:',y)

plt.figure("原始数据散点图")
plot1 = plt.plot(x, y, 's',label='original values')
plt.xlabel('Time(ns)')
plt.ylabel('Voltage(mv)')
plt.legend(loc=1) # 指定legend的位置右下角
plt.title('Sampling scatter diagram of scintillation pulse')

popt, pcov = curve_fit(double_exp, x, y)
'''
# 曲线拟合，并得到拟合曲线相关系数
# popt：阵列参数的最佳值，以使（扩展数据，*popt）-ydata平方残差之和最小
# pcov：二维阵列popt的估计协方差，对角线提供参数估计的方差。
# perr = np.sqrt(np.diag(pcov))，使用perr计算参数的一个标准偏差误差。
'''
# print("所得双指数函数形式为：%fexp(%f*x)+%fexp(%f*x)+%f"%(popt[0],popt[1],popt[2],popt[3],popt[4]))


##########################################
# 对数据进行插值，使得双指数曲线更加光滑
##########################################
x_inter = np.linspace(0,squares[7],1000)
y_inter = double_exp(x_inter,popt[0],popt[1],popt[2],popt[3],popt[4],popt[5]) #拟合y值

plt.figure("插值曲线")
plot2 = plt.plot(x_inter, y_inter, 'r',label='polyfit values')
'''
plt.xlabel('x')
plt.ylabel('y')
plt.legend(loc=1) # 指定legend的位置右下角
plt.title('curve_fit')
plt.show()
'''


##########################################
# 多项式拟合曲线
##########################################
poly = np.polyfit(x,y,3)   # 用7次多项式拟合x，y数组
poly_func = np.poly1d(poly)    # 拟合完之后用这个函数来生成多项式对象
y_poly = poly_func(x)    # 生成多项式对象之后，就是获取x在这个多项式处的值
plt.figure("多项式曲线")
plt.scatter(x,y,marker='o',label='original datas')#对原始数据画散点图
plt.plot(x,y,ls='--',c='red',label='fitting with 4-degree polynomial')#对拟合之后的数据，也就是x，c数组画图
c_inter = poly_func(x_inter)    # 插值数据进行绘图
plt.plot(x_inter,c_inter,ls='--',c='green',label='Interpolation')#对拟合之后的数据，也就是x，c数组画图
plt.legend()

plt.show()



##########################################
# 多项式拟合曲线
##########################################

