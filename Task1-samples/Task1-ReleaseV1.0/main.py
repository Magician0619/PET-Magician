#  -*- coding:utf-8 -*-

'''
#@Author: Magician
#@Date: 2020-09-22 19:23:50 
#@Description: 

Copyright 2020 by Magician
'''

from os import name
import struct

import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.type_check import nan_to_num

import pylab as pl
from scipy import integrate
from scipy.optimize import curve_fit

binFile = open('E:\\PET\\数据集\\6BDM.samples','rb')
poly = binFile.read()
print("字节长度：",len(poly))
frame = int(len(poly)/68)+1
print("帧数：",frame-1)

circle = 6500  # 分析多少组数据 （.xls文件的上限是65536）

global x_rate, y_rate 
global popt,popt_dict
global space
global bounds

x_rate = 1 # 将x单位进行放缩
y_rate = 1000 # 将y单位进行放缩
space = 2000
popt = []
popt_dict = ['a','b','d']
voltage_threshold = [40,110,180,270,270,180,110,40]
y = np.array(voltage_threshold)
bounds = ([-1000,-2,0],[0,0,2])

Energy_list = []
Energy_mean = 21875.05167
global max_value,nomrmal
max_value = 40000
normal = 511
global gx_rate,gy_rate
gx_rate = 100
gy_rate = 1600
global bins_w
bins_w = 1000

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

def gaussian_singletrue(x,*param):
    '''
    真实事件的高斯峰
    '''
    return param[1]*np.exp(-np.power(x - param[3], 2.) / (2 * np.power(param[5], 2.)))

def gaussian_2(x,*param):
    '''二元高斯函数拟合过程

    '''
    return param[0]*np.exp(-np.power(x - param[2], 2.) / (2 * np.power(param[4], 2.)))+\
           param[1]*np.exp(-np.power(x - param[3], 2.) / (2 * np.power(param[5], 2.)))

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

def draw_hist(lenths):
    
    # 绘制直方图
    bins1 = np.linspace(min(lenths),max(lenths),bins_w)
    n1, bins1, patches1 = pl.hist(lenths,bins1)

    # 能谱归一化
    n12 = n1.tolist()
    frequent_index = n12.index(max(n12)) 
    data = lenths*511/(0.5*(bins1[frequent_index]+bins1[frequent_index+1]))
    bins2 = np.linspace(min(data),max(data),bins_w)
    n2, bins2, patches2 = pl.hist(data,bins2)

    # 绘制高斯拟合图
    # bins比n多一个数
    # bins = np.delete(bins,-1) # 方法一：去除列表最后面的一个数
    guass_x = []
    guass_x = np.array(guass_x)
    guass_y = n2
    for i in range(len(bins2)-1):    #方法二：bins需要取矩形两端端点的均值
        temp = 0.5*(bins2[i]+bins2[i+1])
        guass_x = np.append(guass_x,temp)
    popt,pcov = curve_fit(gaussian_2,guass_x/gx_rate,guass_y/gy_rate,p0=[3,4,3,6,1,1],maxfev = 140000)

    plt.figure("高斯拟合图")
    plt.plot(guass_x,guass_y,'b*:',label='data')
    plt.plot(guass_x,gaussian_2(guass_x/gx_rate,*popt)*gy_rate,'r',label='fit')
    plt.legend()
    plt.show()
    print("高斯拟合的参数：",*popt)

    # 计算能量分辨率
    # 将大于半高度的横坐标保存下来，并追加列表，计算列表中首尾两项的差值

    global half_h_w_list
    half_h_w_list = []
    high = max(gaussian_singletrue(guass_x/gx_rate,*popt)*gy_rate)
    for x in guass_x:       
        if(int(gaussian_singletrue(x/gx_rate,*popt)*gy_rate)>int(0.5*high)):
            half_h_w_list = np.append(half_h_w_list,x)
    E_max = 511
    
    half_h_w = max(half_h_w_list)-min(half_h_w_list)
    eta = half_h_w/E_max
    print("能量分辨率为：",eta)
    


for i in range(circle):
    poly_func = poly[i*68:(i+1)*68]
    content = struct.unpack('<hhdddddddd', poly_func)
    x_list = []

    for m in range(2,10):
        x_list.append(float(content[m]))

    for j in range(8): 
        x_list[:] = [x - x_list[0] for x in x_list]

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
        Energy_list = np.append(Energy_list,E)


    except ValueError:
        print("ValueError: Residuals are not finite in the initial point.")
        print(popt)
        print("第%d帧数据所得双指数函数形式为：%f*exp(%f*(x))*(1-exp(%f*(x)))"%(i+1,popt[0],popt[1],popt[2]))
        # break
        # 目前已发现第6042组数据存在问题

        assert_popt(popt,bounds,i)
        x_inter = np.linspace(min(x_dexp),max(x_dexp),space)*x_rate
        y_inter = func(x_inter)*y_rate

        integral,error = integrate.quad(func,0, x_inter[-1])
        E = integral*x_rate*y_rate
        # print("第%d次的积分值为：%f"%(i+1,E))

        # 对错误数据修改成为固定的平均积分值
        Energy_list = np.append(Energy_list,Energy_mean)

draw_hist(Energy_list)

    
