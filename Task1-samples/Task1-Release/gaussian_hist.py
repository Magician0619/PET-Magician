import os
from matplotlib import patches
# from matplotlib.pyplot import plt
import pylab as plt
from numpy import array
import numpy as np
import pylab as pl
from scipy.optimize import curve_fit


oriPath = "Task1-samples\\energy.csv"
global max_value,nomrmal
max_value = 40000
normal = 511
global gx_rate,gy_rate
gx_rate = 100
gy_rate = 20


def get_data(lines):
    '''
    读取数据
    '''
    sizeArry = []
    for line in lines:
        line = line.replace('\n',"")
        line = int(float(line))
        sizeArry.append(line)
    return array(sizeArry)

# 首先打开文件从文件中读取数据
f = open(oriPath,encoding="utf-8")
Lenths = get_data(f.readlines())

def gaussian(x,*param):
    return param[0]*np.exp(-np.power(x - param[2], 2.) / (2 * np.power(param[4], 2.)))+\
           param[1]*np.exp(-np.power(x - param[3], 2.) / (2 * np.power(param[5], 2.)))

def draw_hist(lenths):
    data = lenths/max_value*normal  # 对数据归一化
    bins = np.linspace(min(data),600,200)


    n, bins, patches = pl.hist(data,bins)
    
    # 绘制直方图
    pl.xlabel('Energy')
    pl.ylabel('Counts')
    pl.title('The energy spectra and coincidence-time histograms')
    pl.show()

    # 绘制高斯拟合图
    # bins比n多一个数
    # bins = np.delete(bins,-1) # 方法一：去除列表最后面的一个数
    guass_x = []
    guass_x = np.array(guass_x)
    guass_y = n
    for i in range(len(bins)-1):    #方法二：bins需要取矩形两端端点的均值
        temp = 0.5*(bins[i]+bins[i+1])
        guass_x = np.append(guass_x,temp)
    popt,pcov = curve_fit(gaussian,guass_x,guass_y,p0=[60,80,60,120,20,20],maxfev = 140000)
    plt.plot(guass_x,guass_y,'b+:',label='data')
    plt.plot(guass_x,gaussian(guass_x,*popt),'ro:',label='fit')
    plt.legend()
    plt.show()

    # 计算能量分辨率
    eta0 = abs(gaussian(guass_x,*popt)-guass_y)/guass_y
    eta0[np.isinf(eta0)]=0
    eta =np.mean(eta0)
    print("能量的分辨率为：%f"%(eta))
    
draw_hist(Lenths)


