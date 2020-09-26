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
    bins = np.delete(bins,-1)
    popt,pcov = curve_fit(gaussian,bins,n,p0=[3,4,3,6,1,1])
    plt.plot(bins,n,'b+:',label='data')
    plt.plot(bins,gaussian(bins,*popt),'ro:',label='fit')
    plt.legend()
    plt.show()
    



draw_hist(Lenths)


