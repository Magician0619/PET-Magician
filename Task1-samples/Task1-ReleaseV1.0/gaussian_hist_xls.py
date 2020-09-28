
import matplotlib.mlab as mlab
from re import error
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
gx_rate = 10
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

def gaussian_1(x):
    num_bins = 30 #直方图柱子的数量 
    n, bins, patches = plt.hist(x, num_bins,normed=1, facecolor='blue', alpha=0.5) 
    #直方图函数，x为x轴的值，normed=1表示为概率密度，即和为一，绿色方块，色深参数0.5.返回n个概率，直方块左边线的x值，及各个方块对象 
    y = mlab.normpdf(bins, mu, sigma)#拟合一条最佳正态分布曲线y 
    plt.plot(bins, y, 'r--') #绘制y的曲线 
    plt.xlabel('Energy') #绘制x轴 
    plt.ylabel('Probability') #绘制y轴 
    plt.title(r'Histogram : $\mu=5.8433$,$\sigma=0.8253$')#中文标题 u'xxx' 
    plt.subplots_adjust(left=0.15)#左边距 
    plt.show()
def gaussian_2(x,*param):
    '''二元高斯函数拟合过程

    '''
    return param[0]*np.exp(-np.power(x - param[2], 2.) / (2 * np.power(param[4], 2.)))+\
           param[1]*np.exp(-np.power(x - param[3], 2.) / (2 * np.power(param[5], 2.)))

def gaussian_3(x,a1,a2,a3,m1,m2,m3,s1,s2,s3):   # 三元高斯拟合函数 
     
    return a1*np.exp(-((x-m1)/s1)**2)+a2*np.exp(-((x-m2)/s2)**2)+a3*np.exp(-((x-m3)/s3)**2)

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
    popt,pcov = curve_fit(gaussian_2,guass_x,guass_y,p0=[70,80,60,120,20,20],maxfev = 140000)
    plt.plot(guass_x,guass_y,'b+:',label='data')
    plt.plot(guass_x,gaussian_2(guass_x,*popt),'ro:',label='fit')
    plt.legend()
    plt.show()

    # 计算能量分辨率
    global half_h_w1, half_h_w2,E_max
    half_h_w1, half_h_w2 = 0,0
    high = max(gaussian_2(guass_x,*popt))
    try:
        for x in guass_x:       
            if(x<256|int(gaussian_2(x))==int(0.5*high)):
                half_h_w1 = x
            if(x<256|int(gaussian_2(x))==int(0.5*high)):
                half_h_w2 = x
            if(int(gaussian_2(guass_x)==high)):
                E_max = x
            half_h_w = half_h_w2-half_h_w1
            eta = half_h_w/E_max
            print("能量分辨率为：",eta)

    except error:
        print("报错了！！！")
        pass
            
    
draw_hist(Lenths)


