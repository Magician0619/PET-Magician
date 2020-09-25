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
from matplotlib.ticker import FuncFormatter
from sympy import * 
# import sympy.integrals.manualintegrate
# from scipy.integrate import tplquad,dblquad,quad


binFile = open('E:\\PET\\数据集\\6BDM.samples','rb')
poly = binFile.read()
print("字节长度：",len(poly))
cycle = int(len(poly)/68)+1
print("帧数：",cycle-1)

cycle = 100  # 分析前100组数据 

squares = []

for i in range(cycle):
    poly_func = poly[i*68:(i+1)*68]
    y_poly = struct.unpack('<hhdddddddd', poly_func)
    # print(c)
    for j in range(2,10): 
        squares.append(y_poly[j]-y_poly[2])
        # print("时间差：",c[j]-c[2])
   
# def double_exp(x,a,b,c,d,e,f):
def double_exp(x,a,b,c,d):
    '''
    双指数函数曲线
    '''
    return  a*np.exp(b*x)+c*np.exp(d*x)
    # return  a*np.exp(b*x)+c*np.exp(d*x)+e
    # return  a*np.exp(b*x)+c*np.exp(d*x)+e*x+f


##########################################
# 原始数据点散点绘图
##########################################
# 定义原始数据x、y的散点坐标
circle = 1  # 是否需要多组数据共同拟合曲线，增加曲线拟合的准确性
global rate 
rate = 1000 # 将单位进行放缩
num = [40,110,180,270,270,180,110,40]
y = np.array(num*circle)


for i in range(circle):
    x = squares[8*(circle-1):8*circle]
    x = np.array(x)
    x_dexp = x/rate
    y_dexp = y/rate 
    popt, pcov = curve_fit(double_exp, x_dexp, y_dexp)



##########################################
# 双指数曲线拟合
##########################################




# bounds=(-20,[0.01,0.01,0.01,0.01,0.01,0.01])
'''
# 曲线拟合，并得到拟合曲线相关系数
# popt：阵列参数的最佳值，以使（扩展数据，*popt）-ydata平方残差之和最小
# pcov：二维阵列popt的估计协方差，对角线提供参数估计的方差。
# perr = np.sqrt(np.diag(pcov))，使用perr计算参数的一个标准偏差误差。
'''
print("所得双指数函数形式为：%fexp(%f*x)+%fexp(%f*x)"%(popt[0],popt[1],popt[2],popt[3]))

# 对数据进行插值，使得双指数曲线更加光滑
x_inter = np.linspace(0,x_dexp[7],1000)
y_inter = double_exp(x_inter,popt[0],popt[1],popt[2],popt[3]) #拟合y值


plt.rcParams['font.family'] = ['Times New Roman']
# plt.rcParams.update({'font.size': 8})
plt.figure("双指数插值曲线")
plt.plot(x_inter, y_inter, 'r',label='polyfit values')
# plt.plot(x, y, 's',label='original values')
plt.title('Double exponential interpolation curve')
plt.xlabel('Time(ns)')
plt.ylabel('Voltage(mv)')
# 放缩坐标轴

def axis_scale(temp, position):
    return '%1.0f'%(rate*temp)

plt.gca().yaxis.set_major_formatter(FuncFormatter(axis_scale))
plt.gca().xaxis.set_major_formatter(FuncFormatter(axis_scale))
plt.legend() 





##########################################
# 多项式拟合曲线
##########################################
poly = np.polyfit(x,y,5)   # 用5次多项式拟合x，y数组
poly_func = np.poly1d(poly)    # 拟合完之后用这个函数来生成多项式对象
y_poly = poly_func(x)    # 生成多项式对象之后，就是获取x在这个多项式处的值
plt.figure("多项式曲线")
plt.scatter(x,y,marker='o',label='original data')#对原始数据画散点图
c_inter = poly_func(x_inter)    # 插值数据进行绘图
plt.plot(x_inter,c_inter,ls='--',c='green',label='fitting curve')#对拟合之后的数据，也就是x，c数组画图
plt.title('Polynomial fitting curve')
plt.xlabel('Time(ns)')
plt.ylabel('Voltage(mv)')
plt.legend() 






##########################################
# 计算脉冲积分，脉冲电压值对时间的积分
# 蒙特卡洛方法
##########################################

'''
x = symbols('x')
E = integrate(popt[1]*np.exp(popt[2]*x)+popt[3]*np.exp(d*x), (x, 0, x_inter[-1]))
# 似乎对指数无法求积分，待解决！！
'''

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


##########################################
# 对前10组数据进行能谱分析
##########################################
cycle = 100

for i in range(cycle):
    poly_func = poly[i*68:(i+1)*68]
    y_poly = struct.unpack('<hhdddddddd', poly_func)
    # print(c)
    for j in range(2,10): 
        squares.append(y_poly[j]-y_poly[2])


E = integral(0, x_inter[-1])*((rate)**2)

print("积分结果：",E)









plt.show()